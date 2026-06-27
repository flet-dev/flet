import pytest

from flet.testing.flet_test_app import FletTestApp


def test_flutter_test_target_validates_generated_app_test_in_device_mode(tmp_path):
    app_test = tmp_path / "integration_test" / "app_test.dart"
    app_test.parent.mkdir()
    app_test.write_text("void main() {}\n", encoding="utf-8")

    flet_app = FletTestApp(flutter_app_dir=tmp_path, device_mode=True)

    # The directory target is used; the generated driver is only validated.
    assert flet_app._FletTestApp__flutter_test_target() == "integration_test"


def test_flutter_test_target_requires_generated_app_test_in_device_mode(tmp_path):
    flet_app = FletTestApp(flutter_app_dir=tmp_path, device_mode=True)

    with pytest.raises(
        RuntimeError,
        match="Flutter integration test driver was not generated",
    ):
        flet_app._FletTestApp__flutter_test_target()


def test_flutter_test_target_rejects_empty_app_test(tmp_path):
    app_test = tmp_path / "integration_test" / "app_test.dart"
    app_test.parent.mkdir()
    app_test.write_text(" \n", encoding="utf-8")
    flet_app = FletTestApp(flutter_app_dir=tmp_path, device_mode=True)

    with pytest.raises(RuntimeError, match="Flutter integration test driver is empty"):
        flet_app._FletTestApp__flutter_test_target()


def test_flutter_test_target_keeps_directory_fallback_in_host_mode(tmp_path):
    flet_app = FletTestApp(flutter_app_dir=tmp_path)

    assert flet_app._FletTestApp__flutter_test_target() == "integration_test"


def test_flutter_test_target_keeps_directory_target_for_host_app_test(tmp_path):
    app_test = tmp_path / "integration_test" / "app_test.dart"
    app_test.parent.mkdir()
    app_test.write_text("void main() {}\n", encoding="utf-8")
    flet_app = FletTestApp(flutter_app_dir=tmp_path)

    assert flet_app._FletTestApp__flutter_test_target() == "integration_test"
