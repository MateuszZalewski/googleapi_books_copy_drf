from django.db import models
from .book import Book


class Author(models.Model):
    fullName = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.fullName}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Categories'


class VolumeInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='volumeInfo')
    title = models.CharField(max_length=100, null=True)
    subtitle = models.TextField(null=True)
    authors = models.ManyToManyField(Author, related_name='authors')
    publisher = models.CharField(max_length=100, null=True)
    publishedDate = models.DateField()
    description = models.TextField(null=True)
    pageCount = models.IntegerField()
    printType = models.CharField(max_length=100, null=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    averageRating = models.FloatField()
    ratingsCount = models.IntegerField()
    contentVersion = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=100, null=True)
    mainCategory = models.CharField(max_length=100, null=True)
    previewLink = models.URLField(null=True)
    maturityRating = models.CharField(max_length=100, null=True)
    allowAnonLogging = models.BooleanField(null=True)
    infoLink = models.URLField(null=True)
    canonicalVolumeLink = models.URLField(null=True)


class IndustryIdentifier(models.Model):
    volumeInfo = models.OneToOneField(VolumeInfo, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, null=True)
    identifier = models.CharField(max_length=100, null=True)


class Dimensions(models.Model):
    volumeInfo = models.OneToOneField(VolumeInfo, on_delete=models.CASCADE)
    height = models.CharField(max_length=100, null=True)
    width = models.CharField(max_length=100, null=True)
    thickness = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'Dimensions'


class ReadingModes(models.Model):
    volumeInfo = models.OneToOneField(VolumeInfo, on_delete=models.CASCADE)
    text = models.BooleanField()
    image = models.BooleanField()


class PanelizationSummary(models.Model):
    volumeInfo = models.OneToOneField(VolumeInfo, on_delete=models.CASCADE)
    containsEpubBubbles = models.BooleanField()
    containsImageBubbles = models.BooleanField()


class ImageLinks(models.Model):
    volumeInfo = models.OneToOneField(VolumeInfo, on_delete=models.CASCADE)
    thumbnail = models.URLField(null=True)
    small = models.URLField(null=True)
    medium = models.URLField(null=True)
    large = models.URLField(null=True)
    smallThumbnail = models.URLField(null=True)
    extraLarge = models.URLField(null=True)
