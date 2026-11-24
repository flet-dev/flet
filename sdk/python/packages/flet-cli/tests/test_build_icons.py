import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NamedTuple

from flet_platform_assets import WINDOWS_ICO_SIZES, ico_sizes
from PIL import IcoImagePlugin, Image

from flet_cli.commands.build_base import BaseBuildCommand


class Build(NamedTuple):
    """A Windows build set up for `customize_icons`."""

    cmd: BaseBuildCommand
    assets: Path
    """The app's `assets` directory, empty to begin with."""
    target: Path
    """The runner's `app_icon.ico` in the rendered project."""


def _build(tmp_path: Path, placeholder: bool = True) -> Build:
    """
    Set up a Windows build with the directories `customize_icons` uses.

    Args:
        tmp_path: The test's scratch directory.
        placeholder: Whether the rendered project ships the template's
            `app_icon.ico`, as the stock template does.

    Returns:
        The command and the paths the tests read and write.
    """

    assets = tmp_path / "app" / "assets"
    assets.mkdir(parents=True)
    flutter_dir = tmp_path / "flutter"
    target = flutter_dir / "windows" / "runner" / "resources" / "app_icon.ico"
    target.parent.mkdir(parents=True)
    if placeholder:
        _write_ico(target, dict.fromkeys(WINDOWS_ICO_SIZES, "blue"))

    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.package_app_path = assets.parent
    cmd.flutter_dir = flutter_dir
    cmd.build_dir = tmp_path / "build"
    cmd.target_platform = cmd.config_platform = "windows"
    cmd.options = SimpleNamespace()
    cmd.template_data = {"bundle_id": "com.example.test_app"}
    cmd.template_digest = "test-template-digest"
    cmd.get_pyproject = lambda *_: None
    cmd.update_status = lambda *_: None
    cmd.verbose = 0
    cmd.emojis = {"checkmark": ""}
    return Build(cmd, assets, target)


def _write_ico(path: Path, colours: dict[int, str]) -> bytes:
    """
    Write a `.ico` with one flat-coloured image per size.

    Args:
        path: Where to write it.
        colours: Pixel size -> fill colour of the image of that size.

    Returns:
        The bytes written.
    """

    images = {
        size: Image.new("RGBA", (size, size), colour)
        for size, colour in colours.items()
    }
    largest = images.pop(max(images))
    largest.save(
        path,
        format="ICO",
        sizes=[(size, size) for size in colours],
        append_images=list(images.values()),
    )
    return path.read_bytes()


def _damage_image(path: Path, size: int) -> None:
    """
    Zero the middle of one image of a `.ico`, keeping its header intact.

    Args:
        path: The `.ico` to damage in place.
        size: Pixel size of the image to damage.
    """

    with Image.open(path) as ico:
        assert isinstance(ico, IcoImagePlugin.IcoImageFile)
        entry = next(e for e in ico.ico.entry if e.width == size)
    data = bytearray(path.read_bytes())
    start = entry.offset + entry.size // 2
    data[start : start + 100] = bytes(100)
    path.write_bytes(bytes(data))


def _noise_ico(path: Path, sizes: tuple[int, ...]) -> None:
    """
    Write a `.ico` of noise images, which compress to more than a few bytes.

    Args:
        path: Where to write it.
        sizes: The pixel sizes of its images.
    """

    images = [Image.effect_noise((s, s), 60).convert("RGBA") for s in sizes]
    images[-1].save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[:-1],
    )


def _frames(path: Path) -> dict[int, Any]:
    """
    Read a `.ico` as pixel size -> colour of its top-left pixel.

    Args:
        path: The `.ico` to read.

    Returns:
        One entry per image in the file.
    """

    with Image.open(path) as ico:
        # Only the ICO plugin lets `size` select the image to load.
        assert isinstance(ico, IcoImagePlugin.IcoImageFile)
        frames = {}
        for size in sorted(ico.info["sizes"]):
            ico.size = size
            ico.load()
            frames[size[0]] = ico.convert("RGBA").getpixel((0, 0))
        return frames


def _distinct_colours(path: Path) -> int:
    """
    Count the colours in an icon's largest image.

    Args:
        path: The `.ico` to read.

    Returns:
        How many distinct RGBA values it holds.
    """

    with Image.open(path) as ico:
        colours = ico.convert("RGBA").getcolors(256 * 256)
    assert colours is not None
    return len(colours)


def _console_output(capsys) -> str:
    """
    Everything logged so far, with whitespace normalised.

    The console wraps long lines, so a phrase may be split across two.

    Args:
        capsys: pytest's capture fixture.

    Returns:
        The captured output as one line.
    """

    captured = capsys.readouterr()
    return " ".join((captured.out + captured.err).split())


class TestDefaultIcon:
    """The Flet logo icon used when the app supplies none."""

    def test_removing_source_regenerates_default_icon(self, tmp_path):
        """Removing the icon source generates the default icon from the Flet logo."""
        build = _build(tmp_path)
        source = build.assets / "icon.png"
        Image.new("RGBA", (256, 256), "red").save(source)
        placeholder = build.target.read_bytes()

        build.cmd.customize_icons()
        user_icon = build.target.read_bytes()
        assert user_icon != placeholder

        # Without a user icon, the icon is generated from the Flet logo rather
        # than left as the template's placeholder or the last user icon.
        source.unlink()
        build.cmd.customize_icons()
        default_icon = build.target.read_bytes()
        assert default_icon not in (placeholder, user_icon)
        # The Flet logo is pink and blue on transparency, not a flat colour.
        assert _distinct_colours(build.target) > 2


