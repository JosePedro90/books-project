from unittest.mock import patch

from books.models import Author, Book, IngestionLog
from books.tasks import process_csv
from django.test import TestCase


class ProcessCSVTests(TestCase):

    @patch("books.tasks.send_ingestion_report")
    def test_process_csv_successful(self, mock_send_email):
        file_data = b"title,authors,isbn13,goodreads_book_id,best_book_id,work_id,books_count,original_publication_year,original_title,language_code,average_rating,ratings_count,image_url,small_image_url,ratings_1,ratings_2,ratings_3,ratings_4,ratings_5,work_ratings_count,work_text_reviews_count\nTest Book,Test Author 1,9780321765723,1,2,3,4,2000,Original Title,en,4.5,1000,http://example.com/image.jpg,http://example.com/small_image.jpg,100,150,250,200,300,500,200"
        admin_email = "test@example.com"
        filename = "test.csv"

        books_inserted, books_skipped, errors = process_csv(file_data, admin_email, filename)

        self.assertEqual(books_inserted, 1)
        self.assertEqual(books_skipped, 0)
        self.assertEqual(errors, [])
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(IngestionLog.objects.count(), 1)

        log = IngestionLog.objects.first()
        self.assertEqual(log.filename, filename)
        self.assertEqual(log.records_processed, 1)
        self.assertIsNone(log.errors)

        mock_send_email.assert_called_once_with(1, 1, 0, [], filename, admin_email)

    @patch("books.tasks.send_ingestion_report")
    def test_process_csv_with_errors(self, mock_send_email):
        file_data = b"title,authors,isbn13,average_rating\nTest Book 1,Test Author 1,invalid_isbn-too-loooong,4.5\nTest Book 2,Test Author 2,9780321765723,invalid_rating"  # Invalid ISBN and rating
        admin_email = "test@example.com"
        filename = "test.csv"

        books_inserted, books_skipped, errors = process_csv(file_data, admin_email, filename)

        self.assertEqual(books_inserted, 0)
        self.assertEqual(books_skipped, 0)
        self.assertEqual(len(errors), 2)
        self.assertIn("Error processing book 'Test Book 1': value too long for type character varying(13)", errors[0])
        self.assertIn(
            "Error processing book 'Test Book 2': could not convert string to float: 'invalid_rating", errors[1]
        )

        mock_send_email.assert_called_once()

    @patch("books.tasks.send_ingestion_report")
    def test_process_csv_with_existing_book(self, mock_send_email):
        author = Author.objects.create(name="Test Author 1")
        book = Book.objects.create(title="Test Book", isbn13="9780321765723")
        book.authors.add(author)
        file_data = b"title,authors,isbn13\nTest Book,Test Author 1,9780321765723"  # Same book as above
        admin_email = "test@example.com"
        filename = "test.csv"

        books_inserted, books_skipped, errors = process_csv(file_data, admin_email, filename)

        self.assertEqual(books_inserted, 0)
        self.assertEqual(books_skipped, 1)
        self.assertEqual(errors, [])
        mock_send_email.assert_called_once()

    @patch("books.tasks.send_ingestion_report")
    def test_process_csv_empty_file(self, mock_send_email):
        file_data = b""  # Empty file
        admin_email = "test@example.com"
        filename = "test.csv"

        books_inserted, books_skipped, errors = process_csv(file_data, admin_email, filename)

        self.assertEqual(books_inserted, 0)
        self.assertEqual(errors, [])
        mock_send_email.assert_called_once_with(0, 0, 0, [], filename, admin_email)

    @patch("books.tasks.send_ingestion_report")
    def test_process_csv_invalid_csv_format(self, mock_send_email):
        file_data = b"title,authors\nTest Book"
        admin_email = "test@example.com"
        filename = "test.csv"

        books_inserted, books_skipped, errors = process_csv(file_data, admin_email, filename)

        self.assertEqual(books_inserted, 0)
        self.assertEqual(errors, ["Error processing book 'Test Book': 'NoneType' object has no attribute 'strip'"])
        mock_send_email.assert_called_once_with(1, 0, 0, errors, filename, admin_email)
