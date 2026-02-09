import random
import movie_storage_sql

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
    movies = movie_storage.get_movies()
    print(f"\n{len(movies)} movies in total")
    for m in movies:
        print(f"{m['title']} ({m['year']}): {m['rating']}")

def add_movie():
    movies = movie_storage.get_movies()

    # Title input validation
    while True:
        title = input("Enter new movie name: ").strip()
        if not title:
            print("Movie title cannot be empty.")
            continue
        if any(m['title'].lower() == title.lower() for m in movies):
            print(f"Movie {title} already exists!")
            return
        break

    # Year input validation
    while True:
        try:
            year = int(input("Enter movie year: "))
            break
        except ValueError:
            print("Invalid year. Please enter a number.")

    # Rating input validation
    while True:
        try:
            rating = float(input("Enter movie rating: "))
            break
        except ValueError:
            print("Invalid rating. Please enter a number.")

    movie_storage.add_movie(title, year, rating)
    print(f"Movie {title} successfully added")

def delete_movie():
    title = input("Enter movie name to delete: ").strip()
    if not title:
        print("Movie title cannot be empty.")
        return
    if movie_storage.delete_movie(title):
        print(f"Movie {title} deleted!")
    else:
        print("Movie not found.")

def update_movie():
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

    if movie_storage.update_movie(title, rating):
        print("Movie updated!")
    else:
        print("Movie not found.")

def stats():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        return

    ratings = [m['rating'] for m in movies]
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
    for m in movies:
        if m['rating'] == max_rating:
            print(f"{m['title']}, {max_rating}")

    print("Worst movie(s):")
    for m in movies:
        if m['rating'] == min_rating:
            print(f"{m['title']}, {min_rating}")

def random_movie():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        return
    movie = random.choice(movies)
    print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

def search_movie():
    movies = movie_storage.get_movies()
    query = input("Enter part of movie name: ").strip().lower()
    if not query:
        print("Search query cannot be empty.")
        return
    found = False
    for m in movies:
        if query in m['title'].lower():
            print(f"{m['title']} ({m['year']}): {m['rating']}")
            found = True
    if not found:
        print("No movies found.")

def movies_sorted_by_rating():
    movies = movie_storage.get_movies()
    sorted_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)
    for m in sorted_movies:
        print(f"{m['title']} ({m['year']}): {m['rating']}")

def main():
    print("********** My Movies Database **********")

    while True:
        print_menu()
        choice = input("Enter choice (0-8): ").strip()
        if choice not in [str(i) for i in range(9)]:
            print("Invalid choice. Enter a number between 0 and 8.")
            continue

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

if __name__ == "__main__":
    main()
