from rest_framework import status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book, IngestionLog
from .serializers import (BookSerializer, IngestionLogSerializer)
from .tasks import process_csv


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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({
                "error": "No file provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        admin_email = request.user.email or "admin@example.com"

        file_data = file.read()
        process_csv.delay(file_data, admin_email, file.name)

        return Response({
            "message": "CSV ingestion started. You will receive an email upon completion."
        },
                        status=status.HTTP_202_ACCEPTED)
