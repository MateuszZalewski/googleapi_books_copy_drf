import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Book, SearchInfo
from .serializers import BookSerializer

client = APIClient()


class DeleteBookTest(APITestCase):
    """ Test deleting single book """
    fixtures = ['books.json']

    def test_delete_book_valid(self):
        book = Book.objects.first()
        count_before = Book.objects.count()
        response = client.delete(
            reverse('books-detail', kwargs={'pk': book.pk}))

        self.assertEqual(Book.objects.count(), count_before-1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_invalid(self):
        count_before = Book.objects.count()
        response = client.delete(
            reverse('books-detail', kwargs={'pk': 5}))

        self.assertEqual(Book.objects.count(), count_before)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class CreateNewBooksTest(APITestCase):
    """ Test creating multiple books at once API """

    def setUp(self) -> None:
        self.invalid_payload = {
            'items': [
                {
                    'kind': 'books#volume',
                    'id': 'rToaogEACAAJ',
                    'etag': 5,
                    'selfLink': 'https://www.googleapis.com/books/v1/volumes/rToaogEACAAJ',
                    "searchInfo": {
                        "textSnippet": "Poradnik do gry Dragon Ball Z Kakarot to potężne kompendium wiedzy, "
                                       "które ułatwi ci ukończenie gry i pozwoli odkryć wszystkie sekrety w grze. "
                    }
                },
                {
                    "kind": "books#volume",
                    "id": "4qNgDgAAQBAJ",
                    "etag": "bkFi7TmefBw",
                    "selfLink": 12,
                },
            ],
        }
        self.valid_payload = {
            'items': [
                {
                    'kind': 'books#volume',
                    'id': 'rToaogEACAAJ',
                    'etag': 'VZExkpZl+ak',
                    'selfLink': 'https://www.googleapis.com/books/v1/volumes/rToaogEACAAJ',
                    "searchInfo": {
                        "textSnippet": "Poradnik do gry Dragon Ball Z Kakarot to potężne kompendium wiedzy, "
                                       "które ułatwi ci ukończenie gry i pozwoli odkryć wszystkie sekrety w grze. "
                    }
                },
                {
                    "kind": "books#volume",
                    "id": "4qNgDgAAQBAJ",
                    "etag": "bkFi7TmefBw",
                    "selfLink": "https://www.googleapis.com/books/v1/volumes/4qNgDgAAQBAJ",
                },
            ],
        }

    def test_create_books_valid(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(SearchInfo.objects.count(), 1)

    def test_create_books_invalid(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)


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

    def test_create_book_valid(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_invalid(self):
        response = client.post(
            reverse('books-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)


class GetAllBooksTest(APITestCase):
    """ Test for GET all books API """

    fixtures = ['books.json']

    def test_get_all_books(self):
        response = client.get(reverse('books-list'))

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data['kind'], 'books#volumes')
        self.assertEqual(response.data['items'], serializer.data)
        self.assertEqual(response.data['totalItems'], len(serializer.data))
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

