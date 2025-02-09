from rest_framework import serializers

from .models import Author, Book, IngestionLog, normalize_name


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    authors_input = serializers.CharField(write_only=True)
    reserved = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_reserved(self, obj):
        reserved = obj.reservations.filter(status='reserved').first()
        if reserved:
            return True
        return False

    def create(self, validated_data):
        authors_input = validated_data.pop('authors_input', '')
        book = super().create(validated_data)
        self._update_authors(book, authors_input)
        return book

    def update(self, instance, validated_data):
        authors_input = validated_data.pop('authors_input', None)
        if authors_input is not None:
            self._update_authors(instance, authors_input)
        return super().update(instance, validated_data)

    def _update_authors(self, book, authors_input):
        # Split the comma-separated string into author names
        author_names = [name.strip() for name in authors_input.split(',') if name.strip()]

        # Fetch or create authors using normalized names
        authors = []
        for name in author_names:
            normalized_name = normalize_name(name)
            author, _ = Author.objects.get_or_create(normalized_name=normalized_name, defaults={
                'name': name
            })
            authors.append(author)

        book.authors.set(authors)


class IngestionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngestionLog
        fields = '__all__'


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for handling CSV file uploads."""
    file = serializers.FileField()
