import argparse
import http.server
import socketserver
from pathlib import Path

from rich.console import Console
from rich.style import Style

from flet_cli.commands.base import BaseCommand

error_style = Style(color="red1", bold=True)
console = Console(log_path=False)


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


class Command(BaseCommand):
    """
    Serve static files from a directory with a lightweight web server,
    optionally adding WebAssembly-related headers for Flet web apps.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "web_root",
            type=str,
            nargs="?",
            help="Directory to serve",
            default="./build/web",
        )
        parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=8000,
            help="Port number to serve the files on. Use this to customize the port if "
            "the default is already in use or needs to be changed",
        )

    def handle(self, options: argparse.Namespace) -> None:
        directory = Path(options.web_root).resolve()
        if not directory.is_dir():
            console.print(
                f"Error: Directory '{directory}' does not exist or is not a folder.",
                style=error_style,
            )
            exit(1)

        def handler(*args, **kwargs):
            return CustomHandler(
                *args,
                directory=str(directory),
                **kwargs,
            )

        try:
            with socketserver.TCPServer(("", options.port), handler) as httpd:
                console.print(
                    f"Serving [green]{directory}[/green] at [cyan]"
                    f"http://localhost:{options.port}[/cyan] (Press Ctrl+C to stop)\n"
                )
                httpd.serve_forever()
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Server stopped by user.[/bold yellow]")
        except OSError as e:
            console.print(f"Error: {e}", style=error_style)
            exit(1)
