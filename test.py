import movie_storage_sql as storage
from movies import fetch_movie

def clear_database():
    """Delete all movies from the database."""
    movies = list(storage.list_movies().keys())
    for title in movies:
        storage.delete_movie(title)

def test_add_movie(title):
    """Add a movie via OMDb API."""
    movie = fetch_movie(title)
    if movie:
        storage.add_movie(movie["title"], movie["year"], movie["rating"])

def test_list_movies():
    """List all movies in the database."""
    movies = storage.list_movies()
    print(f"\nListing {len(movies)} movies:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")

def test_update_movie(title, new_rating):
    """Update rating of a movie."""
    storage.update_movie(title, new_rating)

def test_delete_movie(title):
    """Delete a movie from database."""
    storage.delete_movie(title)

def run_tests():
    print("=== Clearing database ===")
    clear_database()

    print("\n=== Adding movies ===")
    test_add_movie("Inception")
    test_add_movie("The Dark Knight")
    test_add_movie("Jumanji")  # Older movie
    test_add_movie("NonExistentMovie123")  # Should fail

    test_list_movies()

    print("\n=== Updating movie rating ===")
    test_update_movie("Jumanji", 7.0)
    test_list_movies()

    print("\n=== Deleting a movie ===")
    test_delete_movie("Inception")
    test_list_movies()

    print("\n=== Random movie ===")
    movies = storage.list_movies()
    if movies:
        import random
        title = random.choice(list(movies.keys()))
        data = movies[title]
        print(f"Random movie: {title} ({data['year']}): {data['rating']}")
    else:
        print("No movies left in database.")

if __name__ == "__main__":
    run_tests()
