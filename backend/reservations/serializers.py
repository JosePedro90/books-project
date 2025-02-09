from django.db import transaction
from rest_framework import serializers

from .enums import ReservationStatus
from .models import Book, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=ReservationStatus.choices(), required=False)

    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'book', 'status', 'reserved_at', 'returned_at']
        read_only_fields = ['reserved_at', 'returned_at']

    def create(self, validated_data):
        book = validated_data['book']

        with transaction.atomic():
            locked_book = Book.objects.select_for_update().get(pk=book.pk)

            if Reservation.objects.filter(book=locked_book, status=ReservationStatus.RESERVED.value).exists():
                raise serializers.ValidationError("This book is already reserved.")

            reservation = Reservation.objects.create(**validated_data)
            return reservation

    def update(self, instance, validated_data):
        book = instance.book

        status = validated_data.get('status', instance.status)

        if status == ReservationStatus.RESERVED.value:
            with transaction.atomic():
                locked_book = Book.objects.select_for_update().get(pk=book.pk)

                if Reservation.objects.filter(book=locked_book,
                                              status=ReservationStatus.RESERVED.value).exclude(pk=instance.pk).exists():
                    raise serializers.ValidationError("This book is already reserved by another user.")

                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                return instance
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
