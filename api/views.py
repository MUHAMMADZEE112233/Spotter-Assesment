from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Book, Author, FavoriteBook
from .serializers import BookSerializer, AuthorSerializer, FavoriteBookSerializer
from django.db.models import Q

from .utils import get_recommendations_for_user

class BookListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating books.

    This view allows authenticated users to retrieve a list of all books
    or create a new book. It supports an optional search query parameter 
    to filter books by title or author name.

    Methods:
        - get_queryset: Filters the queryset based on the 'search' query parameter.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of books. If a 'search' parameter is provided,
        it filters the books based on the title or author name.

        Returns:
            queryset: Filtered queryset of books.
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author_name__icontains=search_query)
            )
        return queryset


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a book.

    This view allows authenticated users to retrieve, update, or delete a 
    specific book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating authors.

    This view allows authenticated users to retrieve a list of all authors
    or create a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting an author.

    This view allows authenticated users to retrieve, update, or delete an 
    author by their ID.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class FavoriteBookView(generics.ListCreateAPIView):
    """
    API view for managing favorite books.

    This view allows authenticated users to:
        - Retrieve a list of their favorite books.
        - Add a new favorite book.
        - Delete a favorite book by ID (via DELETE request).
        - Get book recommendations after any action.
    """
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of favorite books for the current user.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the new favorite book, and after saving, provide updated recommendations.
        """
        serializer.save(user=self.request.user)

        recommendations = get_recommendations_for_user(self.request.user)

        self.recommendations = recommendations

    def create(self, request, *args, **kwargs):
        """
        Override the create method to return recommendations in the response.
        """
        response = super().create(request, *args, **kwargs)

        response.data['recommendations'] = self.recommendations
        return response
        

    def list(self, request, *args, **kwargs):
        """
        Returns a list of favorite books and book recommendations.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        favorites_data = serializer.data
        recommendations = get_recommendations_for_user(request.user)

        return Response({
            'favorites': favorites_data,
            'recommendations': recommendations
        }, status=200)


class FavoriteBookDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a favorite book by 'book_id'.
    """
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Deletes a favorite book using 'book_id' from the URL.
        """
        book_id = kwargs.get('book_id')
        
        try:
            favorite_book = self.get_queryset().get(id=book_id)
        except FavoriteBook.DoesNotExist:
            return Response({"error": "Favorite book not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite_book.delete()

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        favorites_data = serializer.data

        recommendations = get_recommendations_for_user(request.user)

        return Response({
            'message': f"Favorite book with ID {book_id} has been deleted.",
            'recommendations': recommendations
        }, status=status.HTTP_200_OK)

