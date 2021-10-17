from rest_framework import serializers
from .models import Book, SearchInfo


class SearchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchInfo
        exclude = ('book', 'id')


class BookSerializer(serializers.ModelSerializer):
    searchInfo = SearchInfoSerializer(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        if 'searchInfo' in validated_data:
            search_info_data = validated_data.pop('searchInfo')
        else:
            search_info_data = None

        book = Book.objects.create(**validated_data)

        if search_info_data:
            SearchInfo.objects.create(book=book, **search_info_data)
        return book
