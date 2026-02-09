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
18. **User Profiles**: Multiple users can have their own personalized movie collections.
19. **Generate a static website**: Create a personal website (e.g., `John.html`) with your movie details.

---

## Project Structure
```
12. Project- Movie/
├── main.py                 # Main menu-driven app
├── movie_storage/          # Package for storage files
│   ├── __init__.py
│   └── movie_storage_sql.py # SQL database storage with SQLAlchemy
├── test.py                 # Automated test script
├── data/
│   └── movies.db           # SQLite database file (auto-generated)
├── _static/
│   ├── index_template.html # HTML template
│   └── style.css           # CSS for website
├── index.html              # Generated website
├── .env                    # OMDb API key (not committed)
└── .gitignore
```

## Requirements

- Python 3.7+  
- Packages:
```bash
pip install sqlalchemy requests python-dotenv
```


## Setup

### Clone the repository:
```bash
git clone https://github.com/aks-9/movies-data-website-with-sql-apis.git
cd "12. Project- Movie"
```

### Create a .env file in the root folder:
```text
OMDB_API_KEY=YOUR_API_KEY_HERE
```
Replace `YOUR_API_KEY_HERE` with your OMDb API key.
Get a free key at [OMDb API](http://www.omdbapi.com/apikey.aspx).

### Optional: Add .env and database file to .gitignore:
```text
.env
*.db
```

## Running the App
```bash
python main.py
```

You will see the menu:
```text
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
9. Generate website
10. Switch user
Enter choice (0-10):
```

## Usage Examples
### Add a Movie
1. Choose **2. Add movie (OMDb)**
2. Enter: `Inception`
3. Movie 'Inception' added successfully.

### List Movies
1. Choose **1. List movies**
2. Output:
   ```text
   1 movies in total
   Inception (2010): 8.8
   ```

### Update Rating
1. Choose **4. Update movie rating**
2. Enter movie title: `Inception`
3. Enter new rating: `9.0`
4. Movie 'Inception' updated successfully.

### Delete Movie
1. Choose **3. Delete movie**
2. Enter movie title: `Inception`
3. Movie 'Inception' deleted successfully.

### Generate Website
1. Choose **9. Generate website**
2. Website was generated successfully.
3. Open `index.html` in your browser.

## Testing
Run the automated test script:
```bash
python test.py
```
The test script:
- Adds multiple movies
- Tests listing, updating, deleting
- Handles errors when a movie is not found
- Picks a random movie



Error Handling

- **Movie not found**: Prints a message and does not crash.
- **API not accessible**: Prints a message if the internet is down.

---

## Notes

- Only **Title, Year, and IMDb Rating** are stored in the database.
- SQLite database `movies.db` is auto-generated in the `data/` folder.
- Manual rating update is optional since OMDb provides real data.
