import csv
import io

from celery import shared_task
from django.db import transaction

from .emails import send_ingestion_report
from .models import Author, Book, IngestionLog, normalize_name


def format_isbn(value):
    """Ensure ISBN is stored correctly as a string without scientific notation issues."""
    if not value:
        return None
    value = value.strip()

    if "e" in value.lower():
        return None

    return value


def book_exists(row):
    """Check if a book exists based on title and authors (mandatory), and optionally isbn13 or isbn."""
    isbn13 = format_isbn(row.get("isbn13", ""))
    isbn = format_isbn(row.get("isbn", ""))
    title = row.get("title", "").strip()
    authors = row.get("authors", "").strip()

    if not title or not authors:
        return False

    queryset = Book.objects.none()

    if isbn13:
        queryset |= Book.objects.filter(isbn13=isbn13)

    if isbn:
        queryset |= Book.objects.filter(isbn=isbn)

    author_list = [author.strip() for author in authors.split(",")]
    queryset |= Book.objects.filter(title=title, authors__name__in=author_list)

    return queryset.exists()


#TODO: Make this a bulk operation
@shared_task
def process_csv(file_data, admin_email, filename):
    """Process CSV file where each row is handled independently to prevent blocking on failure."""
    books_processed = 0
    books_inserted = 0
    books_skipped = 0
    errors = []

    try:
        decoded_file = file_data.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        for row in csv_reader:
            try:
                with transaction.atomic():
                    books_processed += 1

                    if book_exists(row):
                        books_skipped += 1
                        continue

                    authors_list = [name.strip() for name in row["authors"].split(",")]
                    author_instances = []

                    for author_name in authors_list:
                        normalized_name = normalize_name(author_name)

                        author = None
                        if normalized_name:
                            author = Author.objects.filter(normalized_name=normalized_name).first()
                            if author:
                                author_instances.append(author)

                        if not author:
                            author, _ = Author.objects.get_or_create(name=author_name)
                            author.normalized_name = normalize_name(author.name)
                            author.save()
                            author_instances.append(author)

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
                        if row.get("work_text_reviews_count") else None,
                    )

                    book.authors.set(author_instances)
                    books_inserted += 1

            except Exception as e:
                errors.append(f"Error processing book '{row.get('title', 'Unknown')}': {str(e)}")
                continue

        IngestionLog.objects.create(
            filename=filename,
            records_processed=books_inserted,
            errors="; ".join(errors) if errors else None,
        )

        send_ingestion_report(books_processed, books_inserted, books_skipped, errors, filename, admin_email)

        return books_inserted, errors

    except Exception as e:
        errors.append(str(e))
        return 0, "Critical error: " + str(e)
