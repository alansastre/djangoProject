from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from .forms import DirectionForm
from .models import Book, Author, Direction, Genre, Biography
from django.utils import timezone


def home_redirect(request):
    return HttpResponseRedirect("/books")


# *************************** SIGN IN / SIGN UP  *******************

def do_login(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "accounts/login.html")

    login(request, user)
    return redirect('book_list')


def do_logout(request):
    logout(request)
    return redirect('login')


def do_register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    User.objects.create_user(username, email, password)

    return redirect('login')


# *************************** CRUD Books *******************
@login_required
def book_list(request):
    # if request.user.is_authenticated:
    #     # Do something for authenticated users.
    #     print("USUARIO AUTENTICADO")
    # else:
    #     # Do something for anonymous users.
    #     print("USUARIO NO AUTENTICADO")

    data = {
        "books": Book.objects.all(),  # recupera libros de db,
        "authors": Author.objects.all(),
        "genres": Genre.objects.all()
    }
    return render(request, "books/book-list.html", context=data)

@login_required
def book_new(request):
    data = {
        "authors": Author.objects.all(),
        "genres": Genre.objects.all()
    }
    return render(request, "books/book-edit.html", context=data)

@login_required
def book_load(request, id):
    data = {
        "book": Book.objects.get(id=id),  # recuperamos el libro, dentro tiene su propia lista de géneros
        "authors": Author.objects.all(),
        "genres": Genre.objects.all()  # todos los generos
    }
    return render(request, "books/book-edit.html", context=data)

@login_required
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

@login_required
def book_filter(request):
    author_id_str = request.GET.get("author_id")
    genres = request.GET.getlist("genres")
    author_id = int(author_id_str) if author_id_str else None

    books = None
    if author_id and len(genres) >= 1:
        books = Book.objects.filter(author_id=author_id, genres__id__in=genres).distinct()
    elif author_id:
        books = Book.objects.filter(author_id=author_id)
    elif len(genres) >= 1:
        books = Book.objects.filter(genres__id__in=genres).distinct()
    else:
        books = Book.objects.all()

    # FIX - no filtra bien:
    # filter_args = {}
    # if author_id:
    #     filter_args['author_id'] = author_id
    # if len(genres) > 1:
    #     filter_args['genres__id__in'] = genres
    #
    # books = Book.objects.filter(**filter_args).distinct()

    data = {
        "books": books,
        "authors": Author.objects.all(),
        "genres": Genre.objects.all(),
        # Seleccionados en el filtro
        "author_id": author_id,
        "genres_filtered": Genre.objects.filter(id__in=genres)
    }

    return render(request, "books/book-list.html", context=data)

@login_required
def book_view(request, id):
    book = Book.objects.get(id=id)
    data = {
        "book": book,
        "genres": book.genres.all()
    }
    return render(request, "books/book-view.html", context=data)

@login_required
def book_delete(request, pk):
    try:
        book1 = Book.objects.get(pk=pk)
        book1.delete()
        return HttpResponseRedirect("/books")
    except Book.DoesNotExist:
        return HttpResponseNotFound("Libro no encontrado")

@login_required
def book_delete_by_year(request, year):
    books = Book.objects.filter(year=year)
    result = books.delete()
    return HttpResponse("{} libro/s borrado/s correctamente.".format(result[0]))


# *************************** CRUD Authors *******************
@login_required
def author_list(request):
    data = {
        "authors": Author.objects.all()
    }
    return render(request, "authors/author-list.html", context=data)

@login_required
def author_view(request, id):
    data = {
        "author": Author.objects.get(id=id),
        # "books": Book.objects.filter(author_id=id)
        "books": Author.objects.get(id=id).book_set.all()
    }
    return render(request, "authors/author-view.html", context=data)

@login_required
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

@login_required
def author_new(request):
    data = {
        "directions": Direction.objects.exclude(author__isnull=False)
    }
    return render(request, "authors/author-edit.html", context=data)

@login_required
def author_load(request, id):
    data = {
        "author": Author.objects.get(id=id),
        "directions": Direction.objects.exclude(author__isnull=False)
    }
    return render(request, "authors/author-edit.html", context=data)

@login_required
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
@login_required
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

@login_required
def direction_new(request):
    form = DirectionForm()
    form['street'].label_tag(attrs={'class': 'form-label'})
    return render(request, "directions/direction-edit.html", {'form': form})

@login_required
def direction_view(request, pk):
    direction = Direction.objects.get(pk=pk)
    data = {
        "direction": direction,
    }
    return render(request, "directions/direction-view.html", context=data)

@login_required
def direction_save(request):

    form = DirectionForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect('/directions/new')

    # El formulario es válido
    direction = form.save()
    return redirect('direction_view', pk=direction.id)

@login_required
def direction_load(request, pk):
    direction = Direction.objects.get(pk=pk)

    if request.method == "GET":
        form = DirectionForm(instance=direction)
        return render(request, "directions/direction-edit.html", {"form": form})
    else:  # POST
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()

    return redirect('direction_view', pk=direction.id)


# **************** Vistas basadas en clase ****************

class DirectionListView(generic.ListView):
    model = Direction
    template_name = 'directions/direction-list.html'








