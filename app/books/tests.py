import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer

client = APIClient()


class CreateNewBookTest(APITestCase):
    """ Test for creating new book API """

    def setUp(self) -> None:
        self.invalid_payload = {
            'kind': 'books#volume',
            'id': '',
            'etag': 'VZExkpZl+ak',
            'selfLink': 'https://www.googleapis.com/books/v1/volumes/rToaogEACAAJ',
        }
        self.valid_payload = {
            'kind': 'books#volume',
            'id': 'rToaogEACAAJ',
            'etag': 'VZExkpZl+ak',
            'selfLink': 'https://www.googleapis.com/books/v1/volumes/rToaogEACAAJ',
        }

    def test_create_valid_book(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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

