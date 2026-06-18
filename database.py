import sqlite3

# Create the database and table if they do not already exist
def create_database():

    # Connect to the database file
    # If it doesn't exist, SQLite creates it automatically
    conn = sqlite3.connect("giflibby.db")

    # Create a cursor object
    # Cursor is used to execute SQL commands
    cursor = conn.cursor()

    # Create gifs table if none exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gifs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        categories TEXT,
        tags TEXT
    )
    """)

    # Save changes
    conn.commit()
    # Close connection
    conn.close()

# Add a GIF to the database
def add_gif(name, path, categories, tags):

    # Connect to database
    conn = sqlite3.connect("giflibby.db")

    # Create cursor
    cursor = conn.cursor()

    # Insert a new row
    cursor.execute("""
    INSERT INTO gifs (name, path, categories, tags)
    VALUES (?, ?, ?, ?)
    """, (name, path, categories, tags))

    conn.commit()
    conn.close()

# Return every GIF in the database
def get_all_gifs():

    conn = sqlite3.connect("giflibby.db")

    cursor = conn.cursor()

    # Select every row
    cursor.execute("SELECT * FROM gifs")

    # Store results
    results = cursor.fetchall()

    conn.close()

    return results

# Search for GIFs containing a tag
def search_tags(tag):

    conn = sqlite3.connect("giflibby.db")

    cursor = conn.cursor()

    # Search tags column
    cursor.execute("""
    SELECT * FROM gifs
    WHERE tags LIKE ?
    """, (f"%{tag}%",))

    results = cursor.fetchall()

    conn.close()

    return results

# Search for GIFs belonging to a category
def search_category(category):

    conn = sqlite3.connect("giflibby.db")

    cursor = conn.cursor()

    # Search categories column
    cursor.execute("""
    SELECT * FROM gifs
    WHERE categories LIKE ?
    """, (f"%{category}%",))

    results = cursor.fetchall()

    conn.close()

    return results

# Delete a GIF using its ID
def delete_gif(gif_id):

    conn = sqlite3.connect("giflibby.db")

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM gifs
    WHERE id = ?
    """, (gif_id,))

    conn.commit()
    conn.close()