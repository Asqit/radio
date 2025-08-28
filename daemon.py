#!/usr/bin/env python3
from urllib.parse import urlparse
from typing import Optional
import subprocess
import argparse
import socket
import time
import sys


def err_print(msg: str, *args, **kwargs) -> None:
    print(msg, *args, file=sys.stderr, **kwargs)


def play_stream(url: str, timeout: Optional[int] = None) -> None:
    try:
        proc = subprocess.Popen(
            ["mplayer", url],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        try:
            ret = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise Exception("mplayer timed out")

        if ret == 0:
            raise Exception("mplayer exited cleanly (stream ended unexpectedly)")
        else:
            raise Exception(f"mplayer exited with code {ret}")

    except FileNotFoundError:
        raise Exception("mplayer not found")
    except Exception as e:
        raise Exception(f"Stream playback failed: {e}")


def has_connection(hostname: Optional[str]) -> bool:
    try:
        if hostname is None:
            hostname = "1.1.1.1"

        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        return False


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


def print_head(url: str, max_tries: int, hostname: str) -> None:
    print(
        """
============================
░█▄█░░░░░█▀▄░█▀█░█▀▄░▀█▀░█▀█
░█░█░▄▄▄░█▀▄░█▀█░█░█░░█░░█░█
░▀░▀░░░░░▀░▀░▀░▀░▀▀░░▀▀▀░▀▀▀
============================
By Asqit (https://github.com/Asqit)\n
"""
    )
    print("using:")
    print(f"- stream: {url}")
    print(f"- max-tries: {max_tries}")
    print(f"- hostname: {hostname or '1.1.1.1'}\n\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-tries", help="number of tries before exit", type=int)
    parser.add_argument("--hostname", help="hostname for internet checking", type=str)
    parser.add_argument("--stream-url", help="internet stream", type=str)
    args = parser.parse_args()

    max_tries: int = args.max_tries or 10
    stream_url: str = args.stream_url or read_url()
    hostname: str | None = args.hostname
    tries: int = 0

    print_head(stream_url, max_tries, hostname)

    while True:
        if tries >= max_tries:
            err_print("maximum number of tries has been reached!")
            sys.exit(1)

        if has_connection(hostname):
            try:
                tries = 0
                play_stream(stream_url)
            except Exception as e:
                tries += 1
                err_print(
                    f"exception has occurred during streaming: {e}\n\nRetrying in 5 seconds. "
                )
                time.sleep(5)
        else:
            tries += 1
            err_print("No internet connection. Retrying in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
