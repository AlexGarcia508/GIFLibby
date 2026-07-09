import sqlite3

DATABASE_NAME = "giflibby.db"

# Get database connection
def get_connection():
    return sqlite3.connect(DATABASE_NAME)

# Create database tables
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gifs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        preview_path TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gif_collections (
        gif_id INTEGER NOT NULL,
        collection_id INTEGER NOT NULL,
        PRIMARY KEY (gif_id, collection_id),
        FOREIGN KEY (gif_id) REFERENCES gifs(id),
        FOREIGN KEY (collection_id) REFERENCES collections(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gif_tags (
        gif_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (gif_id, tag_id),
        FOREIGN KEY (gif_id) REFERENCES gifs(id),
        FOREIGN KEY (tag_id) REFERENCES tags(id)
    )
    """)

    conn.commit()
    conn.close()

# Get or create collection
def get_or_create_collection(cursor, name):

    cursor.execute("""
    INSERT OR IGNORE INTO collections (name)
    VALUES (?)
    """, (name,))

    cursor.execute("""
    SELECT id FROM collections
    WHERE name = ?
    """, (name,))

    return cursor.fetchone()[0]

# Get or create tag
def get_or_create_tag(cursor, name):

    cursor.execute("""
    INSERT OR IGNORE INTO tags (name)
    VALUES (?)
    """, (name,))

    cursor.execute("""
    SELECT id FROM tags
    WHERE name = ?
    """, (name,))

    return cursor.fetchone()[0]

# Add GIF
def add_gif(name, url, preview_path, collections, tags):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Add GIF
        cursor.execute("""
        INSERT INTO gifs (
            name,
            url,
            preview_path
        )
        VALUES (?, ?, ?)
        """, (name, url, preview_path))

        gif_id = cursor.lastrowid

        # Add collections
        for collection in collections:

            collection_id = get_or_create_collection(
                cursor,
                collection
            )

            cursor.execute("""
            INSERT OR IGNORE INTO gif_collections
            (gif_id, collection_id)
            VALUES (?, ?)
            """, (gif_id, collection_id))

        # Add tags
        for tag in tags:

            tag_id = get_or_create_tag(
                cursor,
                tag
            )

            cursor.execute("""
            INSERT OR IGNORE INTO gif_tags
            (gif_id, tag_id)
            VALUES (?, ?)
            """, (gif_id, tag_id))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        conn.rollback()

        return False

    finally:

        conn.close()

# Get all GIFs
def get_all_gifs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        gifs.id,
        gifs.name,
        gifs.url,
        gifs.preview_path,
        GROUP_CONCAT(DISTINCT collections.name),
        GROUP_CONCAT(DISTINCT tags.name)

    FROM gifs

    LEFT JOIN gif_collections
        ON gifs.id = gif_collections.gif_id

    LEFT JOIN collections
        ON gif_collections.collection_id = collections.id

    LEFT JOIN gif_tags
        ON gifs.id = gif_tags.gif_id

    LEFT JOIN tags
        ON gif_tags.tag_id = tags.id

    GROUP BY gifs.id
    """)

    results = cursor.fetchall()

    conn.close()

    return results

# Search GIFs by tag
def search_tags(tag):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT gifs.*
    FROM gifs
    JOIN gif_tags
        ON gifs.id = gif_tags.gif_id
    JOIN tags
        ON gif_tags.tag_id = tags.id
    WHERE tags.name LIKE ?
    """, (f"%{tag}%",))

    results = cursor.fetchall()

    conn.close()

    return results

# Search GIFs by collection
def search_collection(collection):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT gifs.*
    FROM gifs
    JOIN gif_collections
        ON gifs.id = gif_collections.gif_id
    JOIN collections
        ON gif_collections.collection_id = collections.id
    WHERE collections.name LIKE ?
    """, (f"%{collection}%",))

    results = cursor.fetchall()

    conn.close()

    return results

# Delete GIF
def delete_gif(gif_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Remove relationships first
    cursor.execute("""
    DELETE FROM gif_collections
    WHERE gif_id = ?
    """, (gif_id,))

    cursor.execute("""
    DELETE FROM gif_tags
    WHERE gif_id = ?
    """, (gif_id,))

    # Remove GIF
    cursor.execute("""
    DELETE FROM gifs
    WHERE id = ?
    """, (gif_id,))

    conn.commit()
    conn.close()

# Get GIF by ID
def get_gif_by_id(gif_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM gifs
    WHERE id = ?
    """, (gif_id,))

    result = cursor.fetchone()

    conn.close()

    return result

# Create a new collection
def create_collection(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO collections (name)
    VALUES (?)
    """, (name.lower(),))

    conn.commit()
    conn.close()

# Get all collections
def get_all_collections():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM collections
    ORDER BY name
    """)

    results = cursor.fetchall()

    conn.close()

    return results

# Delete collection
def delete_collection(collection_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM gif_collections
    WHERE collection_id = ?
    """, (collection_id,))

    cursor.execute("""
    DELETE FROM collections
    WHERE id = ?
    """, (collection_id,))

    conn.commit()
    conn.close()

# Get collection by ID
def get_collection_by_id(collection_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM collections
    WHERE id = ?
    """, (collection_id,))

    result = cursor.fetchone()

    conn.close()

    return result

# Update GIF name
def update_gif_name(gif_id, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE gifs
    SET name = ?
    WHERE id = ?
    """, (name, gif_id))

    conn.commit()
    conn.close()

# Remove all collections from GIF
def remove_gif_collections(gif_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM gif_collections
    WHERE gif_id = ?
    """, (gif_id,))

    conn.commit()
    conn.close()

# Remove all tags from GIF
def remove_gif_tags(gif_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM gif_tags
    WHERE gif_id = ?
    """, (gif_id,))

    conn.commit()
    conn.close()

# Add GIF to collection
def add_gif_collection(gif_id, collection_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO gif_collections
    (gif_id, collection_id)
    VALUES (?, ?)
    """, (gif_id, collection_id))

    conn.commit()
    conn.close()

# Add GIF tag
def add_gif_tag(gif_id, tag_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO gif_tags
    (gif_id, tag_id)
    VALUES (?, ?)
    """, (gif_id, tag_id))

    conn.commit()
    conn.close()

# Get GIF details with collections and tags
def get_gif_full_details(gif_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        gifs.id,
        gifs.name,
        gifs.url,
        gifs.preview_path
    FROM gifs
    WHERE gifs.id = ?
    """, (gif_id,))

    gif = cursor.fetchone()

    if gif is None:

        conn.close()
        return None

    cursor.execute("""
    SELECT collections.name
    FROM collections
    JOIN gif_collections
    ON collections.id = gif_collections.collection_id
    WHERE gif_collections.gif_id = ?
    """, (gif_id,))

    collections = [
        row[0]
        for row in cursor.fetchall()
    ]

    cursor.execute("""
    SELECT tags.name
    FROM tags
    JOIN gif_tags
    ON tags.id = gif_tags.tag_id
    WHERE gif_tags.gif_id = ?
    """, (gif_id,))

    tags = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "id": gif[0],
        "name": gif[1],
        "url": gif[2],
        "preview_path": gif[3],
        "collections": collections,
        "tags": tags
    }