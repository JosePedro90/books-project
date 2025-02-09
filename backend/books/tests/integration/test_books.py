from books.models import Author, Book
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class BookViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_test_user()
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(name="Test Author", normalized_name="test author")
        self.book = Book.objects.create(title="Test Book", isbn="9780321765")
        self.book.authors.set([self.author])

    def create_test_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(username='testuser', password='testpassword')

    def test_book_list(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_book_retrieve(self):
        url = reverse("book-detail", kwargs={
            "pk": self.book.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_book_create_with_authors_input(self):
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "authors_input": "Author One, Author Two"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        new_book = Book.objects.get(title="New Book")
        self.assertEqual(new_book.authors.count(), 2)
        self.assertTrue(new_book.authors.filter(name="Author One").exists())
        self.assertTrue(new_book.authors.filter(name="Author Two").exists())

    def test_book_update_with_authors_input(self):
        url = reverse("book-detail", kwargs={
            "pk": self.book.pk
        })
        data = {
            "title": "Updated Book",
            "authors_input": "New Author One, New Author Two"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(updated_book.authors.count(), 2)
        self.assertTrue(updated_book.authors.filter(name="New Author One").exists())
        self.assertTrue(updated_book.authors.filter(name="New Author Two").exists())
        self.assertFalse(updated_book.authors.filter(name="Test Author").exists())

    def test_book_delete(self):
        url = reverse("book-detail", kwargs={
            "pk": self.book.pk
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_unauthenticated_user_cannot_create_book(self):
        self.client.force_authenticate(user=None)
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "authors_input": "Author One, Author Two"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_book(self):
        self.client.force_authenticate(user=None)
        url = reverse("book-detail", kwargs={
            "pk": self.book.pk
        })
        data = {
            "title": "Updated Book",
            "authors_input": "New Author One, New Author Two"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_delete_book(self):
        self.client.force_authenticate(user=None)
        url = reverse("book-detail", kwargs={
            "pk": self.book.pk
        })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
