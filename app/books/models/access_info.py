from django.db import models
from .book import Book


class AccessInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='accessInfo')
    country = models.CharField(max_length=100, null=True)
    viewability = models.CharField(max_length=100, null=True)
    accessViewStatus = models.CharField(max_length=100, null=True)
    embeddable = models.BooleanField()
    publicDomain = models.BooleanField()
    webReaderLink = models.URLField(null=True)
    textToSpeechPermission = models.CharField(max_length=100, null=True)
    quoteSharingAllowed = models.BooleanField()


class Epub(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE, related_name='epub')
    downloadLink = models.URLField(null=True)
    acsTokenLink = models.URLField(null=True)
    isAvailable = models.BooleanField()


class Pdf(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE, related_name='pdf')
    downloadLink = models.URLField(null=True)
    acsTokenLink = models.URLField(null=True)
    isAvailable = models.BooleanField()


class DownloadAccess(models.Model):
    accessInfo = models.OneToOneField(AccessInfo, on_delete=models.CASCADE, related_name='downloadAccess')
    kind = models.CharField(max_length=100)
    volumeId = models.CharField(max_length=100, null=True)
    restricted = models.BooleanField()
    deviceAllowed = models.BooleanField()
    justAcquired = models.BooleanField()
    maxDownloadDevices = models.IntegerField()
    downloadsAcquired = models.IntegerField()
    nonce = models.CharField(max_length=100, null=True)
    source = models.CharField(max_length=100, null=True)
    reasonCode = models.CharField(max_length=100, null=True)
    message = models.TextField()
    signature = models.CharField(max_length=100, null=True)



