from django.views import generic

from .models import Author, AuthorBiography, Genre, Book
from .forms import AuthorForm, AuthorBiographyForm, GenreForm, BookForm

class HomeView(generic.TemplateView):
    template_name = "base.html"

