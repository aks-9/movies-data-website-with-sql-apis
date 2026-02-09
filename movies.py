import random
import movie_storage_sql as storage


def print_menu():
    """Display the main menu options."""
    print("\nMenu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"\n{len(movies)} movies in total")

    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    """Prompt the user and add a new movie to the database."""
    title = input("Enter new movie name: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    try:
        year = int(input("Enter movie year: "))
        rating = float(input("Enter movie rating: "))
    except ValueError:
        print("Year and rating must be numbers.")
        return

    storage.add_movie(title, year, rating)


def command_delete_movie():
    """Prompt the user and delete a movie from the database."""
    title = input("Enter movie name to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    storage.delete_movie(title)


def command_update_movie():
    """Prompt the user and update a movie's rating."""
    title = input("Enter movie name to update: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    try:
        rating = float(input("Enter new rating: "))
    except ValueError:
        print("Rating must be a number.")
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
    count = len(sorted_ratings)

    median = (
        sorted_ratings[count // 2]
        if count % 2 == 1
        else (sorted_ratings[count // 2 - 1] + sorted_ratings[count // 2]) / 2
    )

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
    """Display a random movie from the database."""
    movies = storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]

    print(f"{title} ({data['year']}): {data['rating']}")


def command_search_movie():
    """Search for movies by partial title match."""
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

    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def main():
    """Run the main menu loop."""
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
