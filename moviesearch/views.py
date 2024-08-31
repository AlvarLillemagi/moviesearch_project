import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Movie, Bookmark
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def search_movies(request):
    query = request.GET.get('query', '')
    movies = []
    if query:
        url = f'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': settings.TMDB_API_KEY,
            'query': query,
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
        else:
            messages.error(request, 'Error fetching data from TMDB.')
    context = {
        'movies': movies,
        'query': query
    }
    return render(request, 'moviesearch/search_results.html', context)

def movie_detail(request, tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movie = response.json()
        is_bookmarked = Bookmark.objects.filter(user=request.user, movie__tmdb_id=tmdb_id).exists()

        if request.method == 'POST':
            if 'add_bookmark' in request.POST:
                movie_obj, created = Movie.objects.get_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'title': movie['title'],
                        'overview': movie['overview'],
                        'release_date': movie['release_date'],
                        'poster_path': movie['poster_path']
                    }
                )
                if not is_bookmarked:
                    Bookmark.objects.create(user=request.user, movie=movie_obj)
                    messages.success(request, 'Movie added to bookmarks.')
                else:
                    messages.info(request, 'Movie is already bookmarked.')

                return redirect('movie_detail', tmdb_id=tmdb_id)

            elif 'remove_bookmark' in request.POST:
                if is_bookmarked:
                    Bookmark.objects.filter(user=request.user, movie__tmdb_id=tmdb_id).delete()
                    messages.success(request, 'Movie removed from bookmarks.')
                else:
                    messages.info(request, 'Movie was not bookmarked.')

                return redirect('movie_detail', tmdb_id=tmdb_id)

        context = {
            'movie': movie,
            'is_bookmarked': is_bookmarked
        }
        return render(request, 'moviesearch/movie_detail.html', context)
    else:
        messages.error(request, 'Error fetching movie details from TMDB.')
        return redirect('search_movies')

@login_required
def add_bookmark(request, tmdb_id):
    if request.method == 'POST':
        url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movie, created = Movie.objects.get_or_create(
                tmdb_id=tmdb_id,
                defaults={
                    'title': data.get('title'),
                    'overview': data.get('overview'),
                    'release_date': data.get('release_date'),
                    'poster_path': data.get('poster_path')
                }
            )
            if created:
                Bookmark.objects.create(user=request.user, movie=movie)
                messages.success(request, f'"{movie.title}" has been added to bookmarks.')
            else:
                messages.info(request, f'"{movie.title}" is already in bookmarks.')
        else:
            messages.error(request, 'Error fetching movie details from TMDB.')
    return redirect('movie_detail', tmdb_id=tmdb_id)

@login_required
def remove_bookmark(request, tmdb_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
        Bookmark.objects.filter(user=request.user, movie=movie).delete()
        messages.success(request, f'"{movie.title}" has been removed from bookmarks.')
    return redirect('movie_detail', tmdb_id=tmdb_id)

@login_required
def bookmarks(request):
    bookmarked_movies = Bookmark.objects.filter(user=request.user).select_related('movie')
    context = {
        'bookmarked_movies': [bookmark.movie for bookmark in bookmarked_movies]
    }
    return render(request, 'moviesearch/bookmarks.html', context)

@login_required
def profile_detail(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        if hasattr(user, 'profile'):
            user.profile.biography = request.POST.get('biography', user.profile.biography)
            user.profile.date_of_birth = request.POST.get('date_of_birth', user.profile.date_of_birth)
            if 'profile_picture' in request.FILES:
                user.profile.profile_picture = request.FILES['profile_picture']
            user.profile.save()
        user.save()

        messages.success(request, 'Your profile has been updated.')
        return redirect('profile_detail')

    return render(request, 'userprofiles/profile_detail.html', {'user': user})

def csrf_failure(request, reason=""):
    return render(request, 'moviesearch/csrf_failure.html', {'reason': reason})
