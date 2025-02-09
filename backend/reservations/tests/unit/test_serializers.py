from books.models import Author, Book
from django.test import TransactionTestCase
from reservations.enums import ReservationStatus
from reservations.models import Reservation
from reservations.serializers import ReservationSerializer


class ReservationSerializerTests(TransactionTestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", isbn13="9780321765723")
        self.book.authors.set([self.author])

    def test_reservation_create_successful(self):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "book": self.book.pk,
        }
        serializer = ReservationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        reservation = serializer.save()

        self.assertEqual(reservation.name, "Test User")
        self.assertEqual(reservation.book, self.book)
        self.assertEqual(reservation.status, ReservationStatus.RESERVED.value)

    def test_reservation_update_successful(self):
        reservation = Reservation.objects.create(name="Test User", email="test@example.com", book=self.book)
        data = {
            "status": ReservationStatus.RETURNED.value,
        }
        serializer = ReservationSerializer(
            instance=reservation, data=data, partial=True
        )  # partial=True for partial updates
        self.assertTrue(serializer.is_valid())
        updated_reservation = serializer.save()

        self.assertEqual(updated_reservation.status, ReservationStatus.RETURNED.value)

    def test_reservation_update_other_fields(self):
        reservation = Reservation.objects.create(name="Test User", email="test@example.com", book=self.book)
        data = {
            "name": "Updated User",
            "email": "updated@example.com",
        }
        serializer = ReservationSerializer(instance=reservation, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_reservation = serializer.save()

        self.assertEqual(updated_reservation.name, "Updated User")
        self.assertEqual(updated_reservation.email, "updated@example.com")

    def test_reservation_create_invalid_book_pk(self):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "book": 999,
        }
        serializer = ReservationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid pk", str(serializer.errors["book"][0]))  # Check for the correct error message

    def test_reservation_update_invalid_book_pk(self):
        reservation = Reservation.objects.create(name="Test User", email="test@example.com", book=self.book)
        data = {
            "book": 999,
            "status": ReservationStatus.RESERVED.value,
        }
        serializer = ReservationSerializer(instance=reservation, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid pk", str(serializer.errors["book"][0]))  # Check for the correct error message

    def test_reservation_create_invalid_status(self):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "book": self.book.pk,
            "status": "invalid_status"
        }
        serializer = ReservationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("is not a valid choice", str(serializer.errors["status"][0]))

    def test_reservation_update_invalid_status(self):
        reservation = Reservation.objects.create(name="Test User", email="test@example.com", book=self.book)
        data = {
            "status": "invalid_status"
        }
        serializer = ReservationSerializer(instance=reservation, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("is not a valid choice", str(serializer.errors["status"][0]))
