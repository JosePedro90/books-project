from unittest.mock import patch

from books.models import Author, Book, IngestionLog
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATE=True)
class CSVUploadViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_test_user()
        self.client.force_authenticate(user=self.user)

    def create_test_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(username='testuser', password='testpassword', email="test@test.com")

    @patch("books.tasks.process_csv")
    def test_csv_upload_successful(self, mock_send_email, mock_process_csv):
        csv_file = SimpleUploadedFile("test.csv", b"title,authors\nTest Book,Test Author")
        url = reverse("upload_csv")  # Correct URL name

        response = self.client.post(url, {
            "file": csv_file
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["message"], "CSV ingestion started. You will receive an email upon completion.")

        mock_process_csv.delay.assert_called_once_with(
            b"title,authors\nTest Book,Test Author", self.user.email, csv_file.name
        )

    @patch("books.tasks.send_ingestion_report")
    def test_csv_upload_with_errors(self, mock_send_email):
        csv_file = SimpleUploadedFile(
            "test.csv", b"title,authors,isbn13\nTest Book,Test Author,invalid_isbn-looooooong"
        )
        url = reverse("upload_csv")  # Correct URL name

        response = self.client.post(url, {
            "file": csv_file
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(IngestionLog.objects.count(), 1)
        log = IngestionLog.objects.first()
        self.assertIn("Error processing book 'Test Book': value too long for type character varying(13)", log.errors)

        mock_send_email.assert_called_once()

    def test_csv_upload_no_file(self):
        url = reverse("upload_csv")  # Correct URL name
        response = self.client.post(url, {}, format="multipart")  # No file

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No file provided.")

    @patch("books.tasks.send_ingestion_report")
    def test_csv_upload_existing_book(self, mock_send_email):
        author = Author.objects.create(name="Test Author", normalized_name="test author")
        book = Book.objects.create(title="Test Book", isbn13="9780321765723")
        book.authors.set([author])

        csv_file = SimpleUploadedFile("test.csv", b"title,authors,isbn13\nTest Book,Test Author,9780321765723")
        url = reverse("upload_csv")  # Correct URL name

        response = self.client.post(url, {
            "file": csv_file
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Book.objects.count(), 1)
        mock_send_email.assert_called_once()
