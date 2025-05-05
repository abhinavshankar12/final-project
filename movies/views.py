from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Movie, Rental, Cart, CartItem
from django.core.cache import cache
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from .forms import UserRegistrationForm


# Home page

def home(request):
    all_movies = Movie.objects.all()
    
    user_search = request.GET.get('search', '')
    if user_search != '':
        all_movies = all_movies.filter(title__icontains=user_search)
    
    top_rated_movies = []
    for m in Movie.objects.all():
        if m.rating > 8:
            top_rated_movies.append(m)
    top_rated_movies.sort(key=lambda x: x.rating, reverse=True)
    
    current_year = timezone.now().year
    
    new_movies = []
    for m in Movie.objects.all():
        if m.release_year >= current_year - 5:
            new_movies.append(m)
    new_movies.sort(key=lambda x: x.release_year, reverse=True)
    
    user_rentals = []
    if request.user.is_authenticated:
        for r in Rental.objects.all():
            if r.user == request.user and r.returned == False:
                user_rentals.append(r.movie.id)
    
    my_context = {
        'movies': all_movies,
        'top_rated': top_rated_movies,
        'latest': new_movies,
        'search_query': user_search,
        'rented_movies': user_rentals,
    }
    
    return render(request, 'movies/home.html', my_context)



# Details on movies

def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except:
        return get_object_or_404(Movie, pk=movie_id)
    
    rented = False
    rented_by_me = False
    
    if request.user.is_authenticated:
        my_rentals = Rental.objects.filter(user=request.user, movie=movie, returned=False)
        if len(my_rentals) > 0:
            rented_by_me = True
        else:
            all_rentals = Rental.objects.filter(movie=movie, returned=False)
            if len(all_rentals) > 0:
                rented = True
    else:
        all_rentals = Rental.objects.filter(movie=movie, returned=False)
        if len(all_rentals) > 0:
            rented = True
    
    stuff_for_template = {
        'movie': movie,
        'is_rented': rented,
        'is_rented_by_user': rented_by_me,
    }
    
    return render(request, 'movies/movie_detail.html', stuff_for_template)

# Rent movie view

@login_required
def rent_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    rentals = Rental.objects.filter(movie=movie, returned=False)
    if len(rentals) > 0:
        return redirect('movie_detail', movie_id=movie_id)
    
    rental = Rental()
    rental.user = request.user
    rental.movie = movie
    rental.save()
    
    return redirect('movie_detail', movie_id=movie_id)

# Return movie
@login_required
def return_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    user_rentals = Rental.objects.filter(user=request.user, movie=movie, returned=False)
    if len(user_rentals) > 0:
        rental = user_rentals[0]
        rental.returned = True
        rental.save()
    
    return redirect('movie_detail', movie_id=movie_id)

# My rented movies view
@login_required
def my_rentals(request):
    user_rentals = Rental.objects.filter(user=request.user, returned=False)
    
    context = {
        'rentals': user_rentals,
    }
    
    return render(request, 'movies/my_rentals.html', context)

@login_required
def view_cart(request):
    """View the user's cart"""
    cart = Cart.get_user_cart(request.user)
    items = CartItem.objects.filter(cart=cart).select_related('movie')
    
    context = {
        'cart_items': items,
    }
    return render(request, 'movies/cart.html', context)

@login_required
def add_to_cart(request, movie_id):
    """Add a movie to the cart"""
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Check if movie is already rented
    if Rental.objects.filter(movie=movie, returned=False).exists():
        messages.error(request, "This movie is already rented by someone else.")
        return redirect('movie_detail', movie_id=movie_id)
    
    try:
        # Get or create user's cart
        cart = Cart.get_user_cart(request.user)
        
        # Add movie to cart if not already there
        cart_item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
        
        # Clear the cache to update it
        cache_key = f'user_cart_{request.user.id}'
        cache.delete(cache_key)
        
        if created:
            messages.success(request, f"{movie.title} added to your cart!")
        else:
            messages.info(request, f"{movie.title} is already in your cart.")
            
    except Exception as e:
        messages.error(request, f"Error adding movie to cart: {str(e)}")
        return redirect('movie_detail', movie_id=movie_id)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('movie_detail', movie_id=movie_id)


@login_required
def remove_from_cart(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    cart = Cart.get_user_cart(request.user)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, movie=movie)
        cart_item.delete()
        
        # Clear the cache to update it
        cache_key = f'user_cart_{request.user.id}'
        cache.delete(cache_key)
        
        messages.success(request, f"{movie.title} removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "This movie is not in your cart.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('view_cart')



@login_required
def checkout_cart(request):
    if request.method == 'POST':
        cart = Cart.get_user_cart(request.user)
        items = CartItem.objects.filter(cart=cart).select_related('movie')
        

        # Check if any movie is already rented
        
        already_rented = []
        for item in items:
            if Rental.objects.filter(movie=item.movie, returned=False).exists():
                already_rented.append(item.movie.title)
        
        if already_rented:
            messages.error(request, f"Cannot rent: {', '.join(already_rented)} already rented.")
            return redirect('view_cart')
        
      
        # Create rentals for all movies in cart
      
        for item in items:
            Rental.objects.create(user=request.user, movie=item.movie)
            item.delete()
        
       
        # Clear the cache
       
        cache_key = f'user_cart_{request.user.id}'
        cache.delete(cache_key)
        
        messages.success(request, "Successfully rented all movies in your cart!")
        return redirect('my_rentals')
    
    return redirect('view_cart')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Movie Catalog.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
