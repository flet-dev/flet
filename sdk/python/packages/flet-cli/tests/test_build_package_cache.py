"""Reuse and recovery of the packages a previous `flet build` left in build/."""

import contextlib
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from flet_cli.cli import parse_command_line
from flet_cli.commands.build_base import BaseBuildCommand


@pytest.fixture
def command(tmp_path):
    """A build command with its build directories under `tmp_path`."""
    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.build_dir = tmp_path / "build"
    cmd.flutter_dir = cmd.build_dir / "flutter"
    cmd.template_data = {"_options": {"target_arch": []}}
    cmd.python_release = SimpleNamespace(android_abis=("arm64-v8a", "x86_64"))
    return cmd


def write_package(directory):
    """Add an installed `flet` package to a site-packages `directory`."""
    package = directory / "flet" / "__init__.pyc"
    package.parent.mkdir(parents=True, exist_ok=True)
    package.write_bytes(b"package")


def write_pubspec(command, **extensions):
    """Write the Flutter project's pubspec.yaml with these path dependencies."""
    command.pubspec_path = str(command.flutter_dir / "pubspec.yaml")
    command.flutter_dir.mkdir(parents=True, exist_ok=True)
    dependencies = {"flutter": {"sdk": "flutter"}, "provider": "^6.0.0"}
    for name, path in extensions.items():
        dependencies[name] = {"path": str(path)}
    Path(command.pubspec_path).write_text(
        yaml.safe_dump({"dependencies": dependencies})
    )


def pubspec_dependencies(command):
    """Return the dependencies listed in the Flutter project's pubspec.yaml."""
    return yaml.safe_load(Path(command.pubspec_path).read_text())["dependencies"]


def write_extension(directory, name="flet_map", version="1.0.0"):
    """Put a Flutter package called `name` into `directory`."""
    extension = directory / name
    extension.mkdir(parents=True, exist_ok=True)
    (extension / "pubspec.yaml").write_text(f"name: {name}\nversion: {version}\n")


class TestSitePackagesMissing:
    """`_site_packages_missing()` decides when installed packages can be reused."""

    @pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin", "Emscripten"])
    def test_missing_empty_and_populated_package_directory(self, command, platform):
        """Counts site-packages as present only once it holds package files."""
        command.package_platform = platform
        root = command.flutter_dir if platform == "Emscripten" else command.build_dir
        packages = root / "site-packages"
        if platform == "Emscripten":
            packages = root / "build" / "site-packages"
            # A native cache must not mask missing web packages.
            write_package(command.build_dir / "site-packages")
        assert command._site_packages_missing()

        (packages / "flet").mkdir(parents=True)
        assert command._site_packages_missing()

        write_package(packages)
        assert not command._site_packages_missing()

    def test_darwin_pod_metadata_is_not_a_package(self, command, tmp_path):
        """Ignores the hidden `.pod` link serious_python leaves on Darwin."""
        command.package_platform = "Darwin"
        packages = command.build_dir / "site-packages"
        packages.mkdir(parents=True)
        pod = tmp_path / "pod"
        pod.mkdir()
        (pod / "sync_site_packages.sh").write_text("#!/bin/sh\n")
        try:
            (packages / ".pod").symlink_to(pod, target_is_directory=True)
        except OSError:
            pytest.skip("Creating symlinks is unavailable")

        assert command._site_packages_missing()

        write_package(packages)
        assert not command._site_packages_missing()

    @pytest.mark.parametrize(
        ("platform", "architectures"),
        [
            ("Android", ("arm64-v8a", "x86_64")),
            (
                "iOS",
                ("iphoneos.arm64", "iphonesimulator.arm64", "iphonesimulator.x86_64"),
            ),
        ],
    )
    def test_every_default_mobile_architecture_needs_packages(
        self, command, platform, architectures
    ):
        """Requires packages for every default mobile architecture."""
        command.package_platform = platform
        packages = command.build_dir / "site-packages"
        # Unrelated root files and empty ABI directories are not a usable cache.
        write_package(packages)
        for arch in architectures:
            (packages / arch).mkdir()
        assert command._site_packages_missing()

        for arch in architectures[:-1]:
            write_package(packages / arch)
        assert command._site_packages_missing()

        write_package(packages / architectures[-1])
        assert not command._site_packages_missing()

        (packages / architectures[-1] / "flet" / "__init__.pyc").unlink()
        assert command._site_packages_missing()

    @pytest.mark.parametrize(
        ("platform", "architecture"),
        [("Android", "arm64-v8a"), ("iOS", "iphoneos.arm64")],
    )
    def test_only_selected_architectures_need_packages(
        self, command, platform, architecture
    ):
        """Requires packages only for the architectures chosen with `--arch`."""
        command.package_platform = platform
        command.template_data["_options"]["target_arch"] = [architecture]
        write_package(command.build_dir / "site-packages" / architecture)

        assert not command._site_packages_missing()


