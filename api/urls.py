from django.urls import path
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDestroyView,
    AuthorListCreateView,
    AuthorRetrieveUpdateDestroyView,
    FavoriteBookView,
    FavoriteBookDeleteView
)

urlpatterns = [
    path("api/books/", BookListCreateView.as_view(), name="book-list-create"),
    path(
        "api/books/<int:pk>/",
        BookRetrieveUpdateDestroyView.as_view(),
        name="book-detail",
    ),
    path("api/authors/", AuthorListCreateView.as_view(), name="author-list-create"),
    path(
        "api/authors/<int:pk>/",
        AuthorRetrieveUpdateDestroyView.as_view(),
        name="author-detail",
    ),
    path("api/favorites/", FavoriteBookView.as_view(), name="favorite-list-create"),
    path('api/favorites/<int:book_id>/', FavoriteBookDeleteView.as_view(), name='favorite-book-delete'),
]
