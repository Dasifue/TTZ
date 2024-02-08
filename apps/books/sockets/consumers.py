from apps.books.models import Author, AuthorBiography, Genre, Book
from apps.books.serializers import AuthorSerializer, AuthorBiographySerializer, GenreSerializer, BookSerializer

from .model_consumer import ModelConsumer

class AuthorConsumer(ModelConsumer):
    model = Author
    serializer_class = AuthorSerializer
    action_preffix = "author"
    queryset = Author.objects.all()

    def create(self, data: dict, notification: bool = True):
        return super().create(data, notification)


class AuthorBiographyConsumer(ModelConsumer):
    model = AuthorBiography
    serializer_class = AuthorBiographySerializer
    action_preffix = "biography"
    queryset = AuthorBiography.objects.all()


class GenreConsumer(ModelConsumer):
    model = Genre
    serializer_class = GenreSerializer
    action_preffix = "genre"
    queryset = Genre.objects.all()


class BookConsumer(ModelConsumer):
    model = Book
    serializer_class = BookSerializer
    action_preffix = "book"
    queryset = Book.objects.all()
    prefetch_related = "genres"

    def create(self, data: dict, notification: bool = True):
        return super().create(data, notification)