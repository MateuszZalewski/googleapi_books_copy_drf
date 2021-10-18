from rest_framework import viewsets, filters, status
import django_filters.rest_framework
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        print (data, many)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
        )

    def get_queryset(self):
        return Book.objects.all()
