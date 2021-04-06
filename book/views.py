from .serializers import AuthorSerializer, BookSerializer, LeadSerializer, LibrarySerializer, TokenSerializer, \
    UserSerializer
from .models import Book, Author, Library, Lead
from .decorators import validate_library_data, validate_book_data, validate_lead_data, validate_author_data

from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# BOOK VIEWS
class ListCreateBookView(generics.ListCreateAPIView):
    """
    GET /book
    POST /book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_book_data
    def post(self, request, *args, **kwargs):
        author = Author.objects.get(pk=request.data["author"]["id"])
        if author:
            book = Book.objects.create(
                title=request.data["title"],
                author=author
            )
            if "libraries" in request.data:
                for library in request.data["libraries"]:
                    if not library["id"]:
                        return Response(
                            data={
                                "message": "Library id is required".format(request.data["author"]["id"])
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    book.libraries.add(library["id"])

            return Response(
                data=BookSerializer(book).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(request.data["author"]["id"])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET /book/:id
        PUT /book/:id
        """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            return Response(
                data={
                    "message": "Book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_book_data
    def put(self, request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            serializer = BookSerializer()
            updated_book = serializer.update(book, request.data)
            return Response(BookSerializer(updated_book).data)
        except Book.DoesNotExist:
            return Response(
                data={
                    "message": "book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SearchBookView(generics.ListAPIView):
    """
    GET /search
    """
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)


# AUTHOR VIEWS
class ListCreateAuthorView(generics.ListCreateAPIView):
    """
    GET /author
    POST /author
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_author_data
    def post(self, request, *args, **kwargs):
        author = Author.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"]
        )
        return Response(
            data=AuthorSerializer(author).data,
            status=status.HTTP_201_CREATED
        )


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /author/:id
    PUT /author/:id
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            author = self.queryset.get(pk=kwargs["pk"])
            return Response(AuthorSerializer(author).data)
        except Author.DoesNotExist:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_author_data
    def put(self, request, *args, **kwargs):
        try:
            author = self.queryset.get(pk=kwargs["pk"])
            serializer = AuthorSerializer()
            updated_library = serializer.update(author, request.data)
            return Response(AuthorSerializer(updated_library).data)
        except Author.DoesNotExist:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


# LEAD VIEWS
class ListCreateLeadView(generics.ListCreateAPIView):
    """
    GET /lead
    POST /lead
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_lead_data
    def post(self, request, *args, **kwargs):
        # find library by pk
        library = Library.objects.get(pk=int(request.data["library"]))
        # Create lead
        lead = Lead.objects.create(
            email=request.data["email"],
            fullname=request.data["fullname"],
            phone=request.data["phone"],
            library=library
        )
        send_mail(
            'Lead Created',
            'Welcome to our platform of books {}'.format(lead.fullname),
            'from@example.com',
            [lead.email],
            fail_silently=False
        )

        return Response(
            data=LeadSerializer(lead).data,
            status=status.HTTP_201_CREATED
        )


# LIBRARY VIEWS
class ListCreateLibraryView(generics.ListCreateAPIView):
    """
    GET /library
    POST /library
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_library_data
    def post(self, request, *args, **kwargs):
        library = Library.objects.create(
            name=request.data["name"],
        )
        return Response(
            data=LibrarySerializer(library).data,
            status=status.HTTP_201_CREATED
        )


class LibraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /library/:id
    PUT /library/:id
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            library = self.queryset.get(pk=kwargs["pk"])
            return Response(LibrarySerializer(library).data)
        except Library.DoesNotExist:
            return Response(
                data={
                    "message": "Library with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_library_data
    def put(self, request, *args, **kwargs):
        try:
            library = self.queryset.get(pk=kwargs["pk"])
            serializer = LibrarySerializer()
            updated_library = serializer.update(library, request.data)
            return Response(LibrarySerializer(updated_library).data)
        except Library.DoesNotExist:
            return Response(
                data={
                    "message": "Library with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LibraryBookDetailView(generics.RetrieveAPIView):
    """
    GET /library/:id/books/:id
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return

    def get(self, request, *args, **kwargs):
        book = self.queryset.filter(
            pk=kwargs["book_pk"],
            libraries=kwargs["pk"]
        )
        if book:
            return Response(BookSerializer(book, many=True).data)

        return Response(
            data={
                "message": "Book with id: {} does not exist in the library".format(kwargs["book_pk"])
            },
            status=status.HTTP_404_NOT_FOUND
        )


# lOGIN VIEW
class LoginView(generics.CreateAPIView):
    """
    POST /auth/login
    """
    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "username": username,
                "password": password,
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(
                data={
                    "message": "User logged in successfully",
                    "token": serializer.initial_data["token"]
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# REGISTER VIEW
class RegisterUsers(generics.CreateAPIView):
    """
    POST /auth/register
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user_email_exist = User.objects.filter(email=email)
        user_username_exist = User.objects.filter(username=username)
        if not user_email_exist and not user_username_exist:
            new_user = User.objects.create_user(
                username=username, password=password, email=email
            )
            return Response(
                data=UserSerializer(new_user).data,
                status=status.HTTP_201_CREATED
            )
        if user_email_exist:
            return Response(
                data={
                    "message": "User with email {} it already exists".format(email)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif user_username_exist:
            return Response(
                data={
                    "message": "User with username {} it already exists".format(username)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# Libraries views
library_list_create_view = ListCreateLibraryView.as_view()
library_detail_view = LibraryDetailView.as_view()
library_book_detail_view = LibraryBookDetailView.as_view()
# Books views
book_list_create_view = ListCreateBookView.as_view()
book_detail_view = BookDetailView.as_view()
book_search_view = SearchBookView.as_view()
# Lead Views
lead_list_create_view = ListCreateLeadView.as_view()
# Author Views
author_list_create_view = ListCreateAuthorView.as_view()
author_detail_view = AuthorDetailView.as_view()
# Login view
login_view = LoginView.as_view()
register_users = RegisterUsers.as_view()


