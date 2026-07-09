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
    get_collection_by_id,
    update_gif_name,
    remove_gif_collections,
    remove_gif_tags,
    add_gif_collection,
    add_gif_tag,
    get_or_create_collection,
    get_or_create_tag
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

    return add_gif(
        name,
        path,
        collections,
        tags
    )

# Get all GIFs
def list_gifs():
    return get_all_gifs()

# Get GIF details
def get_gif_details(gif_id):
    return get_gif_by_id(gif_id)

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

# Edit GIF
def edit_gif(gif_id, name, collection_ids, tags):
    update_gif_name(
        gif_id,
        name
    )

    # Replace collections
    remove_gif_collections(
        gif_id
    )

    for collection_id in collection_ids:

        add_gif_collection(
            gif_id,
            collection_id
        )

    # Replace tags
    remove_gif_tags(
        gif_id
    )

    for tag in tags:
        tag_id = get_or_create_tag(
            tag
        )

        add_gif_tag(
            gif_id,
            tag_id
        )