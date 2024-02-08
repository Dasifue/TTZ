from rest_framework import viewsets, permissions

from apps.books.serializers import AuthorBiographySerializer, AuthorSerializer, GenreSerializer, BookSerializer
from apps.books.models import AuthorBiography, Author, Genre, Book


class AuthorBiographyViewSet(viewsets.ModelViewSet):
    queryset = AuthorBiography.objects.all()
    serializer_class = AuthorBiographySerializer
    lookup_field = "pk"

    permission_classes = [permissions.AllowAny]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "pk"

    permission_classes = [permissions.AllowAny]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "pk"

    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"

    permission_classes = [permissions.AllowAny]