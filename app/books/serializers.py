from collections import OrderedDict
from rest_framework import serializers
from .models import Book, SearchInfo
from .models.access_info import AccessInfo, Epub, Pdf, DownloadAccess


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        # filter out null values with list comprehension
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class DownloadAccessSerializer(NonNullModelSerializer):
    class Meta:
        model = DownloadAccess
        exclude = ('accessInfo', )


class PdfSerializer(NonNullModelSerializer):
    class Meta:
        model = Pdf
        exclude = ('accessInfo', )


class EpubSerializer(NonNullModelSerializer):
    class Meta:
        model = Epub
        exclude = ('accessInfo', )


class AccessInfoSerializer(NonNullModelSerializer):
    downloadAccess = DownloadAccessSerializer(required=False)
    pdf = PdfSerializer(required=False)
    epub = EpubSerializer(required=False)

    class Meta:
        model = AccessInfo
        exclude = ('book', )


class SearchInfoSerializer(NonNullModelSerializer):
    class Meta:
        model = SearchInfo
        exclude = ('book', 'id')


class BookSerializer(NonNullModelSerializer):
    searchInfo = SearchInfoSerializer(required=False)
    accessInfo = AccessInfoSerializer(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        if 'searchInfo' in validated_data:
            search_info_data = validated_data.pop('searchInfo')
        else:
            search_info_data = None

        access_info_data = pdf_data = epub_data = download_access_data = None

        if 'accessInfo' in validated_data:
            access_info_data = validated_data.pop('accessInfo')
            if 'pdf' in access_info_data:
                pdf_data = access_info_data.pop('pdf')
            if 'epub' in access_info_data:
                epub_data = access_info_data.pop('epub')
            if 'downloadAccess' in access_info_data:
                download_access_data = access_info_data.pop('downloadAccess')

        book = Book.objects.create(**validated_data)

        if search_info_data:
            SearchInfo.objects.create(book=book, **search_info_data)
        if access_info_data:
            access_info = AccessInfo.objects.create(book=book, **access_info_data)
            if pdf_data:
                Pdf.objects.create(accessInfo=access_info, **pdf_data)
            if epub_data:
                Epub.objects.create(accessInfo=access_info, **epub_data)
            if download_access_data:
                DownloadAccess.objects.create(accessInfo=access_info, **download_access_data)
        return book
