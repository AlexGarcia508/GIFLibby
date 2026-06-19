import pyautogui
import pyperclip
import win32gui
import win32con
import win32process
import win32api
import time


# Finds the real Discord window
def find_discord():

    discord_hwnd = None


    def callback(hwnd, extra):

        nonlocal discord_hwnd

        title = win32gui.GetWindowText(hwnd)


        # Debug: show Discord-related windows
        if "Discord" in title:

            print(
                "FOUND WINDOW:",
                title,
                "| HWND:",
                hwnd
            )


        # Pick real Discord window
        if (
            "Discord" in title
            and "Overlay" not in title
            and win32gui.IsWindowVisible(hwnd)
        ):
            discord_hwnd = hwnd


    win32gui.EnumWindows(
        callback,
        None
    )


    return discord_hwnd



# Focus Discord using input attachment
def focus_discord():

    discord_hwnd = find_discord()


    if not discord_hwnd:

        print(
            "Discord not found"
        )

        return False



    print(
        "SELECTED:",
        win32gui.GetWindowText(discord_hwnd)
    )


    before = win32gui.GetForegroundWindow()

    print(
        "Before:",
        win32gui.GetWindowText(before)
    )


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
        win32gui.BringWindowToTop(
            discord_hwnd
        )


        # Focus Discord
        win32gui.SetForegroundWindow(
            discord_hwnd
        )


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


        time.sleep(0.5)


        after = win32gui.GetForegroundWindow()


        print(
            "After:",
            win32gui.GetWindowText(after)
        )


        if after == discord_hwnd:

            print(
                "Discord focus successful"
            )

            return True


        print(
            "Discord focus failed"
        )

        return False



    except Exception as e:

        print(
            "Focus error:",
            e
        )

        return False




# Sends GIF URL to Discord
def send_gif(url):

    if focus_discord():


        # Copy URL
        pyperclip.copy(url)


        time.sleep(0.3)


        print(
            "Pasting..."
        )


        # Paste URL
        pyautogui.hotkey(
            "ctrl",
            "v"
        )


        time.sleep(0.2)


        # Send
        pyautogui.press(
            "enter"
        )


        print(
            "GIF sent!"
        )


    else:

        print(
            "Could not focus Discord."
        )