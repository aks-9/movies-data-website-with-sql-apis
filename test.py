import movie_storage_sql as storage

# Clear database first (optional)
for title in list(storage.list_movies().keys()):
    storage.delete_movie(title)

# Add movies
storage.add_movie("Inception", 2010, 8.8)
storage.add_movie("The Dark Knight", 2008, 9.0)
storage.add_movie("Jumanji", 1995, 6.5)

# List movies
print(storage.list_movies())

# Update rating
storage.update_movie("Jumanji", 7.0)
print(storage.list_movies())

# Delete movie
storage.delete_movie("Inception")
print(storage.list_movies())
