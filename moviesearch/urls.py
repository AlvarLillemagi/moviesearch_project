from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_movies, name='search_movies'),
    path('movie/<int:tmdb_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:tmdb_id>/add_bookmark/', views.add_bookmark, name='add_bookmark'),
    path('movie/<int:tmdb_id>/remove_bookmark/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
]
