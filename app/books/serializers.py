from collections import OrderedDict
from rest_framework import serializers
from .models import Book, SearchInfo
from .models.access_info import AccessInfo, Epub, Pdf, DownloadAccess
from .models.volume_info import VolumeInfo, Author, Category, IndustryIdentifier, Dimensions, \
    ReadingModes, PanelizationSummary, ImageLinks
from .models.sale_info import SaleInfo, ListPrice, RetailPrice, Offer


class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        # filter out null values with list comprehension
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class OfferSerializer(NonNullModelSerializer):
    class Meta:
        model = Offer
        exclude = ('saleInfo', 'id', 'listPrice', 'retailPrice')


class RetailPriceSerializer(NonNullModelSerializer):
    class Meta:
        model = ListPrice
        exclude = ('saleInfo', 'id')


class ListPriceSerializer(NonNullModelSerializer):
    class Meta:
        model = ListPrice
        exclude = ('saleInfo', 'id')


class SaleInfoSerializer(NonNullModelSerializer):
    listPrice = ListPriceSerializer(required=False)
    retailPrice = RetailPriceSerializer(required=False)
    offer = OfferSerializer(required=False)

    class Meta:
        model = SaleInfo
        exclude = ('book', 'id')

    def create(self, validated_data):
        list_price_data = validated_data.pop('listPrice', None)
        retail_price_data = validated_data.pop('retailPrice', None)
        offer_data = validated_data.pop('offer', None)
        book = validated_data.pop('book', None)

        sale_info = SaleInfo.objects.create(book=book, **validated_data)
        if list_price_data:
            ListPrice.objects.create(saleInfo=sale_info, **list_price_data)
        if retail_price_data:
            RetailPrice.objects.create(saleInfo=sale_info, **retail_price_data)
        if offer_data:
            Offer.objects.create(saleInfo=sale_info, **offer_data)

        return sale_info

    def update(self, instance, validated_data):
        retail_price_data = validated_data.pop('retailPrice', {})
        if retail_price_data:
            retail_price_serializer = self.fields['retailPrice']
            retail_price_instance = instance.retailPrice
            retail_price_serializer.update(retail_price_instance, retail_price_data)

        list_price_data = validated_data.pop('listPrice', {})
        if list_price_data:
            list_price_serializer = self.fields['listPrice']
            list_price_instance = instance.listPrice
            list_price_serializer.update(list_price_instance, list_price_data)

        offer_data = validated_data.pop('offer', {})
        if offer_data:
            offer_serializer = self.fields['offer']
            offer_instance = instance.offer
            offer_serializer.update(offer_instance, offer_data)

        return super().update(instance, validated_data)


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
    categories = serializers.ListSerializer(child=serializers.CharField(max_length=100), required=False)
    authors = serializers.ListSerializer(child=serializers.CharField(max_length=100), required=False)
    industryIdentifier = IndustryIdentifierSerializer(required=False)
    dimensions = DimensionsSerializer(required=False)
    readingModes = ReadingModesSerializer(required=False)
    panelizationSummary = PanelizationSummarySerializer(required=False)
    imageLinks = ImageLinksSummarySerializer(required=False)

    class Meta:
        model = VolumeInfo
        exclude = ('book', 'id')

    def update(self, instance, validated_data):

        industry_identifier_data = validated_data.pop('industryIdentifier', {})
        if industry_identifier_data:
            industry_identifier_serializer = self.fields['industryIdentifier']
            industry_identifier_instance = instance.industryIdentifier
            industry_identifier_serializer.update(industry_identifier_instance, industry_identifier_data)

        dimensions_data = validated_data.pop('dimensions', {})
        if dimensions_data:
            dimensions_serializer = self.fields['dimensions']
            dimensions_instance = instance.dimensions
            dimensions_serializer.update(dimensions_instance, dimensions_data)

        reading_modes_data = validated_data.pop('readingModes', {})
        if reading_modes_data:
            reading_modes_serializer = self.fields['readingModes']
            reading_modes_instance = instance.readingModes
            reading_modes_serializer.update(reading_modes_instance, reading_modes_data)

        panelization_summary_data = validated_data.pop('panelizationSummary', {})
        if panelization_summary_data:
            panelization_summary_serializer = self.fields['panelizationSummary']
            panelization_summary_instance = instance.panelizationSummary
            panelization_summary_serializer.update(panelization_summary_instance, panelization_summary_data)

        image_links_data = validated_data.pop('imageLinks', {})
        if image_links_data:
            image_links_serializer = self.fields['imageLinks']
            image_links_instance = instance.imageLinks
            image_links_serializer.update(image_links_instance, image_links_data)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', None)
        authors_data = validated_data.pop('authors', None)
        industry_identifiers_data = validated_data.pop('industryIdentifiers', None)
        dimensions_data = validated_data.pop('dimensions', None)
        reading_modes_data = validated_data.pop('readingModes', None)
        panelization_summary_data = validated_data.pop('panelizationSummary', None)
        image_links_data = validated_data.pop('imageLinks', None)
        book = validated_data.pop('book', None)

        volume_info = VolumeInfo.objects.create(book=book, **validated_data)

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

        return volume_info


