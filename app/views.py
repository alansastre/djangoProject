from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from .models import Book, Author, Direction, Genre, Biography
from django.utils import timezone


def home_redirect(request):
    return HttpResponseRedirect("/books")


# *************************** SIGN IN / SIGN UP  *******************

def sign_in(request):
    pass


def sign_up(request):
    pass


def logout(request):
    pass

# *************************** CRUD Books *******************
def book_list(request):
    data = {
        "books": Book.objects.all(),  # recupera libros de db,
        "authors": Author.objects.all(),
        "notification": "Listado de libros",
        "admin": False
    }
    return render(request, "books/book-list.html", context=data)


def book_new(request):
    data = {
        "authors": Author.objects.all(),
        "genres": Genre.objects.all()
    }
    return render(request, "books/book-edit.html", context=data)


def book_load(request, id):
    data = {
        "book": Book.objects.get(id=id),  # recuperamos el libro, dentro tiene su propia lista de géneros
        "authors": Author.objects.all(),
        "genres": Genre.objects.all()  # todos los generos
    }
    return render(request, "books/book-edit.html", context=data)


def book_save(request):
    creation = not request.POST.get("id")
    genres = request.POST.getlist('genres')

    author_id_str = request.POST.get("author_id")
    author_id = int(author_id_str) if author_id_str else None

    if creation:
        book = Book.objects.create(
            isbn=request.POST.get("isbn"),
            title=request.POST.get("title"),
            year=int(request.POST.get("year")),
            published=bool(request.POST.get("published")),
            author_id=author_id
        )
        book.genres.set(genres)
    else:
        # Editar un libro existente
        id_book = int(request.POST.get("id"))
        book = Book.objects.get(id=id_book)

        book.isbn = request.POST.get("isbn")
        book.title = request.POST.get("title")
        book.year = int(request.POST.get("year"))
        book.published = bool(request.POST.get("published"))
        book.author_id = author_id
        book.genres.set(genres)

        book.save()
    return HttpResponseRedirect("/books/{}/view".format(book.id))


def book_author_filter(request):
    author_id_str = request.GET.get("author_id")
    author_id = int(author_id_str) if author_id_str else None
    if author_id:
        data = {
            "books": Book.objects.filter(author_id=author_id),
            "authors": Author.objects.all(),
            "author_id": author_id
        }
        return render(request, "books/book-list.html", context=data)
    return HttpResponseRedirect("/books")


def book_filter(request, isbn):
    print(isbn)
    result = Book.objects.filter(isbn=isbn)
    print(result)
    return HttpResponse(result)


def book_view(request, id):
    book = Book.objects.get(id=id)
    data = {
        "book": book,
        "genres": book.genres.all()
    }
    return render(request, "books/book-view.html", context=data)


def book_delete(request, pk):
    try:
        book1 = Book.objects.get(pk=pk)
        book1.delete()
        return HttpResponseRedirect("/books")
    except Book.DoesNotExist:
        return HttpResponseNotFound("Libro no encontrado")


def book_delete_by_year(request, year):
    books = Book.objects.filter(year=year)
    result = books.delete()
    return HttpResponse("{} libro/s borrado/s correctamente.".format(result[0]))


# *************************** CRUD Authors *******************

def author_list(request):
    data = {
        "authors": Author.objects.all()
    }
    return render(request, "authors/author-list.html", context=data)


def author_view(request, id):
    data = {
        "author": Author.objects.get(id=id),
        # "books": Book.objects.filter(author_id=id)
        "books": Author.objects.get(id=id).book_set.all()
    }
    return render(request, "authors/author-view.html", context=data)


def author_delete(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        author.delete()
        return HttpResponseRedirect("/authors")
    except Author.DoesNotExist:
        data = {
            "error": "Autor no encontrado"
        }
        return render(request, "layout/notfound-404.html", context=data)


def author_new(request):
    data = {
        "directions": Direction.objects.exclude(author__isnull=False)
    }
    return render(request, "authors/author-edit.html", context=data)


def author_load(request, id):
    data = {
        "author": Author.objects.get(id=id),
        "directions": Direction.objects.exclude(author__isnull=False)
    }
    return render(request, "authors/author-edit.html", context=data)


def author_save(request):
    creation = not request.POST.get("id")

    # Extraer la dirección del selector HTML: puede ser None o un id de dirección
    direction_id_str = request.POST.get("direction_id")
    direction_id = int(direction_id_str) if direction_id_str else None

    # Extraer datos de la biografia
    year = int(request.POST.get("year")) if request.POST.get("year") else None
    description = request.POST.get("description")

    if creation:

        biography = None
        if description and year:
            biography = Biography.objects.create(year=year, description=description)

        author = Author.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            num_books=int(request.POST.get("num_books")),
            creation_date=timezone.now(),
            married=bool(request.POST.get("married")),
            salary=float(request.POST.get("salary")),
            direction_id=direction_id,  # Se asocia la dirección
            biography_id=biography.id if biography else None
        )

    else:
        id_author = int(request.POST.get("id"))
        author = Author.objects.get(id=id_author)
        # Atributos
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.email = request.POST.get("email")
        author.num_books = int(request.POST.get("num_books"))
        author.married = bool(request.POST.get("married"))
        author.salary = float(request.POST.get("salary"))
        # Asociaciones
        author.direction_id = direction_id
        if author.biography_id:  # Editar biografia
            author.biography.year = year
            author.biography.description = description
            author.biography.save()
        elif description and year:  # Crear biografia
            biography = Biography.objects.create(year=year, description=description)
            author.biography_id = biography.id

        author.save()

    return HttpResponseRedirect("/authors/{}/view".format(author.id))


# ******************* CRUD Directions *************************

def direction_delete(request, pk):
    try:
        direction = Direction.objects.get(pk=pk)
        direction.delete()
        return HttpResponseRedirect("/authors")
    except Direction.DoesNotExist:
        data = {
            "error": "Direccion no encontrada"
        }
        return render(request, "layout/notfound-404.html", context=data)
