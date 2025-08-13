from django.urls import path, include
from rest_framework.routers import DefaultRouter

from journal.api.views import  AuthorViewSet, GenreViewSet, BookLogViewSet, BookViewSet, QuoteViewSet, LikeViewSet, ShareViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'genres',  GenreViewSet, basename='genres')
router.register(r'books',   BookViewSet, basename='books')
router.register(r'logs',    BookLogViewSet, basename='book_logs')
router.register(r'quotes',  QuoteViewSet, basename='quotes')
router.register(r'likes',   LikeViewSet, basename='likes')
router.register(r'shares',  ShareViewSet, basename='shares')


urlpatterns = [
  path('', include(router.urls)),
]

