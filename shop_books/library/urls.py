from . import views
from django.urls import path, include
from rest_framework import routers

app_name = 'book'

router = routers.DefaultRouter()

router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
