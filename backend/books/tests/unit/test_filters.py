from books.filters import BookFilter
from books.models import Book
from django.test import TestCase
from reservations.models import Reservation


class BookFilterTests(TestCase):

    def test_filter_books_that_are_reserved(self):
        reserved_book = Book.objects.create(title="Reserved Book")
        Reservation.objects.create(book=reserved_book, status="reserved")

        queryset = Book.objects.all()
        filtered_queryset = BookFilter({
            'reserved': True
        }, queryset=queryset).qs

        self.assertIn(reserved_book, filtered_queryset)

    def test_filter_books_that_are_not_reserved(self):
        reserved_book = Book.objects.create(title="Reserved Book")
        Reservation.objects.create(book=reserved_book, status="reserved")
        non_reserved_book = Book.objects.create(title="Non-Reserved Book")

        queryset = Book.objects.all()
        filtered_queryset = BookFilter({
            'reserved': False
        }, queryset=queryset).qs

        self.assertIn(non_reserved_book, filtered_queryset)
        self.assertNotIn(reserved_book, filtered_queryset)

    def test_filter_books_with_no_reservations(self):
        book = Book.objects.create(title="Book with No Reservations")

        queryset = Book.objects.all()
        filtered_queryset = BookFilter({
            'reserved': True
        }, queryset=queryset).qs

        self.assertNotIn(book, filtered_queryset)
