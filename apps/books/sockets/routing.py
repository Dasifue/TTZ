from django.urls import re_path

from . import consumers

websocket_urlpatters = [
    re_path("ws/authors/", view=consumers.AuthorConsumer.as_asgi()),
    re_path("ws/biography/", view=consumers.AuthorBiographyConsumer.as_asgi()),
    re_path("ws/genres/", view=consumers.GenreConsumer.as_asgi()),
    re_path("ws/books/", view=consumers.BookConsumer.as_asgi())
]