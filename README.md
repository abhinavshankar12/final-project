# Movie Catalog Application

A Django-based web application for browsing, searching, and renting movies.

## Features

- Browse movies with poster images, titles, genres, release years, and ratings
- Search for movies by title
- Filter movies by genre, release year, and rating
- Sort movies by rating, release year, or alphabetically
- View movie details including description, cast, and trailer
- User authentication (login/logout)
- Rent and return movies
- Keep track of your rented movies

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/movie-catalog.git
cd movie-catalog
```

2. Install requirements:
```
pip install django
```

3. Run migrations:
```
python manage.py migrate
```

4. Load sample data:
```
python manage.py loaddata movies.json
```

5. Create a superuser (admin):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

### Usage

1. Browse movies on the home page
2. Use search bar to find movies by title
3. Filter movies using the dropdown menus
4. Click on a movie to view its details
5. Login to rent a movie
6. View your rented movies in the "My Rentals" section
7. Return a movie when you're done with it

## Admin Access

- Access the admin panel at http://127.0.0.1:8000/admin/
- Use the superuser credentials created in the setup steps
- Add, edit, or delete movies and manage rentals 