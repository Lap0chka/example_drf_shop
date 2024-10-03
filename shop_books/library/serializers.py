from rest_framework import serializers
from library.models import Book, Author, Category, Comment
from typing import List, Optional


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    class Meta:
        model = Book
        fields: List[str] = ['id', 'title', 'description',
                             'author', 'category', 'publication_date']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model."""

    class Meta:
        model = Author
        fields: List[str] = ['id', 'name', 'surname', 'biography', 'city',
                             'born', 'died', 'country', 'image', 'book']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        model = Category
        fields: List[str] = ['id', 'name', 'slug', 'parent']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    class Meta:
        model = Comment
        fields: List[str] = '__all__'


