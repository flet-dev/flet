import subprocess
import sys

import flet.version


def main():
    try:
        import flet_cli.version

        assert flet_cli.version.version == flet.version.version
    except:
        subprocess.call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-q",
                "--disable-pip-version-check",
                f"flet-cli=={flet.version.version}",
            ]
        )
    import flet_cli.cli

    flet_cli.cli.main()


if __name__ == "__main__":
    main()
