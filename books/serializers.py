from rest_framework import serializers

from .models import Book, IngestionLog


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        #todo: ajust fields after model is created
        fields = '__all__'


class IngestionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngestionLog
        fields = '__all__'


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for handling CSV file uploads."""
    file = serializers.FileField()
