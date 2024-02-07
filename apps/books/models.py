from django.db import models

class AuthorBiography(models.Model):
    author = models.OneToOneField(
        "books.Author", on_delete=models.CASCADE, related_name="biography", verbose_name="Автор"
    )
    biography = models.TextField(verbose_name="Биография")
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=False)
    date_of_death = models.DateField(verbose_name="Дата смерти", null=True, blank=True)

    class Meta:
        verbose_name = "Биография"
        verbose_name_plural = "Биографии"

    def __str__(self) -> str:
        return f"{self.author.name}"


class Author(models.Model):
    image = models.ImageField(verbose_name="Фото", upload_to="authors/", default="defaults/writer.webp", blank=True)
    name = models.CharField(verbose_name="ФИО", max_length=100)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self) -> str:
        return self.name
        

class Genre(models.Model):
    name = models.CharField(verbose_name="Жанр", max_length=30)
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="books", null=True, blank=True, verbose_name="Автор"
    )
    genres = models.ManyToManyField(
        Genre, related_name="books", verbose_name="Жанры"
    )
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание")
    publication_date = models.DateField(verbose_name="Дата публикации")
    uploaded_at = models.DateTimeField(verbose_name="Дата создания", auto_now=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self) -> str:
        return f"{self.name}"
