from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('movie/<int:movie_id>/bookmark/', views.bookmark_movie, name='bookmark_movie'),
]
