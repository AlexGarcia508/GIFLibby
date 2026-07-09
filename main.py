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
    remove_collection
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
    print("3. Search Tags")
    print("4. View Collection")
    print("5. Manage Collections")
    print("6. Delete GIF")
    print("7. Send GIF to Discord")
    print("8. Exit")

    choice = input("\nChoice: ")

    # Add GIF
    if choice == "1":

        name = input("Name: ")

        path = input(
            "Path/URL: "
        )

        print("\nAvailable Collections:")

        collections = list_collections()

        for collection in collections:
            print(
                f"{collection[0]}. {collection[1]}"
            )

        selected = input(
            "\nChoose collections (example: 1,3): "
        )

        collection_ids = [
            item.strip()
            for item in selected.split(",")
            if item.strip()
        ]

        tags = input(
            "Tags (example: cute,happy): "
        ).lower()

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

        for gif in gifs:

            print(f"ID: {gif[0]}")
            print(f"Name: {gif[1]}")
            print(f"Path: {gif[2]}")
            print(f"Collections: {gif[3]}")
            print(f"Tags: {gif[4]}")
            print("-" * 30)

    # Search tags
    elif choice == "3":

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
    elif choice == "4":

        collection = input("Collection: ").lower()

        results = find_by_collection(collection)

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
    elif choice == "5":

        print("\n1. Create Collection")
        print("2. View Collections")
        print("3. Delete Collection")
        print("4. Back")

        option = input("\nChoice: ")

        # Create collection
        if option == "1":

            name = input("Collection name: ")

            create_new_collection(name)

            print("Collection created.")

        # View collections
        elif option == "2":

            collections = list_collections()

            print()

            for collection in collections:

                print(
                    f"ID: {collection[0]} | Name: {collection[1]}"
                )

        # Delete collection
        elif option == "3":

            collection_id = input(
                "Collection ID to delete: "
            )

            remove_collection(collection_id)

            print("Collection deleted.")

        elif option == "4":

            continue

        else:

            print("Invalid choice.")

    # Delete GIF
    elif choice == "6":

        gif_id = input("GIF ID to delete: ")

        remove_gif(gif_id)

        print("GIF deleted.")

    # Send GIF to Discord
    elif choice == "7":

        gif_id = input("GIF ID to send: ")

        print("Sending...")

        time.sleep(0.5)

        send_gif_by_id(gif_id)

    # Exit
    elif choice == "8":

        print("Goodbye.")

        break

    else:

        print("Invalid choice.")