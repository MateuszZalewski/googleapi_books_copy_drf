from collections import OrderedDict
from rest_framework import serializers
from .models import Book, SearchInfo
from .models.access_info import AccessInfo, Epub, Pdf, DownloadAccess
from .models.volume_info import VolumeInfo, Author, Category, IndustryIdentifier, Dimensions, \
    ReadingModes, PanelizationSummary, ImageLinks


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        # filter out null values with list comprehension
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class ImageLinksSummarySerializer(NonNullModelSerializer):
    class Meta:
        model = ImageLinks
        exclude = ('volumeInfo', 'id')


class PanelizationSummarySerializer(NonNullModelSerializer):
    class Meta:
        model = PanelizationSummary
        exclude = ('volumeInfo', 'id')


class ReadingModesSerializer(NonNullModelSerializer):
    class Meta:
        model = ReadingModes
        exclude = ('volumeInfo', 'id')


class DimensionsSerializer(NonNullModelSerializer):
    class Meta:
        model = Dimensions
        exclude = ('volumeInfo', 'id')


class IndustryIdentifierSerializer(NonNullModelSerializer):
    class Meta:
        model = IndustryIdentifier
        exclude = ('volumeInfo', 'id')


class AuthorSerializer(NonNullModelSerializer):
    class Meta:
        model = Author
        fields = ('fullName', )


class CategorySerializer(NonNullModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class VolumeInfoSerializer(NonNullModelSerializer):
    categories = serializers.ListSerializer(child=serializers.CharField(max_length=100))
    authors = serializers.ListSerializer(child=serializers.CharField(max_length=100))
    # categories = CategorySerializer(many=True, required=False)
    # authors = AuthorSerializer(many=True, required=False)
    industryIdentifier = IndustryIdentifierSerializer(required=False)
    dimensions = DimensionsSerializer(required=False)
    readingModes = ReadingModesSerializer(required=False)
    panelizationSummary = PanelizationSummarySerializer(required=False)
    imageLinks = ImageLinksSummarySerializer(required=False)

    class Meta:
        model = VolumeInfo
        exclude = ('book', 'id')


class DownloadAccessSerializer(NonNullModelSerializer):
    class Meta:
        model = DownloadAccess
        exclude = ('accessInfo', )


class PdfSerializer(NonNullModelSerializer):
    class Meta:
        model = Pdf
        exclude = ('accessInfo', 'id')


class EpubSerializer(NonNullModelSerializer):
    class Meta:
        model = Epub
        exclude = ('accessInfo', 'id')


class AccessInfoSerializer(NonNullModelSerializer):
    downloadAccess = DownloadAccessSerializer(required=False)
    pdf = PdfSerializer(required=False)
    epub = EpubSerializer(required=False)

    class Meta:
        model = AccessInfo
        exclude = ('book', 'id')


class SearchInfoSerializer(NonNullModelSerializer):
    class Meta:
        model = SearchInfo
        exclude = ('book', 'id')


class BookSerializer(NonNullModelSerializer):
    searchInfo = SearchInfoSerializer(required=False)
    accessInfo = AccessInfoSerializer(required=False)
    volumeInfo = VolumeInfoSerializer(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        if 'searchInfo' in validated_data:
            search_info_data = validated_data.pop('searchInfo')
        else:
            search_info_data = None

        volume_info_data = categories_data = authors_data = industry_identifiers_data = dimensions_data = None
        reading_modes_data = panelization_summary_data = image_links_data = None

        if 'volumeInfo' in validated_data:
            volume_info_data = validated_data.pop('volumeInfo')
            if 'categories' in volume_info_data:
                categories_data = volume_info_data.pop('categories')
            if 'authors' in volume_info_data:
                authors_data = volume_info_data.pop('authors')
            if 'industryIdentifiers' in volume_info_data:
                industry_identifiers_data = volume_info_data.pop('industryIdentifiers')
            if 'dimensions' in volume_info_data:
                dimensions_data = volume_info_data.pop('dimensions')
            if 'readingModes' in volume_info_data:
                reading_modes_data = volume_info_data.pop('readingModes')
            if 'panelizationSummary' in volume_info_data:
                panelization_summary_data = volume_info_data.pop('panelizationSummary')
            if 'imageLinks' in volume_info_data:
                image_links_data = volume_info_data.pop('imageLinks')

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

        if volume_info_data:
            volume_info = VolumeInfo.objects.create(book=book, **volume_info_data)
            if categories_data:
                for category_data in categories_data:
                    category = Category.objects.create(name=category_data)
                    volume_info.categories.add(category)
            if authors_data:
                for author_data in authors_data:
                    author = Author.objects.create(fullName=author_data)
                    volume_info.authors.add(author)
            if industry_identifiers_data:
                for industry_identifier_data in industry_identifiers_data:
                    IndustryIdentifier.objects.create(volumeInfo=volume_info, **industry_identifier_data)
            if dimensions_data:
                Dimensions.objects.create(volumeInfo=volume_info, **dimensions_data)
            if reading_modes_data:
                ReadingModes.objects.create(volumeInfo=volume_info, **reading_modes_data)
            if panelization_summary_data:
                PanelizationSummary.objects.create(volumeInfo=volume_info, **panelization_summary_data)
            if image_links_data:
                ImageLinks.objects.create(volumeInfo=volume_info, **image_links_data)
            volume_info.save()
        if access_info_data:
            access_info = AccessInfo.objects.create(book=book, **access_info_data)
            if pdf_data:
                Pdf.objects.create(accessInfo=access_info, **pdf_data)
            if epub_data:
                Epub.objects.create(accessInfo=access_info, **epub_data)
            if download_access_data:
                DownloadAccess.objects.create(accessInfo=access_info, **download_access_data)
        return book
