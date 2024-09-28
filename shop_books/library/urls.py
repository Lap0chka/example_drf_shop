from . import views
from django.urls import path

app_name = 'book'

urlpatterns = [
    path('books/', views.BookViewSet.as_view(), name='books'),
    path('books/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),

    # authors
    path('authors/', views.AuthorViewSet.as_view(), name='authors'),
    path('authors/<slug:slug>/', views.AuthorDetailView.as_view(), name='author_detail'),

    # category
    path('categories/', views.CategoryViewSet.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.CategoryBookViewSet.as_view(), name='categories'),
]
