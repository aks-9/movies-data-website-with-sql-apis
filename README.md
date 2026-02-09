# 🎬 My Movies Database

A **Python movie database** that integrates with the **OMDb API**. Add movies by title, fetch **Title, Year, IMDb Rating**, and manage your collection with **CRUD operations** and statistics.

---

## Features

- Add movies using **OMDb API** (just by entering the title)  
- Store movies locally using **SQLite + SQLAlchemy**  
- List all movies with **year and rating**  
- Delete movies  
- Update movie ratings manually (optional)  
- Show **statistics** (average, median, best & worst movies)  
- Pick a **random movie**  
- Search by **partial title**  
- Sort movies by **rating**  

---

## Project Structure
```my-movies-app/
├─ main.py # Main menu-driven app
├─ movie_storage_sql.py # SQLAlchemy database storage
├─ test.py # Automated test script
├─ data/
│ └─ movies.db # SQLite database file
├─ _static/
│ ├─ index_template.html # HTML template
│ └─ style.css # CSS for website
├─ index.html # Generated website
├─ .env # OMDb API key (not committed)
├─ .env.example
└─ .gitignore



---

## Requirements

- Python 3.7+  
- Packages:

```bash
pip install sqlalchemy requests python-dotenv


##Setup

##Clone the repository:

git clone https://github.com/aks-9/movies-data-website-with-sql-apis.git
cd my-movies-app

##Create a .env file in the root folder (or copy .env.example):
OMDB_API_KEY=YOUR_API_KEY_HERE
Replace YOUR_API_KEY_HERE with your OMDb API key.
Get a free key at OMDb API
.


##Optional: Add .env and database file to .gitignore to keep your key safe:

.env
*.db

Running the App
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


Usage Examples
Add a Movie

Choose 2. Add movie (OMDb)

Enter: Inception
Movie 'Inception' added successfully.

List Movies

Choose 1. List movies
1 movies in total
Inception (2010): 8.8


Update Rating

Choose 4. Update movie rating

Enter movie title: Inception

Enter new rating: 9.0
Movie 'Inception' updated successfully.

Delete Movie

Choose 3. Delete movie

Enter movie title: Inception
Movie 'Inception' deleted successfully.


Testing

Run the automated test script:
python test.py


Adds multiple movies

Tests listing, updating, deleting

Handles errors when a movie is not found

Picks a random movie



Error Handling

Movie not found → prints a message and does not crash

API not accessible → prints a message if internet is down

Notes

Only Title, Year, and IMDb Rating are stored (no poster)

SQLite database movies.db is auto-generated

Manual rating update is optional since OMDb provides real data