class TestWindowsIcoCopy:
    """A supplied `.ico` copied into a Windows build unchanged."""

    def test_copied_as_supplied(self, tmp_path):
        """A `.ico` is copied byte for byte, with its own images and size list."""
        build = _build(tmp_path)
        source = build.assets / "icon_windows.ico"
        supplied = _write_ico(source, {16: "red", 24: "green", 256: "blue"})

        build.cmd.customize_icons()

        assert build.target.read_bytes() == supplied
        assert _frames(build.target) == {
            16: (255, 0, 0, 255),
            24: (0, 128, 0, 255),
            256: (0, 0, 255, 255),
        }

    def test_generic_icon_ico_is_copied(self, tmp_path):
        """A generic `icon.ico` is copied on Windows like `icon_windows.ico`."""
        build = _build(tmp_path)
        supplied = _write_ico(build.assets / "icon.ico", {32: "red", 256: "blue"})

        build.cmd.customize_icons()

        assert build.target.read_bytes() == supplied

    def test_changed_ico_is_copied_again(self, tmp_path):
        """A `.ico` changed after a build is copied again on the next one."""
        build = _build(tmp_path)
        source = build.assets / "icon_windows.ico"
        _write_ico(source, {16: "red", 256: "blue"})
        build.cmd.customize_icons()

        replacement = _write_ico(source, {16: "green", 256: "white"})
        # Change detection keys on mtime; bump it explicitly so the test does
        # not depend on filesystem timestamp granularity.
        stat = source.stat()
        os.utime(source, (stat.st_atime, stat.st_mtime + 10))
        build.cmd.customize_icons()

        assert build.target.read_bytes() == replacement

    def test_not_created_for_a_template_without_one(self, tmp_path, capsys):
        """No `app_icon.ico` is created, or reported copied, without a placeholder."""
        build = _build(tmp_path, placeholder=False)
        _write_ico(build.assets / "icon_windows.ico", {16: "red", 256: "blue"})

        build.cmd.customize_icons()

        assert not build.target.exists()
        assert "Copied app icon" not in _console_output(capsys)

    def test_ico_wins_over_png_of_the_same_name(self, tmp_path):
        """A `.ico` is used on Windows even when a `.png` shares its name."""
        build = _build(tmp_path)
        Image.new("RGBA", (256, 256), "red").save(build.assets / "icon_windows.png")
        supplied = _write_ico(
            build.assets / "icon_windows.ico", {16: "green", 256: "blue"}
        )

        build.cmd.customize_icons()

        assert build.target.read_bytes() == supplied

    def test_small_ico_is_copied_with_a_warning(self, tmp_path, capsys):
        """A `.ico` smaller than the project's largest icon is copied with a warning."""
        build = _build(tmp_path)
        supplied = _write_ico(
            build.assets / "icon_windows.ico", {16: "red", 48: "blue"}
        )

        build.cmd.customize_icons()

        assert build.target.read_bytes() == supplied
        output = _console_output(capsys)
        assert "largest image is 48px" in output
        assert "Add a 256x256 image" in output


class TestWindowsIcoFallback:
    """A `.ico` that cannot be read in full gets the default icon."""

    def test_truncated_ico(self, tmp_path, capsys):
        """A truncated `.ico` is not copied; the default icon is used."""
        build = _build(tmp_path)
        source = build.assets / "icon_windows.ico"
        whole = _write_ico(source, {16: "red", 256: "blue"})
        source.write_bytes(whole[: len(whole) // 2])

        build.cmd.customize_icons()

        assert build.target.read_bytes() != whole[: len(whole) // 2]
        assert _distinct_colours(build.target) > 2
        output = _console_output(capsys)
        assert "icon_windows.ico is not a Windows icon" in output
        assert "Using the default Flet icon" in output

    def test_damaged_small_image(self, tmp_path, capsys):
        """A damaged small image gets the default icon, not the largest resampled."""
        build = _build(tmp_path)
        source = build.assets / "icon_windows.ico"
        _noise_ico(source, (16, 48, 256))
        _damage_image(source, 48)

        build.cmd.customize_icons()

        assert build.target.read_bytes() != source.read_bytes()
        # The Flet logo, not noise resampled from the intact 256px image.
        assert _distinct_colours(build.target) < 256 * 64
        output = _console_output(capsys)
        assert "icon_windows.ico is not a Windows icon" in output
        assert "Using the default Flet icon" in output

    def test_file_that_is_not_an_icon(self, tmp_path, capsys):
        """A `.ico` that is not an icon is not copied; the default icon is used."""
        build = _build(tmp_path)
        placeholder = build.target.read_bytes()
        (build.assets / "icon_windows.ico").write_bytes(b"not-actually-an-ico")

        build.cmd.customize_icons()

        generated = build.target.read_bytes()
        assert generated not in (placeholder, b"not-actually-an-ico")
        assert _distinct_colours(build.target) > 2
        output = _console_output(capsys)
        assert "icon_windows.ico is not a Windows icon" in output
        assert "Using the default Flet icon" in output


class TestWindowsIconSizes:
    """The icon sizes a Windows build renders."""

    def test_ico_sizes_do_not_leak_into_later_renders(self, tmp_path):
        """Renders after a copied `.ico` use the Windows sizes, not the `.ico`'s."""
        build = _build(tmp_path)
        source = build.assets / "icon_windows.ico"
        _write_ico(source, {64: "red", 256: "blue"})
        build.cmd.customize_icons()
        assert ico_sizes(build.target) == (64, 256)

        source.unlink()
        png = build.assets / "icon_windows.png"
        Image.new("RGBA", (256, 256), "red").save(png)
        build.cmd.customize_icons()
        assert ico_sizes(build.target) == WINDOWS_ICO_SIZES

        png.unlink()
        build.cmd.customize_icons()
        assert ico_sizes(build.target) == WINDOWS_ICO_SIZES
