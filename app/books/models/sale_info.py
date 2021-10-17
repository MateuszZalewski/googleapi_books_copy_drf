from django.db import models
from .book import Book


class SaleInfo(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='saleInfo')
    country = models.CharField(max_length=100, null=True)
    saleability = models.CharField(max_length=100, null=True)
    isEbook = models.BooleanField()
    buyLink = models.URLField(null=True)
    onSaleDate = models.DateTimeField(null=True)


class RetailPrice(models.Model):
    saleInfo = models.OneToOneField(SaleInfo, on_delete=models.CASCADE, related_name='retailPrice')
    # amountInMicros = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    currencyCode = models.CharField(max_length=3)


class ListPrice(models.Model):
    saleInfo = models.OneToOneField(SaleInfo,  on_delete=models.CASCADE, related_name='listPrice')
    # amountInMicros = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    currencyCode = models.CharField(max_length=3)


class Offer(models.Model):
    saleInfo = models.OneToOneField(SaleInfo, on_delete=models.CASCADE, related_name='offer')
    listPrice = models.ForeignKey(ListPrice, on_delete=models.CASCADE)
    retailPrice = models.ForeignKey(RetailPrice, on_delete=models.CASCADE)
    finskyOfferType = models.IntegerField()
