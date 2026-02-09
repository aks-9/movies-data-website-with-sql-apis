from movie_storage.movie_storage_sql import add_movie, list_movies, delete_movie, update_movie, add_user, get_users

# ------------------------------
# Test user creation
# ------------------------------
print("Testing add_user()")
add_user("TestUser")
users = get_users()
user_id = users[0]['id']
print(f"User created: {users[0]['name']} (ID: {user_id})")

# ------------------------------
# Test adding a movie
# ------------------------------
print("\nTesting add_movie()")
add_movie(user_id, "Inception", 2010, 8.8)
movies = list_movies(user_id)
print("After adding Inception:", movies)

# ------------------------------
# Test listing movies
# ------------------------------
print("\nTesting list_movies()")
print(list_movies(user_id))

# ------------------------------
# Test updating a movie's rating
# ------------------------------
print("\nTesting update_movie()")
update_movie(user_id, "Inception", 9.0)
print("After updating rating:", list_movies(user_id))

# ------------------------------
# Test deleting a movie
# ------------------------------
print("\nTesting delete_movie()")
delete_movie(user_id, "Inception")
print("After deleting Inception:", list_movies(user_id))
