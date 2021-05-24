from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_redirect),

    # login
    path('accounts/login', views.do_login, name="login"),
    path('accounts/logout', views.do_logout, name="logout"),
    path('accounts/register', views.do_register, name="register"),


    # CRUD books
    path('books/', views.book_list, name="book_list"),
    path('books/new', views.book_new, name="book_new"),
    path('books/<int:id>/load', views.book_load, name="book_load"),
    path('books/filter/', views.book_filter, name="book_filter"),
    path('books/save', views.book_save, name="book_save"),
    path('books/<int:id>/view', views.book_view, name="book_view"),
    path('books/<int:pk>/delete', views.book_delete, name='book_delete'),
    path('books/<int:year>/delete/all', views.book_delete_by_year),

    # CRUD authors
    path('authors/', views.author_list, name="author_list"),
    path('authors/<int:id>/view', views.author_view, name="author_view"),
    path('authors/<int:pk>/delete', views.author_delete, name='author_delete'),
    path('authors/new', views.author_new, name="author_new"),
    path('authors/<int:id>/load', views.author_load, name="author_load"),
    path('authors/save', views.author_save, name="author_save"),

    # CRUD directions
    path('directions/<int:pk>/delete', views.direction_delete, name="direction_delete"),
    path('directions/new', views.direction_new, name="direction_new"),
    path('directions/save', views.direction_save, name="direction_save"),
    path('directions/<int:pk>/view', views.direction_view, name="direction_view"),
    path('directions/<int:pk>/load', views.direction_load, name="direction_load"),
    # url de tipo vista basada en clase
    path('directions/', views.DirectionListView.as_view(), name='direction_list'),
]
