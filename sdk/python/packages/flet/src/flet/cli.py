import subprocess
import sys

import flet.version


def main():
    try:
        import flet_cli.cli
    except:
        subprocess.call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                f"flet-cli=={flet.version.version}",
            ]
        )
        import flet_cli.cli

    flet_cli.cli.main()


if __name__ == "__main__":
    main()
