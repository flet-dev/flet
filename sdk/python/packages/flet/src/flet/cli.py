from flet.utils.pip import ensure_flet_cli_package_installed


def main():
    ensure_flet_cli_package_installed()
    import flet_cli.cli

    flet_cli.cli.main()


if __name__ == "__main__":
    main()
