from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CSVUploadView, IngestionLogViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'ingestion-logs', IngestionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-csv/', CSVUploadView.as_view(), name='upload_csv'),
]
