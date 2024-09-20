from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Book, FavoriteBook
from .serializers import BookSerializer

def get_recommendations_for_user(user):
    """
    Generates book recommendations based on a user's favorite books.

    Args:
        user (User): The user whose favorite books will be used for recommendations.

    Returns:
        list: Serialized data of recommended books.
    """
    favorite_books = FavoriteBook.objects.filter(user=user)
    if not favorite_books:
        return []

    favorite_titles = [favorite_book.book.title for favorite_book in favorite_books]
    favorite_authors = {favorite_book.book.author for favorite_book in favorite_books}

    all_books = Book.objects.exclude(id__in=[favorite_book.book.id for favorite_book in favorite_books])
    all_titles = list(all_books.values_list('title', flat=True))

    tfidf_matrix = TfidfVectorizer().fit_transform(all_titles + favorite_titles)
    similarities = cosine_similarity(tfidf_matrix[-len(favorite_titles):], tfidf_matrix[:-len(favorite_titles)])

    recommended_indices = similarities[-1].argsort()[-5:][::-1].tolist()
    recommended_books = [all_books[i] for i in recommended_indices]

    if len(recommended_books) >= 5:
        return BookSerializer(recommended_books[:5], many=True).data

    author_recommendations = Book.objects.filter(author__in=favorite_authors)\
                                        .exclude(id__in=[favorite_book.book.id for favorite_book in favorite_books])[:5]

    combined_recommendations = list(recommended_books) + list(author_recommendations)

    if len(combined_recommendations) >= 5:
        return BookSerializer(combined_recommendations[:5], many=True).data

    remaining_count = 5 - len(combined_recommendations)
    random_books = list(Book.objects.exclude(id__in=[book.id for book in combined_recommendations]).order_by('?')[:remaining_count])

    final_recommendations = combined_recommendations + random_books

    return BookSerializer(final_recommendations[:5], many=True).data
