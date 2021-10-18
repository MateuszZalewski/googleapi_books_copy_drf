from rest_framework import viewsets, filters
import django_filters.rest_framework

from .models import Book
from .serializers import BookSerializer


class BookFilter(django_filters.rest_framework.FilterSet):
    published_date = django_filters.rest_framework.CharFilter(field_name="volumeInfo__publishedDate", lookup_expr='startswith')

    class Meta:
        model = Book
        fields = ('published_date', )


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ('volumeInfo__publishedDate',)
    filterset_class = BookFilter

    def get_queryset(self):
        return Book.objects.all()
