from rest_framework import serializers

from .models import Book, IngestionLog, Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    reserved = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_reserved(self, obj):
        reserved = obj.reservations.filter(status='reserved').first()
        if reserved:
            return True
        return False


class IngestionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngestionLog
        fields = '__all__'


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for handling CSV file uploads."""
    file = serializers.FileField()
