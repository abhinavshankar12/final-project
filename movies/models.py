from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField()
    cast = models.TextField()
    poster = models.CharField(max_length=255)
    trailer = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
