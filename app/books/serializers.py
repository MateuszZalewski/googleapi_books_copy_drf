from collections import OrderedDict
from rest_framework import serializers
from .models import Book, Author, Category


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        # filter out null values with list comprehension
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class BookSerializer(NonNullModelSerializer):
    categories = serializers.ListSerializer(child=serializers.CharField(max_length=100), required=False)
    authors = serializers.ListSerializer(child=serializers.CharField(max_length=100), required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def to_internal_value(self, data):
        internal_data = {'id': data.pop('id')}
        if 'volumeInfo' in data:
            volume_info_data = data.pop('volumeInfo')
            if 'categories' in volume_info_data:
                internal_data['categories'] = volume_info_data.pop('categories')
            if 'authors' in volume_info_data:
                internal_data['authors'] = volume_info_data.pop('authors')
            if 'title' in volume_info_data:
                internal_data['title'] = volume_info_data.pop('title')
            if 'publishedDate' in volume_info_data:
                internal_data['published_date'] = volume_info_data.pop('publishedDate')
            if 'averageRating' in volume_info_data:
                internal_data['average_rating'] = volume_info_data.pop('averageRating')
            if 'ratingsCount' in volume_info_data:
                internal_data['ratings_count'] = volume_info_data.pop('ratingsCount')
            if 'imageLinks' in volume_info_data:
                image_links_data = volume_info_data.pop('imageLinks')
                if 'thumbnail' in image_links_data:
                    internal_data['thumbnail'] = image_links_data.pop('thumbnail')
        return internal_data

    def create(self, validated_data):

        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories')
        else:
            categories_data = None
        if 'authors' in validated_data:
            authors_data = validated_data.pop('authors')
        else:
            authors_data = None

        book = Book.objects.create(**validated_data)

        if categories_data:
            for category_data in categories_data:
                category = Category.objects.create(name=category_data)
                book.categories.add(category)
        if authors_data:
            for author_data in authors_data:
                author = Author.objects.create(fullName=author_data)
                book.authors.add(author)
        book.save()

        return book
