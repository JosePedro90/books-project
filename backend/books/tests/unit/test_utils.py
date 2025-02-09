from books.models import Author, Book
from books.utils import book_exists, clean_isbn, normalize_name
from django.test import TestCase


class CleanISBNTests(TestCase):

    def test_clean_isbn_valid_isbn10(self):
        self.assertEqual(clean_isbn("9780321765723"), "9780321765723")

    def test_clean_isbn_valid_isbn13(self):
        self.assertEqual(clean_isbn("9780321765723000"), "9780321765723000")

    def test_clean_isbn_scientific_notation(self):
        self.assertIsNone(clean_isbn("978e10"))
        self.assertIsNone(clean_isbn("978E10"))

    def test_clean_isbn_none(self):
        self.assertIsNone(clean_isbn(None))

    def test_clean_isbn_empty_string(self):
        self.assertIsNone(clean_isbn(""))

    def test_clean_isbn_with_whitespace(self):
        self.assertEqual(clean_isbn("  9780321765723  "), "9780321765723")


class BookExistsTests(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(name="Test Author 1", normalized_name="test author 1")
        self.book1 = Book.objects.create(title="Test Book 1", isbn13="9780000000001")
        self.book1.authors.add(self.author1)

        self.author2 = Author.objects.create(name="Test Author 2", normalized_name="test author 2")
        self.book2 = Book.objects.create(title="Test Book 2", isbn="9780000002")
        self.book2.authors.add(self.author2)

        self.book3 = Book.objects.create(title="Test Book 3")  # Book without ISBNs
        self.book3.authors.add(self.author1)

    def test_book_exists_by_isbn13(self):
        self.assertTrue(book_exists({
            "isbn13": "9780000000001",
            "title": "Test Book 1",
            "authors": "Test Author 1"
        }))
        self.assertTrue(
            book_exists({
                "isbn13": "9780000000001",
                "title": "Some Other Title",
                "authors": "Some Other Author"
            })
        )

    def test_book_exists_by_isbn(self):
        self.assertTrue(book_exists({
            "isbn": "9780000002",
            "title": "Test Book 2",
            "authors": "Test Author 2"
        }))
        self.assertTrue(
            book_exists({
                "isbn": "9780000002",
                "title": "Some Other Title",
                "authors": "Some Other Author"
            })
        )
        self.assertFalse(book_exists({
            "isbn": "9780000001",
            "title": "Test Book 65",
            "authors": "Test Author 23"
        }))

    def test_book_exists_by_title_and_authors(self):
        self.assertTrue(book_exists({
            "title": "Test Book 1",
            "authors": "Test Author 1"
        }))
        self.assertFalse(book_exists({
            "title": "Test Book 1",
            "authors": "Test Author 2"
        }))
        self.assertTrue(book_exists({
            "title": "Test Book 3",
            "authors": "Test Author 1"
        }))

    def test_book_exists_missing_required_fields(self):
        self.assertFalse(book_exists({
            "isbn13": "9780000000001"
        }))  # Missing title and authors
        self.assertFalse(book_exists({
            "title": "Test Book 1"
        }))  # Missing authors
        self.assertFalse(book_exists({
            "authors": "Test Author 1"
        }))  # Missing title

    def test_book_exists_partial_author_match(self):
        self.assertTrue(book_exists({
            "title": "Test Book 1",
            "authors": "Test Author 1, Some Other Author"
        }))

    def test_book_exists_with_extra_fields(self):
        self.assertTrue(book_exists({
            "title": "Test Book 1",
            "authors": "Test Author 1",
            "extra": "field"
        }))

    def test_book_exists_with_whitespace(self):
        self.assertTrue(book_exists({
            "title": "Test Book 1  ",
            "authors": "  Test Author 1  "
        }))

    def test_book_exists_case_insensitive_title(self):
        self.assertTrue(book_exists({
            "title": "test book 1",
            "authors": "Test Author 1"
        }))

    def test_book_exists_case_insensitive_authors(self):
        self.assertTrue(book_exists({
            "title": "Test Book 1",
            "authors": "test author 1"
        }))


class NormalizeNameTests(TestCase):

    def test_normalize_name_with_accents(self):
        self.assertEqual(normalize_name("JöHn Doe"), "john doe")

    def test_normalize_name_with_extra_spaces(self):
        self.assertEqual(normalize_name("  John   Doe  "), "john doe")

    def test_normalize_name_with_period(self):
        self.assertEqual(normalize_name("John.Doe"), "johndoe")

    def test_normalize_name_empty(self):
        self.assertEqual(normalize_name(""), "")

    def test_normalize_name_with_mixed_case(self):
        self.assertEqual(normalize_name("JoHn DoE"), "john doe")

    def test_normalize_name_with_unicode(self):
        self.assertEqual(normalize_name("José Pérez"), "jose perez")
