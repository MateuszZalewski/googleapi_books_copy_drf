from django.db import models
from .book import Book


class SearchInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='searchInfo')
    textSnippet = models.TextField()
