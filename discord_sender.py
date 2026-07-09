import pyautogui
import pyperclip
import win32gui
import win32con
import win32process
import win32api
import psutil
import time

# Finds the real Discord window
# Finds the real Discord window
def find_discord():
    discord_hwnd = None

    def callback(hwnd, extra):

        nonlocal discord_hwnd

        if not win32gui.IsWindowVisible(hwnd):
            return

        # Get process ID from window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        try:
            process = psutil.Process(pid)
            exe = process.name().lower()

            title = win32gui.GetWindowText(hwnd)

            # Debug: show every window process + title
            print(
                "PROCESS:",
                exe,
                "| TITLE:",
                title,
                "| HWND:",
                hwnd
            )

            # Pick real Discord app
            if (
                exe == "discord.exe"
                and "Overlay" not in title
            ):
                discord_hwnd = hwnd

        except psutil.NoSuchProcess:
            pass

    win32gui.EnumWindows(callback, None)

    return discord_hwnd

# Focus Discord using input attachment
def focus_discord():
    discord_hwnd = find_discord()

    if not discord_hwnd:

        print("Discord not found")

        return False

    print("SELECTED:", win32gui.GetWindowText(discord_hwnd))

    before = win32gui.GetForegroundWindow()

    print("Before:", win32gui.GetWindowText(before))

    try:

        # Restore ONLY if Discord is minimized
        # Prevents changing window size
        if win32gui.IsIconic(discord_hwnd):

            win32gui.ShowWindow(
                discord_hwnd,
                win32con.SW_RESTORE
            )

        # Get thread IDs
        current_thread = win32api.GetCurrentThreadId()

        discord_thread, _ = win32process.GetWindowThreadProcessId(
            discord_hwnd
        )

        foreground_thread, _ = win32process.GetWindowThreadProcessId(
            before
        )

        # Attach input queues
        win32process.AttachThreadInput(
            current_thread,
            foreground_thread,
            True
        )

        win32process.AttachThreadInput(
            current_thread,
            discord_thread,
            True
        )

        # Bring Discord forward
        win32gui.BringWindowToTop(discord_hwnd)

        # Focus Discord
        win32gui.SetForegroundWindow(discord_hwnd)

        # Detach input queues
        win32process.AttachThreadInput(
            current_thread,
            foreground_thread,
            False
        )

        win32process.AttachThreadInput(
            current_thread,
            discord_thread,
            False
        )

        time.sleep(0.1)

        after = win32gui.GetForegroundWindow()

        print("After:", win32gui.GetWindowText(after))

        if after == discord_hwnd:

            print("Discord focus successful")

            return True

        print("Discord focus failed")

        return False

    except Exception as e:
        print("Focus error:", e)

        return False

# Sends GIF URL to Discord
def send_gif(url):
    if focus_discord():

        pyperclip.copy(url)

        time.sleep(0.1)

        print("Pasting...")

        pyautogui.hotkey("ctrl", "v")

        time.sleep(0.2)

        pyautogui.press("enter")

        print("GIF sent!")

    else:

        print("Could not focus Discord.")