from django.contrib import admin

# Register your models here.
from .models import Book, Author, Direction
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Direction)
