import pyautogui
import pyperclip
import pygetwindow as gw
import time


# Finds Discord and focuses it
def focus_discord():
    # Get all windows with Discord in the title
    windows = gw.getWindowsWithTitle("Discord")
    #print("windows =" + windows)

    for window in windows:
        print("TITLE:", window.title)
        print("POSITION:", window.left, window.top)
        print()

    for i, window in enumerate(windows):
        print(i, window.title)

    # If Discord isn't open
    if not windows:
        print("Discord window not found.")
        return False

    # Grab the first Discord window
    discord = windows[0]
    #print("discord =" + discord)

    try:
        # Restore if minimized
        if discord.isMinimized:
            discord.restore()

        print(gw.getActiveWindow().title)
        # Move Discord to front
        discord.activate()
        #time.sleep(0.5)

        return True

    except Exception as e:
        print("Discord focus failed:", e)
        return False

# Sends a GIF URL to Discord
def send_gif(url):
    # Copy the URL
    pyperclip.copy(url)

    # Focus Discord
    if focus_discord():

        # Paste the URL
        pyautogui.hotkey("ctrl", "v")
        # Press enter to send
        pyautogui.press("enter")

        print("GIF sent!")

    else:
        print("Could not send GIF.")