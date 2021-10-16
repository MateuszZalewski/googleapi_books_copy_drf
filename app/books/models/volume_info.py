from django.db import models
from .book import Book


class Author(models.Model):
    fullName = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)


class VolumeInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    authors = models.ManyToManyField(Author)  #
    publisher = models.CharField(max_length=100)
    publishedDate = models.DateField()
    description = models.TextField()
    pageCount = models.IntegerField()
    printType = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)  #
    averageRating = models.FloatField()
    ratingsCount = models.IntegerField()
    contentVersion = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    mainCategory = models.CharField(max_length=100)
    previewLink = models.URLField()
    maturityRating = models.CharField(max_length=100)
    allowAnonLogging = models.BooleanField()
    infoLink = models.URLField()
    canonicalVolumeLink = models.URLField()


class IndustryIdentifier(models.Model):
    volumeInfo = models.ForeignKey(VolumeInfo, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)


class Dimensions(models.Model):
    volumeInfo = models.ForeignKey(VolumeInfo, on_delete=models.CASCADE)
    height = models.CharField(max_length=100)
    width = models.CharField(max_length=100)
    thickness = models.CharField(max_length=100)


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
    thumbnail = models.URLField()
    small = models.URLField()
    medium = models.URLField()
    large = models.URLField()
    smallThumbnail = models.URLField()
    extraLarge = models.URLField()
