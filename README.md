My Movies Database

A Python-based movie database that integrates with the OMDb API. Add movies by title, fetch Title, Year, IMDb Rating, and manage your collection with CRUD operations and statistics.

Features

Add movies using OMDb API (title only)

Store movies locally using SQLite + SQLAlchemy

List all movies with year and rating

Delete movies

Update movie ratings manually

Show statistics (average, median, best & worst movies)

Random movie picker

Search by partial title

Sort movies by rating

Project Structure
my-movies-app/
├─ movies.py               # Main menu-driven app
├─ movie_storage_sql.py    # SQLAlchemy database storage
├─ .env                    # OMDb API key (not committed)
├─ .gitignore
├─ movies.db               # SQLite database file (generated automatically)

Requirements

Python 3.7+

Packages:

pip install sqlalchemy requests python-dotenv

Setup

Clone the repository:

git clone 
cd my-movies-app


Create a .env file in the root folder:

OMDB_API_KEY=your_api_key_here


Replace your_api_key_here with your OMDb API key.
Get a free key at OMDb API
.

Optional: Add .env and database to .gitignore to keep your key safe:

.env
*.db

How to Run
python movies.py


You will see the menu:

Menu:
0. Exit
1. List movies
2. Add movie (OMDb)
3. Delete movie
4. Update movie rating
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
Enter choice (0-8):

Usage Example
Add a movie:

Choose 2. Add movie (OMDb)

Enter: Inception

Movie 'Inception' added successfully.

List movies:

Choose 1. List movies

1 movies in total
Inception (2010): 8.8

Update rating:

Choose 4. Update movie rating

Enter movie title: Inception

Enter new rating: 9.0

Movie 'Inception' updated successfully.

Delete movie:

Choose 3. Delete movie

Enter movie title: Inception

Movie 'Inception' deleted successfully.

Notes

OMDb API errors: If the API is offline or the movie is not found, the program shows an appropriate message.

No poster stored: Only Title, Year, and IMDb Rating are saved.

Database: SQLite file movies.db is automatically created.

License

This project is MIT licensed.