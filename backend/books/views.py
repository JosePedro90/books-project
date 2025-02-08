from urllib import request

from rest_framework import status, views, viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book, IngestionLog
from .serializers import (BookSerializer, IngestionLogSerializer, CSVUploadSerializer)
from .tasks import process_csv


class BookViewSet(viewsets.ModelViewSet):
    """
    API to CRUD books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'authors__name', 'isbn', 'isbn13']
    ordering_fields = ['title', 'average_rating', 'ratings_count', 'original_publication_year']
    ordering = ['title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow any for list and retrieve
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class IngestionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to list ingestion logs
    """
    queryset = IngestionLog.objects.all()
    serializer_class = IngestionLogSerializer
    permission_classes = [IsAuthenticated]


class CSVUploadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({
                "error": "No file provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        admin_email = request.user.email

        file_data = file.read()
        process_csv.delay(file_data, admin_email, file.name)

        return Response({
            "message": "CSV ingestion started. You will receive an email upon completion."
        },
                        status=status.HTTP_202_ACCEPTED)
