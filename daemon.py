#!/usr/bin/env python3
from urllib.parse import urlparse
import http.client
import subprocess
import sys


def err_print(msg: str, *args, **kwargs) -> None:
    print(msg, *args, file=sys.stderr, **kwargs)


def has_internet():
    conn = http.client.HTTPSConnection("8.8.8.8", timeout=5)  # Google's DNS
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


def read_url() -> str:
    try:
        with open("url.txt", "r", encoding="utf-8") as f:
            url = f.read().strip()
            if not url:
                err_print("Error: URL file is empty.")
                sys.exit(1)
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                err_print("Error: Invalid URL format.")
                sys.exit(1)
            return url
    except FileNotFoundError:
        err_print("Error: URL file not found.")
        sys.exit(1)
    except Exception as e:
        err_print(f"Error reading URL file: {e}")
        sys.exit(1)


def play_stream(url: str) -> None:
    try:
        subprocess.run(
            ["mplayer", url],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        raise Exception("Stream playback failed")
    except FileNotFoundError:
        raise Exception("mplayer not found")


def main() -> None:
    stream_url = read_url()
    tries = 0
    MAX_TRIES = 10
    print(
        """
============================
░█▄█░░░░░█▀▄░█▀█░█▀▄░▀█▀░█▀█
░█░█░▄▄▄░█▀▄░█▀█░█░█░░█░░█░█
░▀░▀░░░░░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀▀
============================
By Asqit (https://github.com/Asqit)\n\n
"""
    )
    print("Starting stream daemon...")
    print(f"Streaming from: {stream_url}")
    print(f"{MAX_TRIES} tries max if no internet connection.")

    while True:
        if tries >= MAX_TRIES:
            err_print("Max tries reached. Exiting.")
            sys.exit(1)

        if has_internet():
            try:
                play_stream(stream_url)
            except Exception as e:
                err_print(f"Error: {e}. Retrying in 5 seconds...")
                subprocess.run(["sleep", "5"])
                tries += 1
        else:
            tries += 1
            err_print("No internet connection. Retrying in 10 seconds...")
            subprocess.run(["sleep", "10"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
else:
    err_print("This file is not meant to be imported.")
    sys.exit(1)
