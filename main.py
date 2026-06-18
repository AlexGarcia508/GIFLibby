from database import (
    create_database,
    add_gif,
    get_all_gifs,
    search_tags,
    search_category,
    delete_gif
)

# Create database on startup
create_database()

# Keep program running until user exits
while True:

    print("\n====================")
    print("GIFLibby")
    print("====================")

    print("1. Add GIF")
    print("2. View All GIFs")
    print("3. Search Tags")
    print("4. View Category")
    print("5. Delete GIF")
    print("6. Exit")

    # Get menu choice
    choice = input("\nChoice: ")

    # Add GIF
    if choice == "1":

        # Ask user for information
        name = input("Name: ")

        path = input("Path: ")

        categories = input("Categories (example: happy,cool): ").lower()

        tags = input("Tags (example: cat,funny): ").lower()

        # Save to database
        add_gif(
            name,
            path,
            categories,
            tags
        )

        print("GIF added.")

    # View all GIFs
    elif choice == "2":

        gifs = get_all_gifs()

        print()

        for gif in gifs:

            print(f"ID: {gif[0]}")
            print(f"Name: {gif[1]}")
            print(f"Path: {gif[2]}")
            print(f"Categories: {gif[3]}")
            print(f"Tags: {gif[4]}")
            print("-" * 30)

    # Search tags
    elif choice == "3":

        tag = input("Tag: ").lower()

        results = search_tags(tag)

        print()

        for gif in results:

            print(f"ID: {gif[0]}")
            print(f"Name: {gif[1]}")
            print("-" * 30)

    # Search categories
    elif choice == "4":

        category = input("Category: ").lower()

        results = search_category(category)

        print()

        for gif in results:

            print(f"ID: {gif[0]}")
            print(f"Name: {gif[1]}")
            print("-" * 30)

    # Delete GIF
    elif choice == "5":

        gif_id = input("GIF ID to delete: ")

        delete_gif(gif_id)

        print("GIF deleted.")

    # Exit program
    elif choice == "6":

        print("Goodbye.")

        break

    # Invalid option
    else:

        print("Invalid choice.")