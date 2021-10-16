from django.db import models
from .book import Book


class SaleInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    saleability = models.CharField(max_length=100)
    isEbook = models.BooleanField()
    buyLink = models.URLField()
    onSaleDate = models.DateTimeField()


class RetailPrice(models.Model):
    saleInfo = models.OneToOneField(SaleInfo, on_delete=models.CASCADE)
    # amountInMicros = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    currencyCode = models.CharField(max_length=3)


class ListPrice(models.Model):
    saleInfo = models.OneToOneField(SaleInfo,  on_delete=models.CASCADE)
    # amountInMicros = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    currencyCode = models.CharField(max_length=3)


class Offer(models.Model):
    saleInfo = models.ForeignKey(SaleInfo, on_delete=models.CASCADE)
    listPrice = models.ForeignKey(ListPrice, on_delete=models.CASCADE)
    retailPrice = models.ForeignKey(RetailPrice, on_delete=models.CASCADE)
    finskyOfferType = models.IntegerField()
