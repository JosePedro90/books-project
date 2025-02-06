from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book, IngestionLog
from .serializers import (BookSerializer, CSVUploadSerializer,
                          IngestionLogSerializer)
from .services import process_csv


class BookViewSet(viewsets.ModelViewSet):
    """
    API to CRUD books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class IngestionLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to list ingestion logs
    """
    queryset = IngestionLog.objects.all()
    serializer_class = IngestionLogSerializer
    permission_classes = [IsAuthenticated]


class CSVUploadView(views.APIView):
    """API view for uploading and processing CSV files."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            books_created, errors = process_csv(file)

            response_data = {
                "message": f"CSV file processed successfully. {books_created} books added.",
                "errors": errors if errors else "No errors encountered."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
