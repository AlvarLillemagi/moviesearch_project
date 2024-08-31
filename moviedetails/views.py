import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.conf import settings
from moviesearch.models import Bookmark
from django.contrib.auth.decorators import login_required
from django.contrib import messages

TMDB_API_KEY = settings.TMDB_API_KEY

def movie_details(request, movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}', 
        params={'api_key': TMDB_API_KEY}
    )

    if response.status_code == 200:
        movie = response.json()
        context = {
            'title': movie['title'],
            'year': movie['release_date'][:4],
            'genre': ', '.join([genre['name'] for genre in movie.get('genres', [])]),
            'overview': movie.get('overview', 'No overview available.'),
            'cast': [cast_member['name'] for cast_member in movie.get('credits', {}).get('cast', [])[:5]],
            'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}",
            'movie_id': movie_id
        }
        return render(request, 'moviesearch/movie_details.html', context)
    else:
        raise Http404("Movie not found")

@login_required
def bookmark_movie(request, movie_id):
    user = request.user

    bookmark, created = Bookmark.objects.get_or_create(
        user=user,
        movie_id=movie_id
    )

    if created:
        messages.success(request, "Movie bookmarked successfully!")
    else:
        messages.info(request, "Movie was already bookmarked.")

    return redirect('movie_details', movie_id=movie_id)
