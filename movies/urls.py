from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/rent/', views.rent_movie, name='rent_movie'),
    path('movie/<int:movie_id>/return/', views.return_movie, name='return_movie'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout_cart, name='checkout_cart'),
    path('register/', views.register, name='register'),
] 