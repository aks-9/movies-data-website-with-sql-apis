import random
import movie_storage_sql as movie_storage


def print_menu():
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


def list_movies():
    movies = movie_storage.list_movies()

    print(f"\n{len(movies)} movies in total")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def add_movie():
    # Title input
    title = input("Enter new movie name: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    # Year input
    try:
        year = int(input("Enter movie year: "))
    except ValueError:
        print("Invalid year.")
        return

    # Rating input
    try:
        rating = float(input("Enter movie rating: "))
    except ValueError:
        print("Invalid rating.")
        return

    movie_storage.add_movie(title, year, rating)


def delete_movie():
    title = input("Enter movie name to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    movie_storage.delete_movie(title)


def update_movie():
    title = input("Enter movie name to update: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return

    try:
        rating = float(input("Enter new rating: "))
    except ValueError:
        print("Invalid rating.")
        return

    movie_storage.update_movie(title, rating)


def stats():
    movies = movie_storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    ratings = [data["rating"] for data in movies.values()]

    average = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    n = len(sorted_ratings)

    median = (
        sorted_ratings[n // 2]
        if n % 2 == 1
        else (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
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


def random_movie():
    movies = movie_storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]

    print(f"{title} ({data['year']}): {data['rating']}")


def search_movie():
    movies = movie_storage.list_movies()

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


def movies_sorted_by_rating():
    movies = movie_storage.list_movies()

    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def main():
    print("********** My Movies Database **********")

    while True:
        print_menu()
        choice = input("Enter choice (0-8): ").strip()

        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            movies_sorted_by_rating()
        else:
            print("Invalid choice. Enter a number between 0 and 8.")


if __name__ == "__main__":
    main()
