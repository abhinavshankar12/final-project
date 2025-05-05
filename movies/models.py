from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

# movie class for movie info
class Movie(models.Model):
    title = models.CharField(max_length=200) 
    genre = models.CharField(max_length=100)  
    release_year = models.IntegerField()  
    rating = models.DecimalField(max_digits=3, decimal_places=1)  
    description = models.TextField()  
    cast = models.TextField()  
    poster = models.CharField(max_length=255)  
    trailer = models.CharField(max_length=255, blank=True, null=True)  
    
    # returns movie name as a string
    def __str__(self):
        return self.title
    

#
# Keep track of who rented what
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who rented
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # which movie they got
    rental_date = models.DateTimeField(auto_now_add=True)  # when they rented it
    returned = models.BooleanField(default=False)  # did they return it yet?
    
    # print in admin panel
    def __str__(self):
        return self.user.username + " rented " + self.movie.title
    
    # add rental fee calculation later
    # def calculate_fee(self):


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @classmethod
    def get_user_cart(cls, user):
        cache_key = f'user_cart_{user.id}'
        cart = cache.get(cache_key)
        
        if cart is None:
            cart, created = cls.objects.get_or_create(user=user)
            cache.set(cache_key, cart, 60*30)  # Cache for 30 minutes
        
        return cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'movie')
    
    def __str__(self):
        return f"{self.movie.title} in {self.cart}"
