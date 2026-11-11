import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NamedTuple

from PIL import IcoImagePlugin, Image

from flet_cli.commands.build_base import BaseBuildCommand

TEMPLATE_SIZES = (16, 32, 48, 256)
"""The entry sizes of the build template's `app_icon.ico` placeholder."""


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
        _write_ico(target, dict.fromkeys(TEMPLATE_SIZES, "blue"))

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


def _sizes(path: Path) -> tuple[int, ...]:
    """
    The entry sizes a `.ico` declares.

    Args:
        path: The `.ico` to read.

    Returns:
        The square sizes, ascending.
    """

    return BaseBuildCommand.get_ico_sizes(path)


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


def test_removing_windows_icon_regenerates_default_icon(tmp_path):
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


def test_windows_ico_is_copied_as_supplied(tmp_path):
    """A `.ico` holds artwork its author drew for each size, so none of it
    is rendered from the largest image, and its own size list stands in for
    the template's."""
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


def test_generic_ico_is_copied_on_windows(tmp_path):
    """A `.ico` is a Windows icon whatever it is called; only Windows builds
    see it at all, since `find_platform_image` drops it elsewhere."""
    build = _build(tmp_path)
    supplied = _write_ico(build.assets / "icon.ico", {32: "red", 256: "blue"})

    build.cmd.customize_icons()

    assert build.target.read_bytes() == supplied


def test_changed_ico_is_copied_again(tmp_path):
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


def test_ico_is_not_invented_for_a_template_without_one(tmp_path):
    """Like `write()`, copying only overwrites an icon the rendered project
    declares; a template that ships no `app_icon.ico` references none."""
    build = _build(tmp_path, placeholder=False)
    _write_ico(build.assets / "icon_windows.ico", {16: "red", 256: "blue"})

    build.cmd.customize_icons()

    assert not build.target.exists()


def test_ico_sizes_do_not_leak_into_later_renders(tmp_path):
    """The rendered icon's sizes guide later renders, so a copied `.ico`
    must not replace them with its own: a PNG supplied after it, and the
    default icon after that, still get the template's sizes."""
    build = _build(tmp_path)
    source = build.assets / "icon_windows.ico"
    _write_ico(source, {64: "red", 256: "blue"})
    build.cmd.customize_icons()
    assert _sizes(build.target) == (64, 256)

    source.unlink()
    png = build.assets / "icon_windows.png"
    Image.new("RGBA", (256, 256), "red").save(png)
    build.cmd.customize_icons()
    assert _sizes(build.target) == TEMPLATE_SIZES

    png.unlink()
    build.cmd.customize_icons()
    assert _sizes(build.target) == TEMPLATE_SIZES


def test_template_sizes_follow_a_re_render(tmp_path):
    """A re-rendered template may declare other sizes. Its digest changes
    with it, so the sizes recorded from the previous placeholder give way."""
    build = _build(tmp_path)
    source = build.assets / "icon_windows.ico"
    _write_ico(source, {64: "red", 256: "blue"})
    build.cmd.customize_icons()

    # A re-render restores the placeholder, here one that wants other sizes.
    _write_ico(build.target, {32: "blue", 256: "blue"})
    build.cmd.template_digest = "another-template-digest"
    source.unlink()
    Image.new("RGBA", (256, 256), "red").save(build.assets / "icon_windows.png")
    build.cmd.customize_icons()

    assert _sizes(build.target) == (32, 256)


def test_small_ico_is_copied_with_a_warning(tmp_path, capsys):
    """A `.ico` with no image as large as the project's largest icon is
    still its author's choice, but Windows will enlarge it, so say so."""
    build = _build(tmp_path)
    supplied = _write_ico(build.assets / "icon_windows.ico", {16: "red", 48: "blue"})

    build.cmd.customize_icons()

    assert build.target.read_bytes() == supplied
    output = _console_output(capsys)
    assert "largest image is 48px" in output
    assert "Add a 256x256 image" in output


def test_truncated_ico_warns_and_falls_back_to_default_icon(tmp_path, capsys):
    """A damaged `.ico` must not be copied to fail the resource compiler
    later: like any unreadable source, it warns and gives the default icon."""
    build = _build(tmp_path)
    source = build.assets / "icon_windows.ico"
    whole = _write_ico(source, {16: "red", 256: "blue"})
    source.write_bytes(whole[: len(whole) // 2])

    build.cmd.customize_icons()

    assert build.target.read_bytes() != whole[: len(whole) // 2]
    assert _distinct_colours(build.target) > 2
    output = _console_output(capsys)
    assert "could not read image icon_windows.ico" in output
    assert "Using the default Flet icon" in output


def test_unreadable_ico_warns_and_falls_back_to_default_icon(tmp_path, capsys):
    """A file that is not a Windows icon is not copied as one: the build
    warns and the app gets the default icon, as for any unreadable source."""
    build = _build(tmp_path)
    placeholder = build.target.read_bytes()
    (build.assets / "icon_windows.ico").write_bytes(b"not-actually-an-ico")

    build.cmd.customize_icons()

    generated = build.target.read_bytes()
    assert generated not in (placeholder, b"not-actually-an-ico")
    assert _distinct_colours(build.target) > 2
    output = _console_output(capsys)
    assert "could not read image icon_windows.ico" in output
    assert "Using the default Flet icon" in output
