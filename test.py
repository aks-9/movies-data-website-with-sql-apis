from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie, clear_movies

# ------------------------------
# Clear existing movies before testing
# ------------------------------
clear_movies()

# ------------------------------
# Test adding a movie
# ------------------------------
print("Adding movie: Inception")
add_movie("Inception", 2010, 8.8, poster=None)

print("\nCurrent movies after adding Inception:")
movies = list_movies()
print(movies)

# ------------------------------
# Test adding another movie
# ------------------------------
print("\nAdding movie: Titanic")
add_movie("Titanic", 1997, 7.8)
print("\nCurrent movies after adding Titanic:")
print(list_movies())

# ------------------------------
# Test updating a movie's rating
# ------------------------------
print("\nUpdating Inception rating to 9.0")
update_movie("Inception", 9.0)
print("\nCurrent movies after update:")
print(list_movies())

# ------------------------------
# Test deleting a movie
# ------------------------------
print("\nDeleting movie: Inception")
delete_movie("Inception")
print("\nCurrent movies after deleting Inception:")
print(list_movies())

# ------------------------------
# Test deleting a movie that does not exist
# ------------------------------
print("\nTrying to delete a non-existing movie: Avatar")
deleted = delete_movie("Avatar")
print("Deleted:", deleted)
print(list_movies())

# ------------------------------
# Test updating a movie that does not exist
# ------------------------------
print("\nTrying to update a non-existing movie: Avatar")
updated = update_movie("Avatar", 8.0)
print("Updated:", updated)
print(list_movies())
