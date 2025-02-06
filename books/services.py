import csv
import io
from django.core.mail import send_mail
from django.db import transaction
from .models import Book, Author, IngestionLog

from decimal import Decimal  # Import Decimal to safely convert large numbers


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

    # Simply return the value as a string (no int conversion)
    return value  # Keep it as a string to preserve leading zeros


def process_csv(file):
    """Process CSV file efficiently while ensuring correct author assignments and sending an email report."""
    books_processed = 0
    books_inserted = 0
    books_skipped = 0
    errors = []
    authors_cache = {}

    try:
        decoded_file = file.read().decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        # Fetch existing books based on isbn13, isbn, or title+authors fallback
        existing_books = {
            (book.isbn13 or book.isbn or f"{book.title}_{','.join(a.name for a in book.authors.all())}"): book
            for book in Book.objects.prefetch_related("authors").all()
        }
        existing_book_keys = set(existing_books.keys())

        with transaction.atomic():
            for row in csv_reader:
                try:
                    books_processed += 1

                    # Determine book's unique identifier
                    book_identifier = (
                        row.get("isbn13") or row.get("isbn")
                        or f"{row.get('title', '').strip()}_{row.get('authors', '').strip()}"
                    )

                    # Skip if the book already exists
                    if book_identifier in existing_book_keys:
                        books_skipped += 1
                        continue

                    authors_list = [name.strip() for name in row["authors"].split(",")]
                    author_instances = []

                    for author_name in authors_list:
                        if author_name not in authors_cache:
                            author, _ = Author.objects.get_or_create(name=author_name)
                            authors_cache[author_name] = author
                        author_instances.append(authors_cache[author_name])

                    # Insert book one by one
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
                        language_code=row.get("language_code", "").strip() or None,
                        average_rating=float(row["average_rating"]) if row.get("average_rating") else None,
                        ratings_count=int(float(row["ratings_count"])) if row.get("ratings_count") else None,
                        image_url=row.get("image_url", "").strip() or None,
                        small_image_url=row.get("small_image_url", "").strip() or None,
                    )

                    # Assign authors immediately after inserting book
                    book.authors.set(author_instances)

                    existing_book_keys.add(book_identifier)  # Mark book as inserted
                    books_inserted += 1

                except Exception as e:
                    errors.append(f"Error processing book '{row.get('title', 'Unknown')}': {str(e)}")
                    continue

        # Send email notification
        #send_ingestion_report(books_processed, books_inserted, books_skipped, errors, file.name)

        # Log the ingestion process
        IngestionLog.objects.create(
            filename=file.name,
            records_processed=books_inserted,
            errors="; ".join(errors) if errors else None,
        )

        return books_inserted, f"Processed: {books_processed}, Inserted: {books_inserted}, Skipped: {books_skipped}, Errors: {len(errors)}"

    except Exception as e:
        errors.append(str(e))
        return 0, "Critical error: " + str(e)
