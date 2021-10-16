from django.db import models
from .book import Book


class AccessInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    viewability = models.CharField(max_length=100)
    accessViewStatus = models.CharField(max_length=100)
    embeddable = models.BooleanField()
    publicDomain = models.BooleanField()
    webReaderLink = models.URLField()
    textToSpeechPermission = models.CharField(max_length=100)
    quoteSharingAllowed = models.BooleanField()


class Epub(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE)
    downloadLink = models.URLField()
    acsTokenLink = models.URLField()
    isAvailable = models.BooleanField()


class Pdf(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE)
    downloadLink = models.URLField()
    acsTokenLink = models.URLField()
    isAvailable = models.BooleanField()


class DownloadAccess(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE)
    kind = models.CharField(max_length=100)
    volumeId = models.CharField(max_length=100)
    restricted = models.BooleanField()
    deviceAllowed = models.BooleanField()
    justAcquired = models.BooleanField()
    maxDownloadDevices = models.IntegerField()
    downloadsAcquired = models.IntegerField()
    nonce = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    reasonCode = models.CharField(max_length=100)
    message = models.TextField()
    signature = models.CharField(max_length=100)