class TestFlutterPackagesMissing:
    """`_flutter_packages_missing()` finds extensions pubspec.yaml points to."""

    @pytest.mark.parametrize("relative", [False, True])
    def test_detects_deleted_extension(self, command, relative):
        """Reports an extension in build/flutter-packages until it has a package."""
        packages = command.build_dir / "flutter-packages"
        write_pubspec(
            command,
            flet_map=Path("../flutter-packages/flet_map")
            if relative
            else packages / "flet_map",
        )
        assert command._flutter_packages_missing()

        (packages / "flet_map").mkdir(parents=True)
        assert command._flutter_packages_missing()

        write_extension(packages)
        assert not command._flutter_packages_missing()

    def test_detects_one_deleted_extension_among_several(self, command):
        """Reports a deleted extension when other extensions are still there."""
        packages = command.build_dir / "flutter-packages"
        write_pubspec(
            command,
            flet_map=packages / "flet_map",
            flet_geolocator=packages / "flet_geolocator",
        )
        write_extension(packages, "flet_map")
        assert command._flutter_packages_missing()

        write_extension(packages, "flet_geolocator")
        assert not command._flutter_packages_missing()

    def test_ignores_other_dependencies(self, command, tmp_path):
        """Ignores a missing pubspec.yaml and path dependencies elsewhere."""
        command.pubspec_path = str(command.flutter_dir / "pubspec.yaml")
        assert not command._flutter_packages_missing()

        write_pubspec(command, flet_map=tmp_path / "elsewhere" / "flet_map")
        assert not command._flutter_packages_missing()


class TestMissingExtensionRecovery:
    """`create_flutter_project()` starting over when an extension is gone."""

    @pytest.mark.parametrize("extension_deleted", [False, True])
    def test_restarts_the_build(
        self, command, monkeypatch, tmp_path, extension_deleted
    ):
        """Starts over with a clean project only when an extension is gone."""
        import cookiecutter.main

        command.options = SimpleNamespace(
            template=str(tmp_path / "template"), template_ref=None, template_dir=None
        )
        command.template_data = {"project_name": "test_app"}
        command.get_pyproject = lambda *_: None
        command.config_platform = "web"
        command.emojis = {"checkmark": ""}
        command.verbose = 0
        command.step = lambda *_: contextlib.nullcontext()
        command.pubspec_path = str(command.flutter_dir / "pubspec.yaml")
        # The template renders a pubspec.yaml without extensions.
        monkeypatch.setattr(
            cookiecutter.main, "cookiecutter", lambda **_: write_pubspec(command)
        )
        assert command.create_flutter_project()

        # A previous build added its extension after packaging.
        packages = command.build_dir / "flutter-packages"
        write_extension(packages)
        write_pubspec(command, flet_map=packages / "flet_map")
        stamps = command.build_dir / ".hash"
        derived = ["template-2", "package", "icons", "splashes"]
        for stamp in derived:
            (stamps / stamp).write_text("digest")
        if extension_deleted:
            shutil.rmtree(packages)

        assert command.create_flutter_project() is extension_deleted
        assert [(stamps / s).exists() for s in derived] == [not extension_deleted] * 4
        assert ("flet_map" in pubspec_dependencies(command)) is not extension_deleted


