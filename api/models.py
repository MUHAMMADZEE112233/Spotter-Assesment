from django.conf import settings
from django.db import models


class Author(models.Model):
    """Represent an author with a name."""

    name = models.CharField(max_length=255)


class Book(models.Model):
    """Represent a book with a title and an associated author."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)


class FavoriteBook(models.Model):
    """Store a user's favorite book, linking a user to a book."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
