import pyautogui
import pyperclip
import pygetwindow as gw
import time

GIF_URL = "https://tenor.com/view/cat-standing-cat-amused-cat-gif-25176042"

def focus_discord():
    windows = gw.getWindowsWithTitle("Discord")
    # print("windows =" + windows)

    # NEW: remove Discord overlay/helper windows
    windows = [
        window
        for window in windows
        if "Overlay" not in window.title
    ]

    for window in windows:
        print("TITLE:", window.title)
        print("POSITION:", window.left, window.top)
        print()

    for i, window in enumerate(windows):
        print(i, window.title)

    if not windows:
        print("Discord window not found.")
        return False

    discord = windows[0]
    # print("discord =" + discord)

    try:
        # Restore if minimized
        if discord.isMinimized:
            discord.restore()

        # NEW: before focus check
        print("Before:", gw.getActiveWindow().title)

        # Move Discord to front
        discord.activate()

        time.sleep(0.5)

        # NEW: after focus check
        print("After:", gw.getActiveWindow().title)

        return True

    except Exception as e:

        print("Discord focus failed:", e)
        return False

def send_gif(url):
    pyperclip.copy(url)

    if focus_discord():

        pyautogui.hotkey("ctrl", "v")

        pyautogui.press("enter")

        print("GIF sent!")

    else:

        print("Could not send GIF.")

if __name__ == "__main__":

    send_gif(GIF_URL)