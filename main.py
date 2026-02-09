import random
import os
import movie_storage.movie_storage_sql as storage
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


# ------------------------------
# User Management
# ------------------------------

def select_user():
    """Prompt user to select or create a profile."""
    while True:
        users = storage.get_users()
        print("\nWelcome to the Movie App! 🎬")
        print("Select a user:")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user['name']}")
        print(f"{len(users) + 1}. Create new user")
        print(f"{len(users) + 2}. Exit")

        choice = input("\nEnter choice: ").strip()
        
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= len(users):
                selected_user = users[choice_int - 1]
                print(f"\nWelcome back, {selected_user['name']}!")
                return selected_user['id']
            elif choice_int == len(users) + 1:
                new_name = input("Enter name for new user: ").strip()
                if new_name:
                    if storage.add_user(new_name):
                        print(f"User '{new_name}' created successfully.")
                    else:
                        print("User already exists or error occurred.")
                else:
                    print("Name cannot be empty.")
            elif choice_int == len(users) + 2:
                print("Bye!")
                exit()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")


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
    print("9. Generate website")
    print("10. Switch user")


# ------------------------------
# Movie Commands
# ------------------------------

def command_list_movies(user_id):
    movies = storage.list_movies(user_id)
    if not movies:
        print("No movies available.")
        return

    print(f"\n{len(movies)} movies in total")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie(user_id):
    if not API_KEY:
        print("OMDb API key not found. Please add it to .env")
        return

    title = input("Enter movie title: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    # Check if movie already exists for this user
    movies = storage.list_movies(user_id)
    if title in movies:
        print(f"Movie '{title}' already exists in your collection!")
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
        year_str = data["Year"]
        # Handle years like '2010–' or '2010–2015'
        year = int(year_str[:4])
        rating = float(data["imdbRating"]) if data["imdbRating"] != "N/A" else 0.0
    except Exception as e:
        print("Error parsing movie data:", e)
        return

    if storage.add_movie(user_id, movie_title, year, rating):
        print(f"Movie '{movie_title}' added successfully to your collection!")
    else:
        print(f"Failed to add '{movie_title}'.")


def command_delete_movie(user_id):
    title = input("Enter movie name to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    if storage.delete_movie(user_id, title):
        print(f"Movie '{title}' deleted successfully.")
    else:
        print("Movie not found in your collection.")


def command_update_movie(user_id):
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

    if storage.update_movie(user_id, title, rating):
        print(f"Movie '{title}' updated successfully.")
    else:
        print("Movie not found in your collection.")


def command_stats(user_id):
    movies = storage.list_movies(user_id)
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


def command_random_movie(user_id):
    movies = list(storage.list_movies(user_id).items())
    if not movies:
        print("No movies available.")
        return
    title, data = random.choice(movies)
    print(f"{title} ({data['year']}): {data['rating']}")


def command_search_movie(user_id):
    query = input("Enter part of movie name: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return

    movies = storage.list_movies(user_id)
    found = False
    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True

    if not found:
        print("No movies found.")


def command_movies_sorted_by_rating(user_id):
    movies = storage.list_movies(user_id)
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


# ------------------------------
# Generate Website
# ------------------------------

def generate_website(user_id):
    """Generate a static website (Username.html) from the current user's movies."""
    movies = storage.list_movies(user_id)
    user_name = storage.get_user_by_id(user_id)
    
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

    template = template.replace("__TEMPLATE_TITLE__", f"{user_name}'s Movies")

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

    # Write Username.html in root folder
    filename = f"{user_name}.html"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"Website '{filename}' was generated successfully.")
    except Exception as e:
        print(f"Error writing {filename}:", e)


# ------------------------------
# Main Menu
# ------------------------------

def main():
    print("********** My Movies Database **********")
    user_id = select_user()
    
    while True:
        print_menu()
        choice = input("Enter choice (0-10): ").strip()
        
        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            command_list_movies(user_id)
        elif choice == "2":
            command_add_movie(user_id)
        elif choice == "3":
            command_delete_movie(user_id)
        elif choice == "4":
            command_update_movie(user_id)
        elif choice == "5":
            command_stats(user_id)
        elif choice == "6":
            command_random_movie(user_id)
        elif choice == "7":
            command_search_movie(user_id)
        elif choice == "8":
            command_movies_sorted_by_rating(user_id)
        elif choice == "9":
            generate_website(user_id)
        elif choice == "10":
            user_id = select_user()
        else:
            print("Invalid choice. Enter a number between 0 and 10.")


if __name__ == "__main__":
    main()
