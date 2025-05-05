import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_catalog.settings')
django.setup()

from movies.models import Movie

# List of movies to add

movies = [
    {
        'title': 'The Shawshank Redemption',
        'genre': 'Drama',
        'release_year': 1994,
        'rating': 9.3,
        'poster': 'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg',
        'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.'
    },
    {
        'title': 'The Godfather',
        'genre': 'Crime, Drama',
        'release_year': 1972,
        'rating': 9.2,
        'poster': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
        'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'
    },
    {
        'title': 'Pulp Fiction',
        'genre': 'Crime, Drama',
        'release_year': 1994,
        'rating': 8.9,
        'poster': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
        'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.'
    },
    {
        'title': 'The Dark Knight',
        'genre': 'Action, Crime, Drama',
        'release_year': 2008,
        'rating': 9.0,
        'poster': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg',
        'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'
    },
    {
        'title': 'Fight Club',
        'genre': 'Drama',
        'release_year': 1999,
        'rating': 8.8,
        'poster': 'https://m.media-amazon.com/images/M/MV5BNDIzNDU0YzEtYzE5Ni00ZjlkLTk5ZjgtNjM3NWE4YzA3Nzk3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_.jpg',
        'description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.'
    }
]


# Add the movies to the database


for movie_data in movies:

    # Check if movie already exists
    if not Movie.objects.filter(title=movie_data['title']).exists():
        movie = Movie.objects.create(
            title=movie_data['title'],
            genre=movie_data['genre'],
            release_year=movie_data['release_year'],
            rating=movie_data['rating'],
            poster=movie_data['poster'],
            description=movie_data['description']
        )
        print(f"Added movie: {movie.title}")
    else:
        print(f"Movie already exists: {movie_data['title']}")

print("Script completed!") 