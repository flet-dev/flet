from types import SimpleNamespace

from PIL import Image

from flet_cli.commands.build_base import BaseBuildCommand


def test_removing_windows_icon_regenerates_default_icon(tmp_path):
    assets = tmp_path / "app" / "assets"
    assets.mkdir(parents=True)
    source = assets / "icon.png"
    Image.new("RGBA", (256, 256), "red").save(source)

    flutter_dir = tmp_path / "flutter"
    target = flutter_dir / "windows" / "runner" / "resources" / "app_icon.ico"
    target.parent.mkdir(parents=True)
    Image.new("RGBA", (256, 256), "blue").save(target)
    placeholder = target.read_bytes()

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

    cmd.customize_icons()
    user_icon = target.read_bytes()
    assert user_icon != placeholder

    # Without a user icon, the icon is generated from the Flet logo rather
    # than left as the template's placeholder or the last user icon.
    source.unlink()
    cmd.customize_icons()
    default_icon = target.read_bytes()
    assert default_icon not in (placeholder, user_icon)

    with Image.open(target) as ico:
        # The Flet logo is pink and blue on transparency, not a flat colour.
        colours = ico.convert("RGBA").getcolors(256 * 256)
        assert len(colours) > 2
