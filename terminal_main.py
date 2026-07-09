from database import create_database
import time

from gif_manager import (
    create_gif,
    list_gifs,
    find_by_tag,
    find_by_collection,
    remove_gif,
    send_gif_by_id,
    create_new_collection,
    list_collections,
    remove_collection,
    edit_gif,
    get_gif_details,
    get_full_gif_details
)

# Create database when program starts
create_database()

# Main program loop
while True:
    print("\n====================")
    print("GIFLibby")
    print("====================")
    print("1. Add GIF")
    print("2. View All GIFs")
    print("3. View GIF Details")
    print("4. Search Tags")
    print("5. View Collection")
    print("6. Manage Collections")
    print("7. Edit GIF")
    print("8. Delete GIF")
    print("9. Send GIF to Discord")
    print("10. Exit")

    choice = input("\nChoice: ")

    # Add GIF
    if choice == "1":
        name = input("Name: ")
        path = input("Path/URL: ")

        print("\nAvailable Collections:")
        collections = list_collections()

        for collection in collections:
            print(f"{collection[0]}. {collection[1]}")

        selected = input("\nChoose collections (example: 1,3): ")

        collection_ids = [
            item.strip()
            for item in selected.split(",")
            if item.strip()
        ]

        tags = input("Tags (example: cute,happy): ").lower()

        create_gif(
            name,
            path,
            collection_ids,
            tags
        )

        print("GIF added.")

    # View all GIFs
    elif choice == "2":
        gifs = list_gifs()

        print()

        if gifs:
            for gif in gifs:
                print(f"ID: {gif[0]}")
                print(f"Name: {gif[1]}")
                print(f"Path: {gif[2]}")
                print("-" * 30)
        else:
            print("No GIFs found.")

    # View GIF details
    elif choice == "3":
        gif_id = input("GIF ID: ")

        gif = get_full_gif_details(
            gif_id
        )

        if gif:
            print("\nGIF Details")
            print("-" * 30)
            print(f"ID: {gif['id']}")
            print(f"Name: {gif['name']}")
            print(f"Path: {gif['path']}")

            print("\nCollections:")

            if gif["collections"]:
                for collection in gif["collections"]:
                    print(f"- {collection}")
            else:
                print("None")

            print("\nTags:")

            if gif["tags"]:
                for tag in gif["tags"]:
                    print(f"- {tag}")
            else:
                print("None")
        else:
            print("GIF not found.")

    # Search tags
    elif choice == "4":
        tag = input("Tag: ").lower()

        results = find_by_tag(tag)

        print()

        if results:
            for gif in results:
                print(f"ID: {gif[0]}")
                print(f"Name: {gif[1]}")
                print(f"Path: {gif[2]}")
                print("-" * 30)
        else:
            print("Tag not found.")

    # Search collection
    elif choice == "5":
        collection = input("Collection: ").lower()

        results = find_by_collection(
            collection
        )

        print()

        if results:
            for gif in results:
                print(f"ID: {gif[0]}")
                print(f"Name: {gif[1]}")
                print(f"Path: {gif[2]}")
                print("-" * 30)
        else:
            print("Collection not found.")

    # Manage collections
    elif choice == "6":
        print("\n1. Create Collection")
        print("2. View Collections")
        print("3. Delete Collection")
        print("4. Back")

        option = input("\nChoice: ")

        if option == "1":
            name = input("Collection name: ")

            create_new_collection(
                name
            )

            print("Collection created.")

        elif option == "2":
            collections = list_collections()

            print()

            for collection in collections:
                print(
                    f"ID: {collection[0]} | Name: {collection[1]}"
                )

        elif option == "3":
            collection_id = input(
                "Collection ID to delete: "
            )

            remove_collection(
                collection_id
            )

            print("Collection deleted.")

        elif option == "4":
            continue

        else:
            print("Invalid choice.")

    # Edit GIF
    elif choice == "7":
        gif_id = input("GIF ID to edit: ")

        gif = get_gif_details(
            gif_id
        )

        if gif is None:
            print("GIF not found.")

        else:
            name = input("New name: ")

            print("\nAvailable Collections:")
            collections = list_collections()

            for collection in collections:
                print(f"{collection[0]}. {collection[1]}")

            selected = input("\nChoose collections (example: 1,3): ")

            collection_ids = [
                item.strip()
                for item in selected.split(",")
                if item.strip()
            ]

            tags = input("Tags (example: cute,happy): ")

            tag_list = [
                item.strip().lower()
                for item in tags.split(",")
                if item.strip()
            ]

            edit_gif(
                gif_id,
                name,
                collection_ids,
                tag_list
            )

            print("GIF updated.")

    # Delete GIF
    elif choice == "8":
        gif_id = input("GIF ID to delete: ")

        remove_gif(
            gif_id
        )

        print("GIF deleted.")

    # Send GIF to Discord
    elif choice == "9":
        gif_id = input("GIF ID to send: ")

        print("Sending...")

        time.sleep(0.5)

        send_gif_by_id(
            gif_id
        )

    # Exit
    elif choice == "10":
        print("Goodbye.")
        break

    else:
        print("Invalid choice.")