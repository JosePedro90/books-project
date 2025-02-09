from books.models import Book
from django.db import models
from django.utils import timezone

from reservations.enums import ReservationStatus


class Reservation(models.Model):
    """Model to manage book reservations."""
    STATUS_CHOICES = [(status.value, status.name.capitalize()) for status in ReservationStatus]

    name = models.CharField(max_length=255)  # External user name
    email = models.EmailField(db_index=True)  # External user email

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved', db_index=True)
    reserved_at = models.DateTimeField(default=timezone.now, db_index=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.book.title} ({self.status})"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
