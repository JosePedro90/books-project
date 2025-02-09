from books.models import Author, Book
from books.serializers import (AuthorSerializer, BookSerializer, CSVUploadSerializer, IngestionLogSerializer)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from reservations.models import Reservation


class AuthorSerializerTests(TestCase):

    def test_author_serializer_valid_data(self):
        data = {
            'name': 'John Doe'
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.name, 'John Doe')

    def test_author_serializer_invalid_data(self):
        data = {
            'name': ''
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class BookSerializerTests(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")

    def test_book_serializer_valid_data(self):
        data = {
            'title': 'Test Book',
            'authors_input': 'Test Author 1, Test Author 2',  # Comma-separated authors
            'isbn': '9780321765',
            'isbn13': '9780321765723',
            'goodreads_book_id': 123,
            'best_book_id': 456,
            'work_id': 789,
            'books_count': 2,
            'original_publication_year': 2000,
            'original_title': 'Original Title',
            'language_code': 'en',
            'average_rating': 4.5,
            'ratings_count': 1000,
            'work_ratings_count': 500,
            'work_text_reviews_count': 200,
            'ratings_1': 100,
            'ratings_2': 150,
            'ratings_3': 250,
            'ratings_4': 200,
            'ratings_5': 300,
            'image_url': 'http://example.com/image.jpg',
            'small_image_url': 'http://example.com/small_image.jpg',
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()

        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.authors.count(), 2)
        self.assertIn(self.author1, book.authors.all())
        self.assertIn(self.author2, book.authors.all())
        self.assertEqual(book.isbn, '9780321765')

    def test_book_serializer_invalid_data(self):
        data = {
            'title': ''
        }  # Invalid: Empty title
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_book_serializer_create_new_authors(self):
        data = {
            'title': 'Test Book',
            'authors_input': 'New Author 1, New Author 2',
            # ... other book data
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.authors.count(), 2)
        self.assertTrue(Author.objects.filter(name="New Author 1").exists())
        self.assertTrue(Author.objects.filter(name="New Author 2").exists())

    def test_book_serializer_update_authors(self):
        book = Book.objects.create(title="Existing Book")
        book.authors.add(self.author1)

        data = {
            'title': 'Updated Book Title',
            'authors_input': 'Test Author 2, New Author 3',
        }
        serializer = BookSerializer(instance=book, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_book = serializer.save()

        self.assertEqual(updated_book.title, 'Updated Book Title')
        self.assertEqual(updated_book.authors.count(), 2)
        self.assertIn(self.author2, updated_book.authors.all())
        self.assertTrue(Author.objects.filter(name="New Author 3").exists())
        self.assertNotIn(self.author1, updated_book.authors.all())

    def test_book_serializer_get_reserved(self):
        book = Book.objects.create(title="Test Book", isbn="1234567890", isbn13='1234567890123')
        self.assertFalse(BookSerializer(book).data['reserved'])  # No reservations

        Reservation.objects.create(book=book, status='reserved', name="Test User", email="test@example.com")
        self.assertTrue(BookSerializer(book).data['reserved'])

    def test_book_serializer_multiple_reservations_get(self):
        book = Book.objects.create(title="Test Book", isbn="1234567891", isbn13='1234567891123')
        self.assertFalse(BookSerializer(book).data['reserved'])  # No reservations

        Reservation.objects.create(book=book, status='returned', name="Test User", email="test@example.com")
        self.assertFalse(BookSerializer(book).data['reserved'])
        Reservation.objects.create(book=book, status='reserved', name="Test User", email="test@example.com")
        self.assertTrue(BookSerializer(book).data['reserved'])


class IngestionLogSerializerTests(TestCase):

    def test_ingestion_log_serializer_valid_data(self):
        data = {
            'filename': 'test.csv',
            'records_processed': 10,
            'errors': 'Some errors'
        }
        serializer = IngestionLogSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        log = serializer.save()
        self.assertEqual(log.filename, 'test.csv')

    def test_ingestion_log_serializer_invalid_data(self):
        data = {
            'filename': ''
        }  # Invalid: Empty filename
        serializer = IngestionLogSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('filename', serializer.errors)


class CSVUploadSerializerTests(TestCase):

    def test_csv_upload_serializer_valid_data(self):
        csv_file = SimpleUploadedFile("test.csv", b"title,author\nBook 1,Author 1")
        data = {
            'file': csv_file
        }
        serializer = CSVUploadSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_csv_upload_serializer_invalid_data(self):
        data = {}
        serializer = CSVUploadSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('file', serializer.errors)

    def test_csv_upload_serializer_empty_file(self):
        csv_file = SimpleUploadedFile("test.csv", b"")
        data = {
            'file': csv_file
        }
        serializer = CSVUploadSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('file', serializer.errors)
