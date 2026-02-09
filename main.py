import random
import os
import movie_storage_sql as storage
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


# ------------------------------
# Menu
# ------------------------------

def print_menu():
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
    print("9. Generate website")  # New option


# ------------------------------
# Movie Commands
# ------------------------------

def command_list_movies():
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    print(f"\n{len(movies)} movies in total")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    if not API_KEY:
        print("OMDb API key not found. Please add it to .env")
        return

    title = input("Enter movie title: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    # Check if movie already exists
    movies = storage.list_movies()
    if title in movies:
        print(f"Movie '{title}' already exists!")
        return

    # Query OMDb API
    try:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("Error accessing OMDb API:", e)
        return

    # Handle errors from API
    if data.get("Response") == "False":
        print("Movie not found in OMDb.")
        return

    try:
        movie_title = data["Title"]
        year = int(data["Year"][:4])  # Some years like '2010–' may appear
        rating = float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0
    except Exception as e:
        print("Error parsing movie data:", e)
        return

    storage.add_movie(movie_title, year, rating)
    print(f"Movie '{movie_title}' added successfully.")


def command_delete_movie():
    title = input("Enter movie name to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    if storage.delete_movie(title):
        print(f"Movie '{title}' deleted successfully.")
    else:
        print("Movie not found.")


def command_update_movie():
    title = input("Enter movie name to update: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    while True:
        try:
            rating = float(input("Enter new rating: "))
            break
        except ValueError:
            print("Invalid rating. Please enter a number.")

    if storage.update_movie(title, rating):
        print(f"Movie '{title}' updated successfully.")
    else:
        print("Movie not found.")


def command_stats():
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    ratings = [data['rating'] for data in movies.values()]
    average = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    n = len(sorted_ratings)
    median = (sorted_ratings[n // 2] if n % 2 == 1
              else (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2)

    max_rating = max(ratings)
    min_rating = min(ratings)

    print(f"Average rating: {average:.2f}")
    print(f"Median rating: {median:.2f}")

    print("Best movie(s):")
    for title, data in movies.items():
        if data['rating'] == max_rating:
            print(f"{title}, {max_rating}")

    print("Worst movie(s):")
    for title, data in movies.items():
        if data['rating'] == min_rating:
            print(f"{title}, {min_rating}")


def command_random_movie():
    movies = list(storage.list_movies().items())
    if not movies:
        print("No movies available.")
        return
    title, data = random.choice(movies)
    print(f"{title} ({data['year']}): {data['rating']}")


def command_search_movie():
    query = input("Enter part of movie name: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    movies = storage.list_movies()
    found = False
    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True

    if not found:
        print("No movies found.")


def command_movies_sorted_by_rating():
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


# ------------------------------
# Generate Website
# ------------------------------

def generate_website():
    """Generate a static website (index.html) from the current movies."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available to generate website.")
        return

    template_path = os.path.join("_static", "index_template.html")
    if not os.path.exists(template_path):
        print(f"Template file '{template_path}' not found!")
        return

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    template = template.replace("__TEMPLATE_TITLE__", "My Movies Database")

    # Build movie grid
    movie_grid = ""
    for title, data in movies.items():
        movie_item = f"""
        <li class="movie">
            <div class="movie-title">{title}</div>
            <div class="movie-year">Year: {data['year']} | Rating: {data['rating']}</div>
        </li>
        """
        movie_grid += movie_item

    template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Write index.html in root folder
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(template)
        print("Website was generated successfully.")
    except Exception as e:
        print("Error writing index.html:", e)


# ------------------------------
# Main Menu
# ------------------------------

def main():
    print("********** My Movies Database **********")
    while True:
        print_menu()
        choice = input("Enter choice (0-9): ").strip()
        if choice not in [str(i) for i in range(10)]:
            print("Invalid choice. Enter a number between 0 and 9.")
            continue

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
        elif choice == "9":
            generate_website()


if __name__ == "__main__":
    main()
