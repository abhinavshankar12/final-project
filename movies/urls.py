from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/rent/', views.rent_movie, name='rent_movie'),
    path('movie/<int:movie_id>/return/', views.return_movie, name='return_movie'),
    path('my-rentals/', views.my_rentals, name='my_rentals'),
] 