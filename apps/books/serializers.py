from rest_framework import serializers

from .models import Author, AuthorBiography, Genre, Book


class AuthorBiographySerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorBiography
        fields = "__all__"
        read_only = ("id",)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"
        read_only = ("id",)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"
        read_only = ("id",)


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"
        read_only = ("id", "uploaded_at")