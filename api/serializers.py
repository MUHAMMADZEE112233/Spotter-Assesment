from rest_framework import serializers
from .models import Book, Author, FavoriteBook
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, handles user creation and password hashing."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Creates a new user instance with hashed password."""
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model, representing the author's details."""

    class Meta:
        model = Author
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model, includes nested author details."""

    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ["id", "title", "author"]

    def create(self, validated_data):
        """Creates a new book instance, creating or getting an associated author."""
        author_data = validated_data.pop("author")
        author, created = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book


class FavoriteBookSerializer(serializers.ModelSerializer):
    """Serializer for the FavoriteBook model, linking a user to a book."""

    class Meta:
        model = FavoriteBook
        fields = ["id", "user", "book"]
        read_only_fields = ["user"]
