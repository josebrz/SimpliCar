from rest_framework import serializers
from .models import Author, Book, Library, Lead
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    libraries = LibrarySerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = "__all__"

    def update(self, instance, validated_data):
        # We are looking for an author by id
        author = Author.objects.get(pk=validated_data["author"]["id"])

        instance.title = validated_data.get("title", instance.title)
        instance.author = author
        instance.libraries.set([])

        # if there are libraries in the request
        if "libraries" in validated_data:
            for library in validated_data["libraries"]:
                instance.libraries.add(library["id"])

        # Saved Instance
        instance.save()
        return instance


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = ("email", "fullname", "phone", "library")


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")