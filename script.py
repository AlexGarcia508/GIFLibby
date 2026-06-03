import pyautogui
import pyperclip
import pygetwindow as gw
import time

GIF_URL = "https://tenor.com/view/cat-standing-cat-amused-cat-gif-25176042"


def focus_discord():
    windows = gw.getWindowsWithTitle("Discord")

    if not windows:
        print("Discord window not found.")
        return False

    discord = windows[0]
    discord.activate()
    time.sleep(0.5)
    return True


def send_gif(url):
    pyperclip.copy(url)

    if focus_discord():
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")


if __name__ == "__main__":
    send_gif(GIF_URL)