from sqlalchemy import create_engine, text
import os

# ------------------------------
# Ensure data folder exists
# ------------------------------
if not os.path.exists("data"):
    os.makedirs("data")

# ------------------------------
# Database URL
# ------------------------------
DB_PATH = os.path.join("data", "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"

# Create SQLAlchemy engine
engine = create_engine(DB_URL, echo=False)  # echo=True prints all SQL statements for debugging

# ------------------------------
# Create tables if not exist
# ------------------------------
with engine.connect() as connection:
    # Create users table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))
    
    # Create movies table with user_id
    # We use a combined unique constraint to allow different users to have the same movie
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, title)
        )
    """))
    connection.commit()


# ------------------------------
# User Functions
# ------------------------------

def get_users():
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        return [{"id": row[0], "name": row[1]} for row in result.fetchall()]


def add_user(name):
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": name}
            )
            connection.commit()
            return True
        except Exception as e:
            print(f"Error adding user '{name}': {e}")
            return False


def get_user_by_id(user_id):
    """Get user name by ID."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT name FROM users WHERE id = :id"),
            {"id": user_id}
        )
        row = result.fetchone()
        return row[0] if row else None


# ------------------------------
# CRUD Functions (User-Aware)
# ------------------------------

def list_movies(user_id):
    """Retrieve all movies for a specific user."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating FROM movies WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(user_id, title, year, rating):
    """Add a new movie for a specific user."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (user_id, title, year, rating) 
                    VALUES (:user_id, :title, :year, :rating)
                """),
                {"user_id": user_id, "title": title, "year": year, "rating": rating}
            )
            connection.commit()
            return True
        except Exception as e:
            print(f"Error adding movie '{title}': {e}")
            return False


def delete_movie(user_id, title):
    """Delete a movie for a specific user."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE user_id = :user_id AND title = :title"),
            {"user_id": user_id, "title": title}
        )
        connection.commit()
        return result.rowcount > 0


def update_movie(user_id, title, rating):
    """Update a movie's rating for a specific user."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE user_id = :user_id AND title = :title"),
            {"user_id": user_id, "title": title, "rating": rating}
        )
        connection.commit()
        return result.rowcount > 0
