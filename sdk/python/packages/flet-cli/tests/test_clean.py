import pytest

from flet_cli.cli import get_parser


def _run_clean(args):
    """Parse a `flet clean ...` invocation and run its handler."""
    parser = get_parser()
    parsed = parser.parse_args(["clean", *args])
    parsed.handler(parsed)


def test_clean_deletes_existing_build_dir(tmp_path):
    """`flet clean` removes the app's `build` directory and its contents."""
    build_dir = tmp_path / "build"
    (build_dir / "flutter").mkdir(parents=True)
    (build_dir / "flutter" / "pubspec.yaml").write_text("name: app\n")

    _run_clean([str(tmp_path)])

    assert not build_dir.exists()
    # the app directory itself is left untouched
    assert tmp_path.is_dir()


def test_clean_is_noop_when_no_build_dir(tmp_path):
    """`flet clean` exits successfully when there is no `build` directory."""
    _run_clean([str(tmp_path)])

    assert not (tmp_path / "build").exists()


def test_clean_respects_path_argument(tmp_path):
    """Only the targeted app's `build` directory is deleted."""
    app_a = tmp_path / "app_a"
    app_b = tmp_path / "app_b"
    (app_a / "build").mkdir(parents=True)
    (app_b / "build").mkdir(parents=True)

    _run_clean([str(app_a)])

    assert not (app_a / "build").exists()
    assert (app_b / "build").exists()


def test_clean_errors_on_missing_app_path(tmp_path):
    """`flet clean` exits with a non-zero code when the app path does not exist."""
    missing = tmp_path / "does-not-exist"

    with pytest.raises(SystemExit) as exc_info:
        _run_clean([str(missing)])

    assert exc_info.value.code == 1
