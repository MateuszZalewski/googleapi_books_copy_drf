from rest_framework import status
from rest_framework.test import APITestCase
from django.test import Client
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer

client = Client()


class GetAllBooksTest(APITestCase):
    """ Test for GET all books API """

    fixtures = ['books.json']

    def test_get_all_books(self):
        response = client.get(reverse('books-list'))

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleBookTest(APITestCase):
    """ Test for GET single book API """

    fixtures = ['books.json']

    def test_get_book_valid(self):
        book = Book.objects.first()
        response = client.get(
            reverse('books-detail', kwargs={'pk': book.pk}))

        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_invalid(self):
        response = client.get(
            reverse('books-detail', kwargs={'pk': '1'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

