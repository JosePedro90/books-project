import csv
import io

from celery import shared_task
from django.db import transaction

from .emails import send_ingestion_report
from .models import Author, Book, IngestionLog, normalize_name


def format_isbn(value):
    """Ensure ISBN is stored correctly as a string."""
    if not value:
        return None
    value = value.strip()
    if "e" in value.lower():  # Discard scientific notation values
        return None
    return value


def book_exists(row):
    """Check if a book exists."""
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


@shared_task
def process_csv(file_data, admin_email, filename):
    """Process CSV file, insert new books and authors, and log errors."""

    books_processed = 0
    books_inserted = 0
    books_skipped = 0
    errors = []

    try:
        decoded_file = file_data.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(decoded_file))

        books_to_create = []
        author_names = set()
        rows_to_process = []

        for row in csv_reader:
            rows_to_process.append(row)
            try:
                books_processed += 1
                if book_exists(row):
                    books_skipped += 1
                    continue

                authors_str = row.get("authors")
                if authors_str:
                    for author_name in authors_str.split(","):
                        author_names.add(normalize_name(author_name.strip()))
                books_to_create.append(row)
            except Exception as e:
                errors.append(f"Error preparing book '{row.get('title', 'Unknown')}': {str(e)}")

        with transaction.atomic():
            author_instances = {}
            existing_authors = {
                author.normalized_name: author
                for author in Author.objects.filter(normalized_name__in=author_names)
            }
            authors_to_create = []

            for author_name in author_names:
                if author_name not in existing_authors:
                    original_name = next((name for name in author_names if normalize_name(name) == author_name),
                                         author_name)
                    authors_to_create.append(Author(name=original_name))

            new_authors = Author.objects.bulk_create(authors_to_create)
            for author in new_authors:
                author_instances[author.normalized_name] = author

            author_instances.update(existing_authors)

            # Prepare book objects for bulk insertion
            book_instances = []
            for row in books_to_create:
                try:
                    book = Book(
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
                    book_instances.append(book)
                except (ValueError, TypeError) as e:
                    errors.append(f"Error converting data for '{row.get('title', 'Unknown')}': {str(e)}")
                    continue

            # Bulk insert books in chunks for efficiency
            CHUNK_SIZE = 1000
            for i in range(0, len(book_instances), CHUNK_SIZE):
                chunk = book_instances[i:i + CHUNK_SIZE]
                created_books = Book.objects.bulk_create(chunk)
                for j, book in enumerate(created_books):
                    authors_str = books_to_create[i + j].get("authors")
                    if authors_str:
                        authors_list = [author.strip() for author in authors_str.split(",")]
                        book.authors.set([
                            author_instances[normalize_name(author_name)] for author_name in authors_list
                            if normalize_name(author_name) in author_instances
                        ])
                    books_inserted += 1

        # Log ingestion details
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
