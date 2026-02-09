from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie


# ------------------------------
# Test adding a movie
# ------------------------------
print("Testing add_movie()")
add_movie("Inception", 2010, 8.8)
movies = list_movies()
print("After adding Inception:", movies)

# ------------------------------
# Test listing movies
# ------------------------------
print("\nTesting list_movies()")
print(list_movies())

# ------------------------------
# Test updating a movie's rating
# ------------------------------
print("\nTesting update_movie()")
update_movie("Inception", 9.0)
print("After updating rating:", list_movies())

# ------------------------------
# Test deleting a movie
# ------------------------------
print("\nTesting delete_movie()")
delete_movie("Inception")
print("After deleting Inception:", list_movies())  # Should be empty if it was the only movie
