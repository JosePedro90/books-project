from books.models import Author, Book
from django.test import TestCase
from django.utils import timezone
from reservations.enums import ReservationStatus
from reservations.models import Reservation


class ReservationModelTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", isbn13="9780321765723")
        self.book.authors.set([self.author])

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            name="Test User",
            email="test@example.com",
            book=self.book,
        )

        self.assertEqual(reservation.name, "Test User")
        self.assertEqual(reservation.email, "test@example.com")
        self.assertEqual(reservation.book, self.book)
        self.assertEqual(reservation.status, ReservationStatus.RESERVED.value)
        self.assertIsNotNone(reservation.reserved_at)
        self.assertIsNotNone(reservation.updated_at)

    def test_reservation_status_choices(self):
        choices = Reservation.STATUS_CHOICES
        expected_choices = [(status.value, status.name.capitalize()) for status in ReservationStatus]
        self.assertEqual(choices, expected_choices)

    def test_reservation_str_representation(self):
        reservation = Reservation.objects.create(
            name="Test User",
            email="test@example.com",
            book=self.book,
        )
        self.assertEqual(str(reservation), "Test User - Test Book (reserved)")

    def test_reservation_returned(self):
        reservation = Reservation.objects.create(
            name="Test User",
            email="test@example.com",
            book=self.book,
        )

        now = timezone.now()
        reservation.returned_at = now
        reservation.status = ReservationStatus.RETURNED.value
        reservation.save()

        self.assertEqual(reservation.returned_at, now)
        self.assertEqual(reservation.status, ReservationStatus.RETURNED.value)

    def test_reservation_updated_at_on_save(self):
        reservation = Reservation.objects.create(
            name="Test User",
            email="test@example.com",
            book=self.book,
        )
        initial_updated_at = reservation.updated_at
        reservation.status = ReservationStatus.CANCELED.value
        reservation.save()
        self.assertNotEqual(reservation.updated_at, initial_updated_at)
