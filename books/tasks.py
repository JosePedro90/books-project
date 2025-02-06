import csv
import io

from celery import shared_task
from django.db import transaction

from .emails import send_ingestion_report
from .models import Book, Author, IngestionLog


def format_isbn(value):
    """Ensure ISBN is stored correctly as a string without scientific notation issues."""
    if not value:
        return None
    value = value.strip()

    # Check if the value is in scientific notation (contains 'e'),
    # it can result in losing leading zeros or modifying the number,
    # especially if the number is in scientific notation.
    if "e" in value.lower():
        return None  # Discard

    return value  # Keep it as a string to preserve leading zeros


def book_exists(row):
    """Check if a book exists based on title and authors (mandatory), and optionally isbn13 or isbn."""
    # Create identifiers for isbn13, isbn, title, and authors
    isbn13 = format_isbn(row.get("isbn13", ""))
    isbn = format_isbn(row.get("isbn", ""))
    title = row.get("title", "").strip()
    authors = row.get("authors", "").strip()

    # Ensure title and authors are present before querying
    if not title or not authors:
        return False  # Title and authors are mandatory, return False if either is missing

    # Create the base queryset
    queryset = Book.objects.none()

    # Check isbn13 and isbn only if they are present
    if isbn13:
        queryset |= Book.objects.filter(isbn13=isbn13)

    if isbn:
        queryset |= Book.objects.filter(isbn=isbn)

    # Always check for title and authors
    author_list = [author.strip() for author in authors.split(",")]
    queryset |= Book.objects.filter(title=title, authors__name__in=author_list)

    # Return if any records match
    return queryset.exists()


@shared_task
def process_csv(file_data, admin_email, filename):
    """Process CSV file where each row is handled independently to prevent blocking on failure."""
    books_processed = 0
    books_inserted = 0
    books_skipped = 0
    errors = []
    authors_cache = {}

    try:
        decoded_file = file_data.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        for row in csv_reader:
            try:
                with transaction.atomic():  # Each row has its own transaction
                    books_processed += 1

                    # Check if the book already exists
                    if book_exists(row):
                        books_skipped += 1
                        continue

                    authors_list = [name.strip() for name in row["authors"].split(",")]
                    author_instances = []

                    for author_name in authors_list:
                        if author_name not in authors_cache:
                            author, _ = Author.objects.get_or_create(name=author_name)
                            authors_cache[author_name] = author
                        author_instances.append(authors_cache[author_name])

                    # Insert the new book
                    #TODO: Improve the way to handle missing value and type conversion
                    book = Book.objects.create(
                        isbn13=format_isbn(row.get("isbn13", "")),
                        isbn=format_isbn(row.get("isbn", "")),
                        goodreads_book_id=int(float(row["goodreads_book_id"]))
                        if row.get("goodreads_book_id") else None,
                        best_book_id=int(float(row["best_book_id"])) if row.get("best_book_id") else None,
                        work_id=int(float(row["work_id"])) if row.get("work_id") else None,
                        books_count=int(float(row["books_count"])) if row.get("books_count") else 1,
                        original_publication_year=int(float(row["original_publication_year"]))
                        if row.get("original_publication_year") else None,
                        title=row.get("title", "").strip() or None,
                        original_title=row.get("original_title", "").strip() or None,
                        language_code=row.get("language_code", "").strip() or None,
                        average_rating=float(row["average_rating"]) if row.get("average_rating") else None,
                        ratings_count=int(float(row["ratings_count"])) if row.get("ratings_count") else None,
                        image_url=row.get("image_url", "").strip() or None,
                        small_image_url=row.get("small_image_url", "").strip() or None,
                        ratings_1=int(float(row["ratings_1"])) if row.get("ratings_1") else None,
                        ratings_2=int(float(row["ratings_2"])) if row.get("ratings_2") else None,
                        ratings_3=int(float(row["ratings_3"])) if row.get("ratings_3") else None,
                        ratings_4=int(float(row["ratings_4"])) if row.get("ratings_4") else None,
                        ratings_5=int(float(row["ratings_5"])) if row.get("ratings_5") else None,
                        work_ratings_count=int(float(row["work_ratings_count"]))
                        if row.get("work_ratings_count") else None,
                        work_text_reviews_count=int(float(row["work_text_reviews_count"]))
                    )

                    # Assign authors immediately after inserting book
                    book.authors.set(author_instances)
                    books_inserted += 1

            except Exception as e:
                errors.append(f"Error processing book '{row.get('title', 'Unknown')}': {str(e)}")
                continue  # Continue processing next row even if this one fails

        # Log the ingestion process
        IngestionLog.objects.create(
            filename=filename,
            records_processed=books_inserted,
            errors="; ".join(errors) if errors else None,
        )
        # Send report
        send_ingestion_report(books_processed, books_inserted, books_skipped, errors, filename, admin_email)

        return books_inserted, errors

    except Exception as e:
        errors.append(str(e))
        return 0, "Critical error: " + str(e)
