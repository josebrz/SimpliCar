import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Library, Lead, Book, Author
from .serializers import LibrarySerializer, BookSerializer, AuthorSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_library(name=""):
        if name != "":
            library = Library.objects.create(
                name=name
            )
            return library

    @staticmethod
    def create_author(first_name="", last_name=""):
        if first_name != "" and last_name != "":
            author = Author.objects.create(
                first_name=first_name,
                last_name=last_name
            )
            return author

    @staticmethod
    def create_book(title, author, libraries):
        if title != '' and author:
            book = Book.objects.create(
                title=title,
                author=author,
            )
            book.libraries.add(libraries.id)

    def make_a_request(self, view_name, kind="post", **kwargs):
        """
        Make a post/put request to create a library
        """
        if kind == "post":
            return self.client.post(
                reverse(
                    view_name,
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        elif kind == "put":
            return self.client.put(
                reverse(
                    view_name,
                    kwargs={
                        "pk": kwargs["pk"]
                    }
                ),
                data=json.dumps(kwargs["data"]),
                content_type='application/json'
            )
        else:
            return None

    def fetch_author(self, pk=0):
        return self.client.get(
            reverse(
                "author-detail",
                kwargs={
                    "pk": pk
                }
            )
        )

    def fetch_library(self, pk=0):
        return self.client.get(
            reverse(
                "library-detail",
                kwargs={
                    "pk": pk
                }
            )
        )

    def fetch_book_in_library(self, pk=0, book_pk=0):
        return self.client.get(
            reverse(
                "library-book-list",
                kwargs={
                    "pk": pk,
                    "book_pk": book_pk
                }
            )
        )

    def fetch_book(self, pk=0):
        return self.client.get(
            reverse(
                "book-detail",
                kwargs={
                    "pk": pk
                }
            )
        )

    def search_books(self, param):
        return self.client.get(
             path='http://127.0.0.1:8000/api/book/search',
             data={
                 'text': param
             }
            )

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login"
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register"
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def setUp(self):
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        # Create Libraries
        library1 = self.create_library('Crecer')
        library2 = self.create_library('Lotus')
        library3 = self.create_library('El Ático Azul')
        library4 = self.create_library('Crónicas Doradas')
        # Create Authors
        author1 = self.create_author('José', 'Brizuela')
        author2 = self.create_author('Sofia', 'Echave')
        author3 = self.create_author('Patricia', 'Rios')
        author4 = self.create_author('Nicolas', 'Catalano')
        # Create Books
        self.create_book("Oil idea detail up.", author4, library4)
        self.create_book("Trade agent test firm leg once new.", author3, library3)
        self.create_book("Save control throughout card on town though.", author2, library2)
        self.create_book("Leg challenge campaign exactly.", author1, library1)

        # Expected Values (Valid-Invalid)
        self.valid_author_data = {
            "id": 2,
            "first_name": "test first_name",
            "last_name": "test last_name",
        }
        self.valid_author_data_post = {
            "id": 5,
            "first_name": "test first_name",
            "last_name": "test last_name",
        }

        self.invalid_author_data = {
            "id": 2,
            "first_name": "",
            "last_name": "",
        }

        self.valid_library_data = {
            "id": 2,
            "name": "test name",
        }
        self.valid_library_data_post = {
            "id": 5,
            "name": "test name",
        }
        self.invalid_library_data = {
            "id": 5,
            "name": "",
        }
        self.valid_book_data = {
            "title": "Test title",
            "author": {
                "id": 1
            },
            "libraries": [
                {
                    "id": 1
                }
            ]
        }

        self.invalid_book_data = {
            "title": "",
            "author": {
                "id": 9999
            },
            "libraries": [
                {
                    "id": 9999
                }
            ]
        }

        self.valid_book_data_put = {
            "id": 2,
            "title": "Test title",
            "author": {
                "id": 1,
                "first_name": "José",
                "last_name": "Brizuela"
            },
            "libraries": [
                {
                    "id": 1,
                    "name": "Crecer"
                },
            ]
        }

        self.valid_book_data_post = {
            "id": 5,
            "title": "Test title",
            "author": {
                "id": 1,
                "first_name": "José",
                "last_name": "Brizuela"
            },
            "libraries": [
                {
                    "id": 1,
                    "name": "Crecer"
                }
            ]
        }
        self.valid_lead_data_post = {
            "email": "test@test.com",
            "fullname": "test test",
            "phone": "123456",
            "library": 1
        }
        self.invalid_lead_data = {
            "email": "",
            "fullname": "",
            "phone": "",
            "library": 1
        }

        self.valid_id = 1
        self.invalid_id = 11000


# Author TESTs
class GetSingleAuthorTest(BaseViewTest):

    def test_get_author_by_pk(self):
        """
        This test ensures that a single author of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_author(self.valid_id)
        # fetch the data from db
        expected = Author.objects.get(pk=self.valid_id)
        serialized = AuthorSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a author that does not exist
        response = self.fetch_author(self.invalid_id)
        self.assertEqual(
            response.data["message"],
            "Author with id: 11000 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateAuthorTest(BaseViewTest):

    def test_put_library_by_pk(self):
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="author-detail",
            kind='put',
            pk=2,
            data=self.valid_author_data
        )
        self.assertEqual(response.data, self.valid_author_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            view_name="author-detail",
            kind="put",
            pk=3,
            data=self.invalid_author_data
        )
        self.assertEqual(
            response.data["message"],
            "The first name and last name is required to add a Author"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddAuthorTest(BaseViewTest):

    def test_post_author(self):
        """
        This test ensures that a single author can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="author-list-create",
            kind="post",
            data=self.valid_author_data
        )
        self.assertEqual(response.data, self.valid_author_data_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            view_name="author-list-create",
            kind="post",
            data=self.invalid_author_data
        )
        self.assertEqual(
            response.data["message"],
            "The first name and last name is required to add a Author"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Library TESTs
class GetLibrariesTest(BaseViewTest):

    def test_get_all_libraries(self):
        """
            This test ensures that all libraries added in the setUp method
            exist when we make a GET request to the libraries/ endpoint
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("library-list-create")
        )
        # fetch the data from db
        expected = Library.objects.all()
        serialized = LibrarySerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleLibraryTest(BaseViewTest):

    def test_get_library_by_pk(self):
        """
        This test ensures that a single library of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_library(self.valid_id)
        # fetch the data from db
        expected = Library.objects.get(pk=self.valid_id)
        serialized = LibrarySerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a library that does not exist
        response = self.fetch_library(self.invalid_id)
        self.assertEqual(
            response.data["message"],
            "Library with id: 11000 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateLibraryTest(BaseViewTest):

    def test_put_library_by_pk(self):
        """
        This test ensures that only one library can be updated. In this
        test, we update the second database library with valid data and
        the third library with invalid data and make claims
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="library-detail",
            kind='put',
            pk=2,
            data=self.valid_library_data
        )
        self.assertEqual(response.data, self.valid_library_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            view_name="library-detail",
            kind="put",
            pk=3,
            data=self.invalid_library_data
        )
        self.assertEqual(
            response.data["message"],
            "The name is required to add a library"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddLibraryTest(BaseViewTest):

    def test_post_library(self):
        """
        This test ensures that a single library can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="library-list-create",
            kind="post",
            data=self.valid_library_data
        )
        self.assertEqual(response.data, self.valid_library_data_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            view_name="library-list-create",
            kind="post",
            data=self.invalid_library_data
        )
        self.assertEqual(
            response.data["message"],
            "The name is required to add a library"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSingleLibraryBookTest(BaseViewTest):

    def test_get_library_book_by_pk(self):
        """
        This test ensures that a single book in a library with a given ID is
        returned
        """
        queryset = Book.objects.all()

        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_book_in_library(pk=1, book_pk=4)
        # fetch the data from db
        expected = queryset.filter(pk=4, libraries=1)
        serialized = BookSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a book that does not exist
        response = self.fetch_book_in_library(self.invalid_id, self.invalid_id)
        self.assertEqual(
            response.data["message"],
            "Book with id: 11000 does not exist in the library"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Books TEST
class GetBookTest(BaseViewTest):

    def test_get_all_books(self):
        """
            This test ensures that all books added in the setUp method
            exist when we make a GET request to the book/ endpoint
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("book-list-create")
        )
        # fetch the data from db
        expected = Book.objects.all()
        serialized = BookSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddBookTest(BaseViewTest):

    def test_post_book(self):
        """
        This test ensures that a single Book can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="book-list-create",
            kind="post",
            data=self.valid_book_data
        )

        self.assertEqual(response.data, self.valid_book_data_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            view_name="book-list-create",
            kind="post",
            data=self.invalid_book_data
        )
        self.assertEqual(
            response.data["message"],
            "The title is required to add/update a Book"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateBookTest(BaseViewTest):

    def test_put_book_by_pk(self):
        """
        This test ensures that only one Book can be updated. In this
        test, we update the second database book with valid data and
        the third book with invalid data and make claims
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="book-detail",
            kind='put',
            pk=2,
            data=self.valid_book_data
        )

        self.assertEqual(response.data, self.valid_book_data_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with invalid data
        response = self.make_a_request(
            view_name="book-detail",
            kind="put",
            pk=3,
            data=self.invalid_book_data
        )
        self.assertEqual(
            response.data["message"],
            "The title is required to add/update a Book"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSingleBookTest(BaseViewTest):

    def test_get_book_by_pk(self):
        """
        This test ensures that a single book of a given id is
        returned
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.fetch_book(self.valid_id)
        # fetch the data from db
        expected = Book.objects.get(pk=self.valid_id)
        serialized = BookSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test with a library that does not exist
        response = self.fetch_book(self.invalid_id)
        self.assertEqual(
            response.data["message"],
            "Book with id: 11000 does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SearchBookTest(BaseViewTest):

    def test_search_book_by_param(self):
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.search_books('throughout')
        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Lead TEST
class AddLeadTest(BaseViewTest):

    def test_post_lead(self):
        """
        This test ensures that a single lead can be added
        """
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.make_a_request(
            view_name="lead-list-create",
            kind="post",
            data=self.valid_lead_data_post
        )

        self.assertEqual(response.data, self.valid_lead_data_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.make_a_request(
            view_name="lead-list-create",
            kind="post",
            data=self.invalid_lead_data
        )
        self.assertEqual(
            response.data["message"],
            "The email is required to add a Lead"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# Auth TEST
class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """

    def test_register_a_user(self):
        response = self.register_a_user("new_user", "new_pass", "new_user@mail.com")
        # assert status code is 201 CREATED
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
