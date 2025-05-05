from django.contrib import admin
from .models import Movie, Rental, Cart, CartItem

# Register your models here.
admin.site.register(Movie)
admin.site.register(Rental)
admin.site.register(Cart)
admin.site.register(CartItem)
