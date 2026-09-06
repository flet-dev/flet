"""Icon/splash image selection in `flet build`.

`find_platform_image` must pick a *decodable* image deterministically when
several files share a base name — otherwise the choice depends on filesystem
glob order and an `icon.svg` can slip through to the generator, which cannot
decode it and would fall back to no icon at all.
"""

from types import SimpleNamespace

from flet_cli.commands.build_base import BaseBuildCommand


class _FakeHash:
    def update(self, *_):
        pass


def _find(tmp_path, filenames, *, image_name="icon", target_platform="web"):
    assets = tmp_path / "assets"
    assets.mkdir(exist_ok=True)
    for name in filenames:
        (assets / name).write_bytes(b"x")
    fake_self = SimpleNamespace(target_platform=target_platform, verbose=0)
    return BaseBuildCommand.find_platform_image(
        fake_self, assets, image_name, _FakeHash()
    )


def test_prefers_raster_over_svg(tmp_path):
    # Both present: the raster png must win regardless of glob order.
    assert _find(tmp_path, ["icon.svg", "icon.png"]) == "icon.png"


def test_png_preferred_over_other_raster(tmp_path):
    # Ranking, not alphabetical order (jpg < png alphabetically).
    assert _find(tmp_path, ["icon.jpg", "icon.png"]) == "icon.png"


def test_svg_only_returns_none_with_warning(tmp_path, capsys):
    assert _find(tmp_path, ["icon.svg"]) is None
    combined = capsys.readouterr()
    assert "icon.svg" in (combined.out + combined.err)


def test_no_candidates_is_silent_none(tmp_path, capsys):
    assert _find(tmp_path, []) is None
    combined = capsys.readouterr()
    assert "Warning" not in (combined.out + combined.err)


def test_ico_is_windows_only(tmp_path):
    # ico is incompatible on web (no raster sibling) -> default icon.
    assert _find(tmp_path, ["icon.ico"], target_platform="web") is None
    # ...but valid on a windows build.
    assert _find(tmp_path, ["icon.ico"], target_platform="windows") == "icon.ico"
