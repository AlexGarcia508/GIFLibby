import subprocess
import time
import requests
import websocket
import json
import os
import win32api


chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

port = "9223"

profile = os.path.join(
    os.getcwd(),
    "giflibby_chrome_profile"
)

os.makedirs(profile, exist_ok=True)

ws = None
chrome_process = None


def cleanup_old_cdp():
    try:
        version = requests.get(
            f"http://localhost:{port}/json/version",
            timeout=1
        ).json()

        old_ws = websocket.create_connection(
            version["webSocketDebuggerUrl"],
            origin=f"http://localhost:{port}"
        )

        old_ws.send(json.dumps({
            "id": 1,
            "method": "Browser.close"
        }))

        old_ws.close()

        print("Closed old Chrome session")
        time.sleep(2)

    except:
        pass


def cleanup():
    global ws, chrome_process

    if ws:
        try:
            ws.close()
        except:
            pass

    if chrome_process:
        try:
            chrome_process.terminate()
        except:
            pass


def wait_for_page():
    for _ in range(60):
        try:
            targets = requests.get(
                f"http://localhost:{port}/json"
            ).json()

            for target in targets:
                if target["type"] == "page":
                    return target

        except:
            pass

        time.sleep(0.5)

    return None


def get_expression(url):
    if "klipy.com" in url:
        print("Using Klipy extractor")

        return """
        document.querySelector(
            'meta[property="og:video:url"]'
        )?.content || null
        """

    if "tenor.com" in url:
        print("Using Tenor extractor")

        return """
        (() => {

            const html =
                document.documentElement.outerHTML;

            const match = html.match(
                /https?:\\/\\/[^"' ]+\\.mp4[^"' ]*/g
            );

            return match ? match[0] : null;

        })()
        """

    return None


def extract_mp4(url):
    global chrome_process, ws

    print("Cleaning old Chrome session...")

    cleanup_old_cdp()

    print("\nOpening:")
    print(url)

    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    width = 700
    height = 500

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    chrome_process = subprocess.Popen([
        chrome,
        f"--user-data-dir={profile}",
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-sync",
        "--disable-default-apps",
        "--new-window",
        f"--window-size={width},{height}",
        f"--window-position={x},{y}",
        url
    ])

    print("\nWaiting for CDP...")

    page = wait_for_page()

    if not page:
        print("Could not find page")
        cleanup()
        return None

    print("Page:")
    print(page["url"])

    try:
        ws = websocket.create_connection(
            page["webSocketDebuggerUrl"],
            origin=f"http://localhost:{port}"
        )
    except:
        print("Could not connect to Chrome")
        cleanup()
        return None

    print("Connected")

    expression = get_expression(url)

    if not expression:
        print("Unsupported website")
        cleanup()
        return None

    print("\nSearching MP4...")

    mp4 = None

    for i in range(60):
        try:
            ws.send(json.dumps({
                "id": i + 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": expression
                }
            }))

            response = json.loads(
                ws.recv()
            )

            mp4 = response["result"]["result"]["value"]

            if mp4:
                break

        except:
            pass

        time.sleep(0.25)

    if mp4:
        print("\nMP4 FOUND:")
        print(mp4)
    else:
        print("\nNo MP4 found")

    cleanup()

    print("\nDone!")

    return mp4