from .serializers import AuthorSerializer, BookSerializer, LeadSerializer, LibrarySerializer, TokenSerializer, UserSerializer
from .models import Book, Author, Library, Lead
from .decorators import validate_library_data, validate_book_data

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListCreateBookView(generics.ListCreateAPIView):
    """
    GET book/
    POST book/
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
    pass


class ListCreateLibraryView(generics.ListCreateAPIView):
    """
    GET libraries/
    POST library/
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
    GET library/:id/
    PUT library/:id/
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
    GET library/:id/books/:id
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


# class LeadListView(generics.ListAPIView):
#     paginate_by = 10
#     model = Lead
#     context_object_name = 'leads'
#
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer
#
#     def get_queryset(self):
#         qs = super(LeadListView, self).get_queryset()
#         qs.order_by('email')
#         return qs


# book_list_view = BookListView.as_view()
# author_list_view = AuthorListView.as_view()

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
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


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
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
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )


# Libraries views
library_list_create_view = ListCreateLibraryView.as_view()
library_detail_view = LibraryDetailView.as_view()
library_book_detail_view = LibraryBookDetailView.as_view()
# Books views
book_list_create_view = ListCreateBookView.as_view()
book_detail_view = BookDetailView.as_view()
# Login view
login_view = LoginView.as_view()
register_users = RegisterUsers.as_view()

# lead_list_view = LeadListView.as_view()
