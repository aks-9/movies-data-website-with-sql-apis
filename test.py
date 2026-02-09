from movie_storage.movie_storage_sql import add_movie, list_movies, delete_movie, update_movie, add_user, get_users, get_user_by_id
import os

# ------------------------------
# Setup for testing
# ------------------------------
print("--- Starting Automated Tests ---")

# ------------------------------
# Test user management
# ------------------------------
print("\n[1] Testing User Management")
test_name = "AutomatedTestUser"
add_user(test_name)
users = get_users()
test_user = next((u for u in users if u['name'] == test_name), None)

if test_user:
    user_id = test_user['id']
    print(f"SUCCESS: User '{test_name}' found with ID: {user_id}")
    
    fetched_name = get_user_by_id(user_id)
    print(f"SUCCESS: get_user_by_id({user_id}) returned '{fetched_name}'")
else:
    print(f"FAILURE: User '{test_name}' not found after add_user()")
    exit(1)

# ------------------------------
# Test CRUD (User-Aware)
# ------------------------------
print("\n[2] Testing CRUD Operations for User ID:", user_id)

# Add
print("Adding 'The Matrix'...")
add_movie(user_id, "The Matrix", 1999, 8.7)
movies = list_movies(user_id)
if "The Matrix" in movies:
    print("SUCCESS: Movie added and listed.")
else:
    print("FAILURE: Movie not found in list.")

# Update
print("Updating rating for 'The Matrix' to 9.5...")
update_movie(user_id, "The Matrix", 9.5)
movies = list_movies(user_id)
if movies["The Matrix"]["rating"] == 9.5:
    print("SUCCESS: Movie rating updated.")
else:
    print("FAILURE: Movie rating not updated.")

# Delete
print("Deleting 'The Matrix'...")
delete_movie(user_id, "The Matrix")
movies = list_movies(user_id)
if "The Matrix" not in movies:
    print("SUCCESS: Movie deleted.")
else:
    print("FAILURE: Movie still exists.")

# ------------------------------
# Test Multi-User Separation
# ------------------------------
print("\n[3] Testing Multi-User Separation")
user2_name = "User2_Test"
add_user(user2_name)
users = get_users()
user2 = next((u for u in users if u['name'] == user2_name), None)
user2_id = user2['id']

print(f"Adding 'Avatar' to {test_name}...")
add_movie(user_id, "Avatar", 2009, 7.9)

print(f"Adding 'Avatar' to {user2_name}...")
add_movie(user2_id, "Avatar", 2009, 8.5)

user1_movies = list_movies(user_id)
user2_movies = list_movies(user2_id)

print(f"{test_name} Avatar rating: {user1_movies['Avatar']['rating']}")
print(f"{user2_name} Avatar rating: {user2_movies['Avatar']['rating']}")

if user1_movies['Avatar']['rating'] != user2_movies['Avatar']['rating']:
    print("SUCCESS: Users have separate collections even for the same movie title.")
else:
    print("FAILURE: Collections are not separate.")

# Cleanup for rerun-ability (optional but good for this script)
delete_movie(user_id, "Avatar")
delete_movie(user2_id, "Avatar")

print("\n--- All Tests Completed Successfully ---")
