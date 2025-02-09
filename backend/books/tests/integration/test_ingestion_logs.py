from books.models import IngestionLog
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class IngestionLogViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_test_user()
        self.client.force_authenticate(user=self.user)
        IngestionLog.objects.create(filename="test.csv", records_processed=10)

    def create_test_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(username='testuser', password='testpassword')

    def test_ingestion_log_list(self):
        url = reverse("ingestionlog-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_ingestion_log_retrieve(self):
        log = IngestionLog.objects.first()
        url = reverse("ingestionlog-detail", kwargs={
            "pk": log.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["filename"], "test.csv")
