from types import SimpleNamespace

from PIL import Image

from flet_cli.commands.build_base import BaseBuildCommand


def test_removing_windows_icon_restores_template_icon(tmp_path):
    assets = tmp_path / "app" / "assets"
    assets.mkdir(parents=True)
    source = assets / "icon.png"
    Image.new("RGBA", (256, 256), "red").save(source)

    flutter_dir = tmp_path / "flutter"
    target = flutter_dir / "windows" / "runner" / "resources" / "app_icon.ico"
    target.parent.mkdir(parents=True)
    Image.new("RGBA", (256, 256), "blue").save(target)
    original = target.read_bytes()

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
    assert target.read_bytes() != original

    # A later regeneration must not replace the original backup.
    Image.new("RGBA", (256, 256), "green").save(assets / "icon_windows.png")
    cmd.customize_icons()
    source.unlink()
    (assets / "icon_windows.png").unlink()
    cmd.customize_icons()
    assert target.read_bytes() == original
