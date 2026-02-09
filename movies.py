import random
import movie_storage_sql as storage
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
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
        print("OMDb API is not accessible. Check your internet connection.")
        return None

    if data.get("Response") == "False":
        print(f"Movie '{title}' not found in OMDb.")
        return None

    rating = float(data["imdbRating"]) if data.get("imdbRating") and data["imdbRating"] != "N/A" else 0.0

    return {
        "title": data["Title"],
        "year": int(data["Year"]),
        "rating": rating
    }


def print_menu():
    """Display main menu."""
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
        return  # Already printed error

    storage.add_movie(movie["title"], movie["year"], movie["rating"])


def command_delete_movie():
    """Delete a movie by title."""
    title = input("Enter movie title to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    storage.delete_movie(title)


def command_update_movie():
    """Update a movie's rating manually (optional)."""
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

    ratings = [data["rating"] for data in movies.values()]
    average = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    n = len(sorted_ratings)
    median = (sorted_ratings[n // 2] if n % 2 == 1
              else (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2)

    max_rating = max(ratings)
    min_rating = min(ratings)

    print(f"Average rating: {average:.2f}")
    print(f"Median rating: {median}")

    print("Best movie(s):")
    for title, data in movies.items():
        if data["rating"] == max_rating:
            print(f"{title}, {max_rating}")

    print("Worst movie(s):")
    for title, data in movies.items():
        if data["rating"] == min_rating:
            print(f"{title}, {min_rating}")


def command_random_movie():
    """Display a random movie."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]
    print(f"{title} ({data['year']}): {data['rating']}")


def command_search_movie():
    """Search movies by part of title."""
    movies = storage.list_movies()
    query = input("Enter part of movie name: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    found = False
    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True

    if not found:
        print("No movies found.")


def command_movies_sorted_by_rating():
    """Display movies sorted by rating (highest first)."""
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)

    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def main():
    """Main menu loop."""
    print("********** My Movies Database **********")

    while True:
        print_menu()
        choice = input("Enter choice (0-8): ").strip()

        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            command_list_movies()
        elif choice == "2":
            command_add_movie()
        elif choice == "3":
            command_delete_movie()
        elif choice == "4":
            command_update_movie()
        elif choice == "5":
            command_stats()
        elif choice == "6":
            command_random_movie()
        elif choice == "7":
            command_search_movie()
        elif choice == "8":
            command_movies_sorted_by_rating()
        else:
            print("Invalid choice. Enter a number between 0 and 8.")


if __name__ == "__main__":
    main()
