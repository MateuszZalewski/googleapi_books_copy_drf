from collections import OrderedDict

from rest_framework import viewsets, status
from rest_framework import filters as drf_filters
from rest_framework.response import Response

from django_filters import rest_framework as df_filters
from django.forms import MultipleChoiceField

from .models import Book
from .serializers import BookSerializer


class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(df_filters.MultipleChoiceFilter):
    field_class = MultipleField


class BookFilter(df_filters.FilterSet):
    published_date = df_filters.CharFilter(field_name="volumeInfo__publishedDate", lookup_expr='startswith')
    author = MultipleFilter(field_name='volumeInfo__authors__fullName', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ('published_date', 'author')


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = (drf_filters.OrderingFilter, df_filters.DjangoFilterBackend)
    ordering_fields = ('volumeInfo__publishedDate',)
    filterset_class = BookFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BookSerializer(queryset, many=True)
        return Response(OrderedDict([
            ('kind', 'books#volumes'),
            ('totalItems', queryset.count()),
            ('items', serializer.data)
        ]))

    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        print(data, many)
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
