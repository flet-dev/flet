"""
Smoke test for `flet serve` against a built web artifact directory.

This script starts the local static server, waits for it to become healthy,
and verifies the cross-origin headers required by Flet web apps.
"""

from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


EXPECTED_HEADERS = {
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Access-Control-Allow-Origin": "*",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test `flet serve` for web output.")
    parser.add_argument(
        "--web-root",
        type=Path,
        required=True,
        help="Path to the built web directory (for example: build/web).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=45.0,
        help="Max time to wait for `flet serve` to become healthy.",
    )
    parser.add_argument(
        "--probe-interval-seconds",
        type=float,
        default=1.0,
        help="Delay between readiness probes.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("flet-serve-smoke.log"),
        help="File used to capture `flet serve` output.",
    )
    return parser.parse_args()


def find_open_port(host: str = "127.0.0.1") -> int:
    # Bind to port 0 so the OS picks a currently-free port for this process.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def main() -> int:
    args = parse_args()
    web_root = args.web_root.resolve()
    log_file = args.log_file.resolve()

    if not web_root.is_dir():
        print(f"Error: web root does not exist or is not a directory: {web_root}", file=sys.stderr)
        return 1

    port = find_open_port()
    url = f"http://127.0.0.1:{port}/"

    # Launch the local CLI module directly to avoid PATH/tool-wrapper ambiguity.
    with log_file.open("w", encoding="utf-8") as output:
        server = subprocess.Popen(
            [sys.executable, "-m", "flet_cli.cli", "serve", str(web_root), "--port", str(port)],
            stdout=output,
            stderr=subprocess.STDOUT,
        )

        try:
            deadline = time.time() + args.timeout_seconds
            last_error: Exception | None = None
            response_headers = None
            response_body = b""

            # Probe until the server is healthy, exits unexpectedly, or timeout is reached.
            while time.time() < deadline:
                if server.poll() is not None:
                    break

                try:
                    with urllib.request.urlopen(url, timeout=2) as response:
                        response_headers = response.headers
                        response_body = response.read()
                    if response_body:
                        break
                except Exception as exc:  # noqa: BLE001 - diagnostic value for CI failures
                    last_error = exc
                    time.sleep(args.probe_interval_seconds)

            if server.poll() is not None:
                output.flush()
                log_output = log_file.read_text(encoding="utf-8", errors="replace")
                print(
                    "Error: `flet serve` exited before becoming healthy.\n"
                    f"Exit code: {server.returncode}\n"
                    f"Log:\n{log_output}",
                    file=sys.stderr,
                )
                return 1

            if response_headers is None or not response_body:
                print(
                    "Error: timed out waiting for `flet serve` to return web content.\n"
                    f"Last probe error: {last_error}",
                    file=sys.stderr,
                )
                return 1

            for name, expected_value in EXPECTED_HEADERS.items():
                actual_value = response_headers.get(name)
                if actual_value != expected_value:
                    print(
                        f"Error: unexpected {name}: {actual_value!r} (expected {expected_value!r})",
                        file=sys.stderr,
                    )
                    return 1

            print(f"`flet serve` smoke test passed: {url}")
            return 0
        finally:
            # Always stop the background server to avoid leaking processes in CI jobs.
            if server.poll() is None:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
