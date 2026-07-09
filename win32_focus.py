import win32gui
import win32con
import pyautogui
import pyperclip
import time


def find_discord():

    discord_hwnd = None

    def callback(hwnd, extra):

        nonlocal discord_hwnd

        title = win32gui.GetWindowText(hwnd)

        # Ignore Discord overlay/helper windows
        if (
            "Discord" in title
            and "Overlay" not in title
            and win32gui.IsWindowVisible(hwnd)
        ):
            discord_hwnd = hwnd


    win32gui.EnumWindows(callback, None)

    return discord_hwnd



def focus_discord():

    hwnd = find_discord()


    if not hwnd:
        print("Discord not found")
        return False


    # Restore if minimized
    win32gui.ShowWindow(
        hwnd,
        win32con.SW_RESTORE
    )


    # Focus Discord
    win32gui.SetForegroundWindow(hwnd)


    time.sleep(0.5)


    return (
        win32gui.GetForegroundWindow() == hwnd
    )



def send_gif(url):

    if not focus_discord():

        print("Could not focus Discord")
        return


    # Copy URL after Discord focus
    pyperclip.copy(url)


    time.sleep(0.2)


    pyautogui.hotkey(
        "ctrl",
        "v"
    )

    pyautogui.press(
        "enter"
    )

    print("GIF sent!")



if __name__ == "__main__":

    send_gif(
        "https://tenor.com/view/cat-standing-cat-amused-cat-gif-25176042"
    )