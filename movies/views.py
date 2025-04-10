from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Movie, Rental

# Home page view
def home(request):
    # Get all movies
    movies = Movie.objects.all()
    
    # Get search query
    search_query = request.GET.get('search', '')
    if search_query:
        movies = movies.filter(title__icontains=search_query)
    
    # Get filter parameters
    genre = request.GET.get('genre', '')
    year = request.GET.get('year', '')
    rating = request.GET.get('rating', '')
    
    # Apply filters
    if genre:
        movies = movies.filter(genre__icontains=genre)
    if year:
        movies = movies.filter(release_year=year)
    if rating:
        movies = movies.filter(rating__gte=rating)
    
    # Get sort parameter
    sort = request.GET.get('sort', '')
    if sort == 'rating':
        movies = movies.order_by('-rating')
    elif sort == 'year':
        movies = movies.order_by('-release_year')
    elif sort == 'a-z':
        movies = movies.order_by('title')
    
    # Get top rated movies (rating > 8.0)
    top_rated = Movie.objects.filter(rating__gt=8.0).order_by('-rating')
    
    # Get latest movies (released in the last 5 years)
    current_year = timezone.now().year
    latest = Movie.objects.filter(release_year__gte=current_year-5).order_by('-release_year')
    
    # Get unique genres and years for filter dropdowns
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    # Get rented movies
    rented_movies = []
    if request.user.is_authenticated:
        rented_movies = Rental.objects.filter(user=request.user, returned=False).values_list('movie_id', flat=True)
    
    context = {
        'movies': movies,
        'top_rated': top_rated,
        'latest': latest,
        'genres': genres,
        'years': years,
        'search_query': search_query,
        'selected_genre': genre,
        'selected_year': year,
        'selected_rating': rating,
        'selected_sort': sort,
        'rented_movies': rented_movies,
    }
    
    return render(request, 'movies/home.html', context)

# Movie details view
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Check if movie is rented
    is_rented = False
    is_rented_by_user = False
    
    if request.user.is_authenticated:
        user_rental = Rental.objects.filter(movie=movie, user=request.user, returned=False).first()
        if user_rental:
            is_rented_by_user = True
        else:
            is_rented = Rental.objects.filter(movie=movie, returned=False).exists()
    else:
        is_rented = Rental.objects.filter(movie=movie, returned=False).exists()
    
    context = {
        'movie': movie,
        'is_rented': is_rented,
        'is_rented_by_user': is_rented_by_user,
    }
    
    return render(request, 'movies/movie_detail.html', context)

# Rent movie view
@login_required
def rent_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Check if movie is already rented
    if Rental.objects.filter(movie=movie, returned=False).exists():
        return redirect('movie_detail', movie_id=movie_id)
    
    # Create rental
    Rental.objects.create(user=request.user, movie=movie)
    
    return redirect('movie_detail', movie_id=movie_id)

# Return movie view
@login_required
def return_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Get user's rental for this movie
    rental = Rental.objects.filter(user=request.user, movie=movie, returned=False).first()
    
    if rental:
        rental.returned = True
        rental.save()
    
    return redirect('movie_detail', movie_id=movie_id)

# My rented movies view
@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user, returned=False)
    context = {
        'rentals': rentals,
    }
    return render(request, 'movies/my_rentals.html', context)
