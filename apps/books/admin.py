from django.contrib import admin

from .models import Author, AuthorBiography, Genre, Book


class BiographyInline(admin.StackedInline):
    model = AuthorBiography


@admin.register(Author)
class AdminAuthor(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_display_links = list_display
    inlines = (BiographyInline,)


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = ("id", "author", "name")
    search_fields = ("name",)
    list_filter = ("author",)
    list_display_links = list_display


@admin.register(Genre)
class AdminGenre(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_display_links = list_display