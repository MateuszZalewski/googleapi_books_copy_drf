from django.db import models


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


class Book(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    authors = models.ManyToManyField(Author, related_name='authors')
    categories = models.ManyToManyField(Category, related_name='categories')
    published_date = models.CharField(max_length=10, null=True)
    average_rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)
    thumbnail = models.URLField(null=True)
