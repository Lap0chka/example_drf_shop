import random

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAdminUser
from rest_framework.response import Response

from library.models import Book, Author, Category, Comment
from library.serializers import BookSerializer, AuthorSerializer, CategorySerializer, CommentSerializer


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BookViewSet(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = ResultsSetPagination


class AuthorViewSet(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = ResultsSetPagination


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'

    def get_object(self):
        return get_object_or_404(Author, slug=self.kwargs[self.lookup_field])


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=self.kwargs[self.lookup_field])
        comments = Comment.objects.filter(book=book)

        book_serializer = BookSerializer(book)
        comments_serializer = CommentSerializer(comments, many=True)

        return Response({
            'book': book_serializer.data,
            'comments': comments_serializer.data
        }, status=status.HTTP_200_OK)


class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ResultsSetPagination


class CategoryBookViewSet(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = ResultsSetPagination
    lookup_field = 'slug'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs[self.lookup_field])
        return Book.objects.filter(category=category)


