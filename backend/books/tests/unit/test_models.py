from books.models import Author, Book, IngestionLog
from django.db import DataError, IntegrityError
from django.test import TestCase


class AuthorModelTests(TestCase):

    def test_author_creation(self):
        author = Author.objects.create(name="John Doe")
        self.assertEqual(author.name, "John Doe")
        self.assertEqual(author.normalized_name, "john doe")

    def test_author_str_representation(self):
        author = Author.objects.create(name="Jane Smith")
        self.assertEqual(str(author), "Jane Smith")

    def test_author_unique_constraint(self):
        Author.objects.create(name="John Doe")
        with self.assertRaises(IntegrityError):
            Author.objects.create(name="John Doe")

    def test_author_normalization_on_save(self):
        author = Author(name="  José  Pérez  ")
        author.save()
        self.assertEqual(author.normalized_name, "jose perez")

    def test_author_name_max_length(self):
        long_name = "A" * 300
        with self.assertRaises(DataError):
            Author.objects.create(name=long_name)


class BookModelTests(TestCase):

    def test_book_creation(self):
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(
            title="Test Book",
            isbn="439023481",
            isbn13="9780439023481",
            goodreads_book_id=123,
            best_book_id=456,
            work_id=789,
            books_count=2,
            original_publication_year=2000,
            original_title="Original Title",
            language_code="en",
            average_rating=4.5,
            ratings_count=1000,
            work_ratings_count=500,
            work_text_reviews_count=200,
            ratings_1=100,
            ratings_2=150,
            ratings_3=250,
            ratings_4=200,
            ratings_5=300,
            image_url="http://example.com/image.jpg",
            small_image_url="http://example.com/small_image.jpg",
        )
        book.authors.add(author)

        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.isbn, "439023481")
        self.assertEqual(book.isbn13, "9780439023481")
        self.assertEqual(book.authors.count(), 1)
        self.assertEqual(book.authors.first(), author)
        self.assertEqual(book.goodreads_book_id, 123)
        self.assertEqual(book.best_book_id, 456)
        self.assertEqual(book.work_id, 789)
        self.assertEqual(book.books_count, 2)
        self.assertEqual(book.original_publication_year, 2000)
        self.assertEqual(book.original_title, "Original Title")
        self.assertEqual(book.language_code, "en")
        self.assertEqual(book.average_rating, 4.5)
        self.assertEqual(book.ratings_count, 1000)
        self.assertEqual(book.work_ratings_count, 500)
        self.assertEqual(book.work_text_reviews_count, 200)
        self.assertEqual(book.ratings_1, 100)
        self.assertEqual(book.ratings_2, 150)
        self.assertEqual(book.ratings_3, 250)
        self.assertEqual(book.ratings_4, 200)
        self.assertEqual(book.ratings_5, 300)
        self.assertEqual(book.image_url, "http://example.com/image.jpg")
        self.assertEqual(book.small_image_url, "http://example.com/small_image.jpg")

    def test_book_str_representation(self):
        book = Book.objects.create(title="Test Book")
        self.assertEqual(str(book), "Test Book")

    def test_book_isbn_unique_constraint(self):
        Book.objects.create(isbn="439023481", title="Book1")
        with self.assertRaises(IntegrityError):
            Book.objects.create(isbn="439023481", title="Book2")

    def test_book_isbn13_unique_constraint(self):
        Book.objects.create(isbn13="9780439023481", title="Book1")
        with self.assertRaises(IntegrityError):
            Book.objects.create(isbn13="9780439023481", title="Book2")

    def test_book_title_max_length(self):
        long_title = "A" * 300
        with self.assertRaises(DataError):
            Book.objects.create(title=long_title)

    def test_book_isbn_max_length(self):
        long_isbn = "12345678901"
        with self.assertRaises(DataError):
            Book.objects.create(title="Test Book", isbn=long_isbn)

    def test_book_isbn13_max_length(self):
        long_isbn13 = "12345678901234"
        with self.assertRaises(DataError):
            Book.objects.create(title="Test Book", isbn13=long_isbn13)

    def test_book_books_count_default(self):
        book = Book.objects.create(title="Test Book")
        self.assertEqual(book.books_count, 1)


class IngestionLogModelTests(TestCase):

    def test_ingestion_log_creation(self):
        log = IngestionLog.objects.create(filename="test.csv", records_processed=10)
        self.assertEqual(log.filename, "test.csv")
        self.assertEqual(log.records_processed, 10)

    def test_ingestion_log_errors_can_be_null(self):
        log = IngestionLog.objects.create(filename="test.csv", records_processed=10, errors=None)
        self.assertIsNone(log.errors)

    def test_ingestion_log_errors_content(self):
        errors_list = ["Error 1 occurred.", "Error 2 happened.", "Another error."]
        errors_string = "; ".join(errors_list)
        log = IngestionLog.objects.create(filename="test.csv", records_processed=5, errors=errors_string)
        self.assertEqual(log.errors, errors_string)