class TestPackagePythonApp:
    """`package_python_app()` keeping the previous Flutter packages."""

    @pytest.fixture
    def packaging(self, command):
        """Package a web app that has an extension; returns what the command saw."""
        command.options = parse_command_line(["build", "web"])
        command.package_platform = "Emscripten"
        command.target_platform = "web"
        command.config_platform = "web"
        command.python_release = SimpleNamespace(short="3.14", android_abis=())
        command.dart_exe = "dart"
        command.verbose = 0
        command.python_app_path = command.package_app_path = (
            command.build_dir.parent / "app"
        )
        command.python_app_path.mkdir(parents=True)
        command.flutter_dir.mkdir(parents=True)
        command.flutter_packages_dir = command.build_dir / "flutter-packages"
        command.flutter_packages_temp_dir = command.build_dir / "flutter-packages-temp"
        command.get_pyproject = lambda *_: None
        command.step = lambda *_: contextlib.nullcontext()
        write_extension(command.flutter_packages_dir)

        seen = {}

        class Stop(Exception):
            """Ends the package step once the package command is reached."""

        def run(args, cwd, env=None, capture_output=True):
            """Record the state the package command would run in, then stop."""
            seen["flutter_packages"] = (
                command.flutter_packages_dir / "flet_map" / "pubspec.yaml"
            ).exists()
            seen["skip"] = "--skip-site-packages" in args
            raise Stop

        command.run = run

        def package():
            """Run the package step up to the package command."""
            with pytest.raises(Stop):
                command.package_python_app()
            return seen

        return package

    @pytest.mark.parametrize("previous_build", [False, True])
    def test_reinstall_keeps_flutter_packages(self, command, packaging, previous_build):
        """Keeps build/flutter-packages when the package command starts."""
        if previous_build:
            # Packages installed by a build whose package arguments differed.
            write_package(command.flutter_dir / "build" / "site-packages")
            stamp = command.build_dir / ".hash" / "package"
            stamp.parent.mkdir(parents=True)
            stamp.write_text("previous package arguments")

        assert packaging() == {"flutter_packages": True, "skip": False}


class TestRegisterFlutterExtensions:
    """`register_flutter_extensions()` replacing Flutter packages after packaging."""

    @pytest.fixture
    def register(self, command):
        """Register extensions over stale ones; returns the registered versions."""
        command.flutter_packages_dir = command.build_dir / "flutter-packages"
        command.flutter_packages_temp_dir = command.build_dir / "flutter-packages-temp"
        command.flutter_dependencies = {}
        command.template_data = {"flutter": {"dependencies": []}}
        command.verbose = 0
        command.emojis = {"checkmark": ""}
        command.step = lambda *_: contextlib.nullcontext()
        command.apply_extension_settings = lambda: None
        write_extension(command.flutter_packages_dir, "flet_map", "1.0.0")
        write_extension(command.flutter_packages_dir, "flet_old")

        def register(skipped):
            """Register extensions after packaging, reused or not."""
            command.site_packages_skipped = skipped
            command.register_flutter_extensions()
            return {
                name: yaml.safe_load(
                    (Path(dependency["path"]) / "pubspec.yaml").read_text()
                )["version"]
                for name, dependency in command.flutter_dependencies.items()
            }

        return register

    def test_reinstall_replaces_stale_extensions(self, command, register):
        """Replaces build/flutter-packages with the packages just installed."""
        write_extension(command.flutter_packages_temp_dir, "flet_map", "2.0.0")
        assert register(skipped=False) == {"flet_map": "2.0.0"}
        assert not command.flutter_packages_temp_dir.exists()

    def test_reinstall_without_extensions_removes_them(self, command, register):
        """Removes the previous extensions when the app no longer has any."""
        assert register(skipped=False) == {}
        assert not command.flutter_packages_dir.exists()

    def test_skipped_install_keeps_extensions(self, register):
        """Keeps and registers the previous extensions when packages are reused."""
        assert register(skipped=True) == {"flet_map": "1.0.0", "flet_old": "1.0.0"}
