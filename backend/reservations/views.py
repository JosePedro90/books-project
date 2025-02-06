from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Reservation
from .serializers import ReservationSerializer


class IsAdminUser(permissions.BasePermission):
    """Custom permission to allow only admin users to view reservations."""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API to manage book reservations. Only admins can view reservations and update statuses.
    External users can create reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in [
            'list', 'retrieve', 'partial_update', 'update', 'destroy'
        ]:  # Restrict GET and PATCH/PUT to admins
            return [IsAdminUser()]
        return [permissions.AllowAny()]  # Allow external users to create reservations

    def get_queryset(self):
        # Extra security: Even if permission fails, non-admins will see no data
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Book reserved successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Allow admins to update the status of a reservation."""
        reservation = self.get_object()
        new_status = request.data.get('status')

        # Validate status against STATUS_CHOICES
        if new_status not in dict(Reservation.STATUS_CHOICES).keys():
            return Response({
                "error": "Invalid status provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation.status = new_status
        if new_status == 'returned':
            reservation.returned_at = timezone.now()
        elif new_status == 'reserved':
            reservation.returned_at = None  # Clear returned date if reactivating
        reservation.save()

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Ensure PUT requests also validate status."""
        return self.partial_update(request, *args, **kwargs)
