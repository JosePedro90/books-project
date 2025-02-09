from django.db.models import Exists, OuterRef
from django_filters import rest_framework as filters
from reservations.models import Reservation

from .models import Book


class BookFilter(filters.FilterSet):
    reserved = filters.BooleanFilter(method='filter_reserved')

    class Meta:
        model = Book
        fields = []

    def filter_reserved(self, queryset, name, value):
        reservations = Reservation.objects.filter(
            book=OuterRef('pk'),
            status='reserved',
        )

        if value:
            return queryset.annotate(is_reserved=Exists(reservations)).filter(is_reserved=True)
        else:
            return queryset.annotate(is_reserved=Exists(reservations)).filter(is_reserved=False)
