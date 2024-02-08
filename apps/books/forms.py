from django import forms

from .models import AuthorBiography, Author, Genre, Book

class AuthorBiographyForm(forms.ModelForm):

    class Meta:
        model = AuthorBiography
        exclude = ("author",)


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = "__all__"


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = "__all__"


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ("author", "uploaded_at")