class DownloadAccessSerializer(NonNullModelSerializer):
    class Meta:
        model = DownloadAccess
        exclude = ('accessInfo', 'id')


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

    def update(self, instance, validated_data):
        pdf_data = validated_data.pop('pdf', {})
        if pdf_data:
            pdf_serializer = self.fields['pdf']
            pdf_instance = instance.pdf
            pdf_serializer.update(pdf_instance, pdf_data)

        epub_data = validated_data.pop('epub', {})
        if epub_data:
            epub_serializer = self.fields['epub']
            epub_instance = instance.epub
            epub_serializer.update(epub_instance, pdf_data)

        download_access_data = validated_data.pop('downloadAccess', {})
        if download_access_data:
            download_access_serializer = self.fields['downloadAccess']
            download_access_instance = instance.downloadAccess
            download_access_serializer.update(download_access_instance, pdf_data)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        pdf_data = validated_data.pop('pdf', None)
        epub_data = validated_data.pop('epub', None)
        download_access_data = validated_data.pop('downloadAccess', None)
        book = validated_data.pop('book', None)

        access_info = AccessInfo.objects.create(book=book, **validated_data)

        if pdf_data:
            Pdf.objects.create(accessInfo=access_info, **pdf_data)
        if epub_data:
            Epub.objects.create(accessInfo=access_info, **epub_data)
        if download_access_data:
            DownloadAccess.objects.create(accessInfo=access_info, **download_access_data)

        return access_info


class SearchInfoSerializer(NonNullModelSerializer):
    class Meta:
        model = SearchInfo
        exclude = ('book', 'id')


class BookSerializer(NonNullModelSerializer):
    searchInfo = SearchInfoSerializer(required=False)
    accessInfo = AccessInfoSerializer(required=False)
    volumeInfo = VolumeInfoSerializer(required=False)
    saleInfo = SaleInfoSerializer(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def update(self, instance, validated_data):
        search_info_data = validated_data.pop('searchInfo', {})
        if search_info_data:
            # search_info_serializer = self.fields['searchInfo']
            search_info_serializer = SearchInfoSerializer()
            search_info_instance = instance.searchInfo
            search_info_serializer.update(search_info_instance, search_info_data)

        volume_info_data = validated_data.pop('volumeInfo', {})
        if volume_info_data:
            volume_info_serializer = self.fields['volumeInfo']
            volume_info_instance = instance.volumeInfo
            volume_info_serializer.update(volume_info_instance, volume_info_data)

        access_info_data = validated_data.pop('accessInfo', {})
        if access_info_data:
            access_info_serializer = self.fields['accessInfo']
            access_info_instance = instance.accessInfo
            access_info_serializer.update(access_info_instance, access_info_data)

        sale_info_data = validated_data.pop('saleInfo', {})
        if sale_info_data:
            sale_info_serializer = self.fields['saleInfo']
            sale_info_instance = instance.saleInfo
            sale_info_serializer.update(sale_info_instance, sale_info_data)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        search_info_data = validated_data.pop('searchInfo', None)
        volume_info_data = validated_data.pop('volumeInfo', None)
        access_info_data = validated_data.pop('accessInfo', None)
        sale_info_data = validated_data.pop('saleInfo', None)

        book = Book.objects.create(**validated_data)

        if search_info_data:
            search_info_serializer = self.fields['searchInfo']
            search_info_data['book'] = book
            search_info_serializer.create(search_info_data)

        if access_info_data:
            access_info_serializer = self.fields['accessInfo']
            access_info_data['book'] = book
            access_info_serializer.create(access_info_data)

        if volume_info_data:
            volume_info_serializer = self.fields['volumeInfo']
            volume_info_data['book'] = book
            volume_info_serializer.create(volume_info_data)

        if sale_info_data:
            sale_info_serializer = self.fields['saleInfo']
            sale_info_data['book'] = book
            sale_info_serializer.create(sale_info_data)

        return book
