from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('genre/<slug:slug>/', views.GenreListView.as_view(), name='genre_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]