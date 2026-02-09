import random
import movie_storage_sql as storage
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get OMDb API key from environment
API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

if not API_KEY:
    raise ValueError("OMDB_API_KEY is not set in .env file")


def fetch_movie(title):
    """Fetch movie info from OMDb API by title."""
    params = {"apikey": API_KEY, "t": title}

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()
    except requests.RequestException:
        print("OMDb API is not accessible.")
        return None

    if data.get("Response") == "False":
        return None

    # Handle missing or "N/A" rating
    rating = float(data["imdbRating"]) if data.get("imdbRating") and data["imdbRating"] != "N/A" else 0.0

    return {
        "title": data["Title"],
        "year": int(data["Year"]),
        "rating": rating
    }


def print_menu():
    """Display the main menu."""
    print("\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie (OMDb)")
    print("3. Delete movie")
    print("4. Update movie rating")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")


def command_list_movies():
    """Display all movies."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")

    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    """Add a movie using OMDb API by entering only the title."""
    title_input = input("Enter movie title: ").strip()
    if not title_input:
        print("Movie title cannot be empty.")
        return

    movie = fetch_movie(title_input)
    if movie is None:
        print("Movie not found in OMDb.")
        return

    storage.add_movie(movie["title"], movie["year"], movie["rating"])


def command_delete_movie():
    """Delete a movie by title."""
    title = input("Enter movie title to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    storage.delete_movie(title)


def command_update_movie():
    """Update a movie's rating."""
    title = input("Enter movie title to update: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    try:
        rating = float(input("Enter new rating: "))
    except ValueError:
        print("Invalid rating. Must be a number.")
        return

    storage.update_movie(title, rating)


def command_stats():
    """Display statistics about movie ratings."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    ra
