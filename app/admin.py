from django.contrib import admin

# Register your models here.
from .models import Book, Author, Direction, Biography, Genre
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Direction)
admin.site.register(Biography)
admin.site.register(Genre)
