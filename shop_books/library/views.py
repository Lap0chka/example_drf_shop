from typing import Any, List
from urllib.request import Request

from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Book, Author, Category, Comment
from library.serializers import BookSerializer, AuthorSerializer, CategorySerializer, CommentSerializer


class ResultsSetPagination(PageNumberPagination):
    """Custom pagination class to control the pagination of results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = ResultsSetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a book and its comments."""
        book = get_object_or_404(Book, slug=self.kwargs[self.lookup_field])
        comments = Comment.objects.filter(book=book)

        book_serializer = BookSerializer(book)
        comments_serializer = CommentSerializer(comments, many=True)

        return Response({
            'book': book_serializer.data,
            'comments': comments_serializer.data
        }, status=status.HTTP_200_OK)


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for managing authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = ResultsSetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'

    def get_object(self) -> Author:
        """Retrieve an author object by slug."""
        return get_object_or_404(Author, slug=self.kwargs[self.lookup_field])


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ResultsSetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a specific category with its books."""
        self.object = self.get_object()
        books = Book.objects.filter(category=self.object)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self) -> Category:
        """Retrieve a category object by slug."""
        return get_object_or_404(Category, slug=self.kwargs[self.lookup_field])


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = ResultsSetPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'