from django.db import models
from django.utils import timezone
from books.models import Book


class Reservation(models.Model):
    """Model to manage book reservations."""
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('canceled', 'Canceled'),
        ('returned', 'Returned'),
    ]

    name = models.CharField(max_length=255)  # External user name
    email = models.EmailField()  # External user email

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved')
    reserved_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.book.title} ({self.status})"
