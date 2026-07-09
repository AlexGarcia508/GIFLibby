from discord_sender import send_gif
from database import (
    add_gif,
    get_all_gifs,
    search_tags,
    search_collection,
    delete_gif,
    get_gif_by_id,
    create_collection,
    get_all_collections,
    delete_collection,
    get_collection_by_id
)

# Add a new GIF
def create_gif(name, path, collection_ids, tags):
    collections = []

    for collection_id in collection_ids:

        collection = get_collection_by_id(
            collection_id
        )

        if collection:
            collections.append(
                collection[1]
            )

    tags = [
        item.strip().lower()
        for item in tags.split(",")
        if item.strip()
    ]

    add_gif(
        name,
        path,
        collections,
        tags
    )

# Get all GIFs
def list_gifs():
    return get_all_gifs()

# Find GIFs by tag
def find_by_tag(tag):
    return search_tags(tag.lower())

# Find GIFs by collection
def find_by_collection(collection):
    return search_collection(collection.lower())

# Remove GIF
def remove_gif(gif_id):
    delete_gif(gif_id)

# Send GIF to Discord
def send_gif_by_id(gif_id):

    gif = get_gif_by_id(gif_id)

    if gif is None:
        print("GIF not found.")
        return

    url = gif[2]

    print(f"Sending {gif[1]}...")

    send_gif(url)

# Create collection
def create_new_collection(name):
    create_collection(name)

# List collections
def list_collections():
    return get_all_collections()

# Remove collection
def remove_collection(collection_id):
    delete_collection(collection_id)