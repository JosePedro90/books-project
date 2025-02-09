from books.models import Author, Book
from django.test import TestCase
from reservations.enums import ReservationStatus
from reservations.models import Reservation
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class ReservationViewSetIntegrationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", isbn13="9780321765723")
        self.book.authors.set([self.author])
        self.user = self.create_test_user()
        self.admin_user = self.create_test_admin_user()

    def create_test_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(username='testuser', password='testpassword')

    def create_test_admin_user(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='adminuser', password='adminpassword')
        user.is_staff = True
        user.save()
        return user

    def test_reservation_create_successful(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "book": self.book.pk,
        }
        url = reverse("reservation-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Book reserved successfully!")
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.book, self.book)

    def test_reservation_create_book_already_reserved(self):
        self.client.force_authenticate(user=self.user)
        Reservation.objects.create(
            name="Existing User", email="existing@example.com", book=self.book, status=ReservationStatus.RESERVED.value
        )
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "book": self.book.pk,
        }
        url = reverse("reservation-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This book is already reserved.", response.data[0])

    def test_reservation_list_admin(self):
        self.client.force_authenticate(user=self.admin_user)  # Authenticate as admin
        Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_reservation_list_non_admin(self):
        self.client.force_authenticate(user=self.user)  # Authenticate as non-admin
        url = reverse("reservation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_retrieve_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test")

    def test_reservation_retrieve_non_admin(self):
        self.client.force_authenticate(user=self.user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_update_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        data = {
            "status": ReservationStatus.RETURNED.value
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], ReservationStatus.RETURNED.value)

    def test_reservation_update_non_admin(self):
        self.client.force_authenticate(user=self.user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        data = {
            "status": ReservationStatus.RETURNED.value
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reservation_delete_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_delete_non_admin(self):
        self.client.force_authenticate(user=self.user)
        reservation = Reservation.objects.create(name="Test", email="test@test.com", book=self.book)
        url = reverse("reservation-detail", kwargs={
            "pk": reservation.pk
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
