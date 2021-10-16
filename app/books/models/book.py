from django.db import models


class Book(models.Model):
    kind = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    etag = models.CharField(max_length=100)
    selfLink = models.URLField()
