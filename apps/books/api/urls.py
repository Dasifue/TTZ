from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("author_biographies", viewset=views.AuthorBiographyViewSet)
router.register("authors", viewset=views.AuthorViewSet)
router.register("genres", viewset=views.GenreViewSet)
router.register("books", viewset=views.BookViewSet)


urlpatterns = [
    path("", include(router.urls)),
]