from django.db import models

from books.utils import normalize_name


class Author(models.Model):
    """Model for storing authors with a normalized name."""
    name = models.CharField(max_length=255, unique=True)  # Original name
    normalized_name = models.CharField(max_length=255, unique=True, editable=False)  # Normalized name

    def save(self, *args, **kwargs):
        """Ensure the name is stored in a normalized format before saving."""
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model for storing books with all fields from the CSV."""
    goodreads_book_id = models.IntegerField(null=True, blank=True)
    best_book_id = models.IntegerField(
        null=True,
        blank=True,
    )
    work_id = models.IntegerField(
        null=True,
        blank=True,
    )
    books_count = models.IntegerField(default=1)

    isbn = models.CharField(max_length=10, null=True, blank=True, unique=True, db_index=True)
    isbn13 = models.CharField(max_length=13, null=True, blank=True, unique=True, db_index=True)

    authors = models.ManyToManyField("Author", related_name="books")

    original_publication_year = models.IntegerField(null=True, blank=True, db_index=True)
    original_title = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)

    language_code = models.CharField(max_length=10, null=True, blank=True)

    average_rating = models.FloatField(null=True, blank=True, db_index=True)
    ratings_count = models.IntegerField(null=True, blank=True, db_index=True)
    work_ratings_count = models.IntegerField(null=True, blank=True)
    work_text_reviews_count = models.IntegerField(null=True, blank=True)

    ratings_1 = models.IntegerField(null=True, blank=True)
    ratings_2 = models.IntegerField(null=True, blank=True)
    ratings_3 = models.IntegerField(null=True, blank=True)
    ratings_4 = models.IntegerField(null=True, blank=True)
    ratings_5 = models.IntegerField(null=True, blank=True)

    image_url = models.URLField(null=True, blank=True)
    small_image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class IngestionLog(models.Model):
    filename = models.CharField(max_length=255)
    records_processed = models.IntegerField()
    errors = models.TextField(null=True, blank=True)
    ingested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.records_processed} records"
