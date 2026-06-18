# discord_sender.py

# Allows us to control keyboard/mouse
import pyautogui

# Allows us to copy text to clipboard
import pyperclip

# Allows us to find open windows
import pygetwindow as gw

# Used for delays
import time



# Finds Discord and focuses it
def focus_discord():

    # Get all windows with Discord in the title
    windows = gw.getWindowsWithTitle("Discord")


    # If Discord isn't open
    if not windows:
        print("Discord window not found.")
        return False


    # Grab the first Discord window
    discord = windows[0]


    # Bring Discord to the front
    discord.activate()


    # Give Windows time to focus it
    time.sleep(0.5)


    return True



# Sends a GIF URL to Discord
def send_gif(url):

    # Copy the URL
    pyperclip.copy(url)


    # Focus Discord
    if focus_discord():

        # Paste the URL
        pyautogui.hotkey(
            "ctrl",
            "v"
        )


        # Press enter to send
        pyautogui.press("enter")


        print("GIF sent!")

    else:
        print("Could not send GIF.")