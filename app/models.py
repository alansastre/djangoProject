from django.db import models
from django.utils import timezone


class Direction(models.Model):
    street = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = "directions"

    def __str__(self):
        return self.street + " - " + self.country


class Biography(models.Model):
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = "biographies"

    def __str__(self):
        return self.description


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=False, default="support@library.com")
    num_books = models.IntegerField(default=1)
    creation_date = models.DateTimeField(default=timezone.now)
    married = models.BooleanField(default=False)
    salary = models.FloatField(default=0)

    direction = models.OneToOneField(Direction, on_delete=models.CASCADE, null=True, blank=True)
    biography = models.OneToOneField(Biography, on_delete=models.SET_NULL, null=True, blank=True)

    # FIX objects error with this:
    # objects = models.Manager()

    class Meta:
        db_table = "authors"

    def __str__(self):
        return self.first_name + " - " + self.last_name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    class Meta:
        db_table = "genres"

    def __str__(self):
        return self.name + " - " + self.color

# class Editorial(models.Model):
#     pass
# class Library(models.Model):
#     pass
# class LibraryAddress(models.Model):
#     pass

class Book(models.Model):
    # attributes
    isbn = models.CharField(max_length=40)
    title = models.CharField(max_length=150)
    year = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    # relationships
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)  # Many To One
    genres = models.ManyToManyField(Genre)

    class Meta:
        db_table = "books"

    def __str__(self):
        return self.isbn + " - " + self.title