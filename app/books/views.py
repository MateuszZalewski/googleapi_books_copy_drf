from rest_framework import viewsets, filters

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('volumeInfo__publishedDate',)

    def get_queryset(self):
        return Book.objects.all()
