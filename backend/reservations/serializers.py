from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'book', 'status', 'reserved_at', 'returned_at']
        read_only_fields = ['reserved_at', 'returned_at', 'status']

    def validate(self, data):
        book = data['book']

        # Prevent multiple users from reserving the same book at the same time
        if Reservation.objects.filter(book=book, status='reserved').exists():
            raise serializers.ValidationError("This book is already reserved by another user.")

        return data


class CurrentReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['status']
