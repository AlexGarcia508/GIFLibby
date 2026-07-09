from database import create_database
import time

from gif_manager import (
    create_gif,
    list_gifs,
    find_by_tag,
    find_by_collection,
    remove_gif,
    send_gif_by_id
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
    print("5. Delete GIF")
    print("6. Send GIF to Discord")
    print("7. Exit")

    choice = input("\nChoice: ")

    # Add GIF
    if choice == "1":

        name = input("Name: ")
        path = input("Path/URL: ")

        collections = input(
            "Collections (example: cat,funny): "
        ).lower()

        tags = input(
            "Tags (example: cute,happy): "
        ).lower()

        create_gif(
            name,
            path,
            collections,
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
            print("-" * 30)

    # Search tags
    elif choice == "3":

        tag = input("Tag: ").lower()

        results = find_by_tag(tag)

        print()

        for gif in results:

            print(f"ID: {gif[0]}")
            print(f"Name: {gif[1]}")
            print(f"Path: {gif[2]}")
            print("-" * 30)

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

    # Delete GIF
    elif choice == "5":

        gif_id = input("GIF ID to delete: ")

        remove_gif(gif_id)

        print("GIF deleted.")

    # Send GIF to Discord
    elif choice == "6":

        gif_id = input("GIF ID to send: ")

        print("Sending...")

        time.sleep(0.5)

        send_gif_by_id(gif_id)

    # Exit
    elif choice == "7":

        print("Goodbye.")

        break

    else:

        print("Invalid choice.")