import textwrap
from pathlib import Path

import pytest

from flet_cli.commands.build_base import BaseBuildCommand
from flet_cli.utils.extension_settings import (
    ExtensionSettings,
    contributed_settings,
    find_extension_settings,
    merge_compile_options,
    merge_gradle_dependencies,
)

DESUGARING = 'coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")'


def _install(
    site_packages: Path,
    name: str,
    files: dict[str, str],
    version: str = "1.0.0",
) -> Path:
    """Install a fake distribution whose RECORD lists `files`, and return its
    dist-info directory."""
    for relative, content in files.items():
        path = site_packages / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content))
    dist_info = site_packages / f"{name.replace('-', '_')}-{version}.dist-info"
    dist_info.mkdir(parents=True)
    (dist_info / "METADATA").write_text(
        f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n\nBody\n"
    )
    record = [*files, f"{dist_info.name}/METADATA", f"{dist_info.name}/RECORD"]
    (dist_info / "RECORD").write_text("".join(f"{r},,\n" for r in record))
    return dist_info


def _extension(name: str, **settings) -> ExtensionSettings:
    """Build settings of one extension, keyed by dotted setting names."""
    return ExtensionSettings(
        name=name,
        version="1.0.0",
        path=Path(f"{name}/flet-extension.toml"),
        settings={k.replace("__", "."): v for k, v in settings.items()},
    )


class TestFindExtensionSettings:
    def test_reads_file_listed_in_record_anywhere_in_wheel(self, tmp_path):
        """A file listed in RECORD is read wherever the wheel placed it."""
        _install(
            tmp_path,
            "flet-b",
            {
                "flet_b/__init__.py": "",
                "flet_b/flet-extension.toml": """
                    [android.compile_options]
                    isCoreLibraryDesugaringEnabled = "true"
                """,
            },
        )
        _install(
            tmp_path,
            "flet-a",
            {"flet-extension.toml": f"[android]\ngradle_dependencies = '{DESUGARING}'"},
            version="2.0.0",
        )
        _install(tmp_path, "plain", {"plain/__init__.py": ""})

        extensions, warnings = find_extension_settings(tmp_path, None)

        assert warnings == []
        assert [e.label for e in extensions] == ["flet-a 2.0.0", "flet-b 1.0.0"]
        assert extensions[0].settings == {"android.gradle_dependencies": DESUGARING}
        assert extensions[1].settings == {
            "android.compile_options": {"isCoreLibraryDesugaringEnabled": "true"}
        }

    def test_reads_flutter_folder_files_from_flutter_packages(self, tmp_path):
        """Files under `flutter/` are read from where the build moved them."""
        site_packages = tmp_path / "site-packages"
        flutter_packages = tmp_path / "flutter-packages"
        _install(
            site_packages,
            "flet-x",
            {"flutter/flet_x/flet-extension.toml": "[android.compile_options]\n"},
        )
        moved = flutter_packages / "flet_x" / "flet-extension.toml"
        moved.parent.mkdir(parents=True)
        (site_packages / "flutter/flet_x/flet-extension.toml").rename(moved)

        extensions, warnings = find_extension_settings(site_packages, flutter_packages)

        assert warnings == []
        assert [e.path for e in extensions] == [moved]

    def test_reads_distribution_once_across_architectures(self, tmp_path):
        """A distribution installed for several architectures is read once."""
        for arch in ("arm64-v8a", "x86_64"):
            _install(
                tmp_path / arch,
                "flet-x",
                {"flet_x/flet-extension.toml": "[android.compile_options]\n"},
            )

        extensions, _ = find_extension_settings(tmp_path, None)

        assert [e.label for e in extensions] == ["flet-x 1.0.0"]

    def test_warns_when_listed_file_is_missing(self, tmp_path):
        """A file removed after installation is reported, not silently skipped."""
        _install(tmp_path, "flet-x", {"flet_x/flet-extension.toml": ""})
        (tmp_path / "flet_x/flet-extension.toml").unlink()

        extensions, warnings = find_extension_settings(tmp_path, None)

        assert extensions == []
        assert len(warnings) == 1
        assert "flet-x 1.0.0 lists flet_x/flet-extension.toml" in warnings[0]

    def test_warns_when_file_is_installed_outside_packages(self, tmp_path):
        """A data file, which RECORD lists outside site-packages, is reported."""
        dist_info = _install(tmp_path, "flet-x", {"flet-extension.toml": ""})
        record = dist_info / "RECORD"
        record.write_text(
            record.read_text().replace(
                "flet-extension.toml,", "../../flet-extension.toml,"
            )
        )

        extensions, warnings = find_extension_settings(tmp_path, None)

        assert extensions == []
        assert len(warnings) == 1
        assert "outside its packages" in warnings[0]

    def test_warns_for_flutter_package_whose_metadata_was_removed(self, tmp_path):
        """A Flutter package left without its distribution's metadata is reported."""
        site_packages = tmp_path / "site-packages"
        flutter_packages = tmp_path / "flutter-packages"
        _install(site_packages, "flet-a", {"flutter/flet_a/pubspec.yaml": ""})
        _install(site_packages, "plain", {"plain/__init__.py": ""})
        for package in ("flet_a", "flet_b"):
            (flutter_packages / package).mkdir(parents=True)
            (flutter_packages / package / "pubspec.yaml").write_text("")

        _, warnings = find_extension_settings(site_packages, flutter_packages)

        assert len(warnings) == 1
        assert "Flutter package flet_b" in warnings[0]

    def test_warns_when_package_metadata_was_removed(self, tmp_path):
        """Installed packages without any .dist-info are reported."""
        (tmp_path / "flet_x").mkdir()

        extensions, warnings = find_extension_settings(tmp_path, None)

        assert extensions == []
        assert len(warnings) == 1
        assert ".dist-info" in warnings[0]

    @pytest.mark.parametrize("create", [False, True])
    def test_nothing_installed_is_not_reported(self, tmp_path, create):
        """An empty or absent site-packages directory produces no warning."""
        site_packages = tmp_path / "site-packages"
        if create:
            site_packages.mkdir()
        assert find_extension_settings(site_packages, None) == ([], [])

    def test_unsupported_settings_are_ignored_with_warning(self, tmp_path):
        """Keys outside the allowlist, such as app identity, are not applied."""
        _install(
            tmp_path,
            "flet-x",
            {
                "flet_x/flet-extension.toml": """
                    product = "Renamed"
                    [android]
                    gradle_dependencies = "implementation(\\"a:b:1\\")"
                    [android.signing]
                    key_store = "x"
                """
            },
        )

        extensions, warnings = find_extension_settings(tmp_path, None)

        assert list(extensions[0].settings) == ["android.gradle_dependencies"]
        assert ["'product'" in w for w in warnings] == [True, False]
        assert "'android.signing.key_store'" in warnings[1]

    def test_tool_table_is_rejected_with_hint(self, tmp_path):
        """The pyproject form fails with a message to drop the prefix."""
        _install(
            tmp_path,
            "flet-x",
            {"flet_x/flet-extension.toml": "[tool.flet.android.compile_options]\n"},
        )
        with pytest.raises(ValueError, match=r"without the tool\.flet prefix"):
            find_extension_settings(tmp_path, None)

    def test_compile_option_values_are_stripped(self, tmp_path):
        """Surrounding whitespace in a value is removed when the file is read."""
        _install(
            tmp_path,
            "flet-x",
            {
                "flet_x/flet-extension.toml": (
                    "[android.compile_options]\nencoding = ' \"UTF-8\" '"
                )
            },
        )
        extensions, _ = find_extension_settings(tmp_path, None)
        assert extensions[0].settings["android.compile_options"] == {
            "encoding": '"UTF-8"'
        }

    @pytest.mark.parametrize(
        "content",
        [
            "[android]\ncompile_options = 1",
            '[android.compile_options]\nencoding = ""',
            "[android.compile_options]\nencoding = true",
            '[android]\ngradle_dependencies = " "',
            "[android]\ngradle_dependencies = ['a']",
            "[android",
        ],
    )
    def test_invalid_values_fail_the_build(self, tmp_path, content):
        """Malformed files and values name the extension that ships them."""
        _install(tmp_path, "flet-x", {"flet_x/flet-extension.toml": content})
        with pytest.raises(ValueError, match="flet-x 1.0.0"):
            find_extension_settings(tmp_path, None)

    def test_more_than_one_file_per_distribution_fails(self, tmp_path):
        """A distribution may declare its settings in one file only."""
        _install(
            tmp_path,
            "flet-x",
            {"a/flet-extension.toml": "", "b/flet-extension.toml": ""},
        )
        with pytest.raises(ValueError, match="more than one"):
            find_extension_settings(tmp_path, None)


class TestMergeCompileOptions:
    def test_extension_options_are_defaults_under_the_app(self):
        """Extension compile options apply unless the app sets the same one."""
        extension = _extension(
            "flet-x",
            android__compile_options={
                "isCoreLibraryDesugaringEnabled": "true",
                "encoding": '"UTF-8"',
            },
        )
        assert merge_compile_options({"encoding": '"ASCII"'}, [extension]) == {
            "isCoreLibraryDesugaringEnabled": "true",
            "encoding": '"ASCII"',
        }

    def test_conflicting_extensions_fail_unless_the_app_resolves(self):
        """A conflict between extensions fails until the app resolves it."""
        extensions = [
            _extension("flet-a", android__compile_options={"encoding": '"UTF-8"'}),
            _extension("flet-b", android__compile_options={"encoding": '"ASCII"'}),
        ]
        with pytest.raises(
            ValueError, match="Conflicting.*flet-a 1.0.0.*flet-b 1.0.0.*resolve"
        ):
            merge_compile_options(None, extensions)
        assert merge_compile_options({"encoding": '"UTF-16"'}, extensions) == {
            "encoding": '"UTF-16"'
        }

    def test_values_differing_in_whitespace_do_not_conflict(self, tmp_path):
        """Values read from files are compared after surrounding whitespace is
        removed."""
        for name, value in (("flet-a", "true"), ("flet-b", " true ")):
            _install(
                tmp_path,
                name,
                {
                    f"{name}/flet-extension.toml": (
                        "[android.compile_options]\n"
                        f'isCoreLibraryDesugaringEnabled = "{value}"'
                    )
                },
            )
        extensions, _ = find_extension_settings(tmp_path, None)
        assert merge_compile_options(None, extensions) == {
            "isCoreLibraryDesugaringEnabled": "true"
        }

    def test_matching_extension_values_do_not_conflict(self):
        """Extensions setting the same value for an option combine silently."""
        options = {"isCoreLibraryDesugaringEnabled": "true"}
        extensions = [
            _extension("flet-a", android__compile_options=options),
            _extension("flet-b", android__compile_options=options),
        ]
        assert merge_compile_options(None, extensions) == options

    @pytest.mark.parametrize("app_options", [None, {}, {"encoding": '"A"'}])
    def test_app_value_is_unchanged_without_extension_options(self, app_options):
        """Without extension options the app's value is returned as is."""
        extensions = [_extension("flet-x", android__gradle_dependencies=DESUGARING)]
        assert merge_compile_options(app_options, extensions) == app_options

    def test_invalid_app_value_is_left_for_validation(self):
        """A non-table app value is returned for the setting's own validation."""
        extensions = [
            _extension("flet-x", android__compile_options={"encoding": '"A"'})
        ]
        assert merge_compile_options(["invalid"], extensions) == ["invalid"]


class TestMergeGradleDependencies:
    def test_declarations_combine_without_duplicates(self):
        """Extension declarations come first, once, followed by the app's."""
        extensions = [
            _extension("flet-a", android__gradle_dependencies=DESUGARING),
            _extension("flet-b", android__gradle_dependencies=DESUGARING),
            _extension(
                "flet-c", android__gradle_dependencies='implementation("c:c:1")'
            ),
        ]
        app = """
            implementation("app:app:1")
        """
        assert merge_gradle_dependencies(app, extensions) == "\n".join(
            [DESUGARING, 'implementation("c:c:1")', 'implementation("app:app:1")']
        )

    def test_declarations_the_app_already_has_are_skipped(self):
        """An app that declares the dependency itself keeps a single copy."""
        extensions = [_extension("flet-x", android__gradle_dependencies=DESUGARING)]
        app = f"    {DESUGARING}\n"
        assert merge_gradle_dependencies(app, extensions) == app

    def test_multiline_declaration_is_kept_when_only_its_lines_appear(self):
        """A declaration is skipped only when the app contains it as a whole."""
        declaration = 'implementation(\n    "vendor:runtime:1"\n)'
        extensions = [_extension("flet-x", android__gradle_dependencies=declaration)]
        app = textwrap.dedent("""
            debugImplementation(
                "vendor:runtime:1"
            )
            implementation(
                "other:dependency:1"
            )
        """)
        merged = merge_gradle_dependencies(app, extensions)
        assert merged.startswith(declaration)

    @pytest.mark.parametrize(
        ("app", "kept"),
        [
            ('implementation( "vendor:runtime:1" )', False),
            ('implementation(\n  "vendor:runtime:1"\n)', False),
            ('debugImplementation("vendor:runtime:1")', True),
            ('// implementation("vendor:runtime:1")', True),
            ('maven("https://x")\nimplementation("vendor:runtime:1")', False),
        ],
    )
    def test_app_declarations_are_matched_as_wholes(self, app, kept):
        """Whitespace is ignored, while other configurations and commented-out
        declarations do not count as the app declaring the dependency."""
        declaration = 'implementation("vendor:runtime:1")'
        extensions = [_extension("flet-x", android__gradle_dependencies=declaration)]
        merged = merge_gradle_dependencies(app, extensions)
        assert merged.startswith(declaration + "\n") is kept

    def test_equivalent_extension_declarations_are_added_once(self):
        """Declarations differing only in whitespace are added once."""
        extensions = [
            _extension("flet-a", android__gradle_dependencies='api("a:a:1")'),
            _extension("flet-b", android__gradle_dependencies='api( "a:a:1" )'),
        ]
        assert merge_gradle_dependencies(None, extensions) == 'api("a:a:1")'

    @pytest.mark.parametrize("app", [None, "", 42])
    def test_app_value_is_unchanged_without_extension_declarations(self, app):
        """Without extension declarations the app's value is returned as is."""
        extensions = [_extension("flet-x", android__compile_options={})]
        assert merge_gradle_dependencies(app, extensions) == app

    def test_invalid_app_value_is_left_for_validation(self):
        """A non-string app value is returned for the setting's own validation."""
        extensions = [_extension("flet-x", android__gradle_dependencies=DESUGARING)]
        assert merge_gradle_dependencies(["a"], extensions) == ["a"]


def test_contributed_settings_name_table_properties():
    """Build output names each property an extension sets."""
    extension = _extension(
        "flet-x",
        android__compile_options={"isCoreLibraryDesugaringEnabled": "true"},
        android__gradle_dependencies=DESUGARING,
    )
    assert contributed_settings(extension) == [
        "android.compile_options.isCoreLibraryDesugaringEnabled",
        "android.gradle_dependencies",
    ]


class TestBuildCommand:
    def _command(self, tmp_path, app_settings, package_platform="Android"):
        """A build command with an installed extension and resolved options."""
        cmd = BaseBuildCommand.__new__(BaseBuildCommand)
        cmd.build_dir = tmp_path / "build"
        cmd.flutter_dir = cmd.build_dir / "flutter"
        cmd.flutter_packages_dir = cmd.build_dir / "flutter-packages"
        cmd.package_platform = package_platform
        cmd.get_pyproject = app_settings.get
        cmd.extensions = []
        cmd.warnings = []
        cmd.warn = cmd.warnings.append

        def cleanup(code, message):
            """Capture a failed build without exiting the test process."""
            assert code == 1
            raise ValueError(message)

        cmd.cleanup = cleanup
        cmd.template_data = {
            "_options": {
                "android_compile_options": cmd.get_android_compile_options(),
                "android_gradle_dependencies": cmd.get_android_gradle_dependencies(),
            }
        }
        return cmd

    @pytest.mark.parametrize(
        ("package_platform", "site_packages"),
        [
            ("Android", "build/site-packages/arm64-v8a"),
            ("Emscripten", "build/flutter/build/site-packages"),
        ],
    )
    def test_extension_settings_reach_template_options(
        self, tmp_path, package_platform, site_packages
    ):
        """Installed extension settings are applied for the second template pass."""
        _install(
            tmp_path / site_packages,
            "flet-x",
            {
                "flutter/flet_x/flet-extension.toml": f"""
                    [android]
                    gradle_dependencies = '{DESUGARING}'
                    [android.compile_options]
                    isCoreLibraryDesugaringEnabled = "true"
                """
            },
        )
        cmd = self._command(tmp_path, {}, package_platform)
        (tmp_path / site_packages / "flutter").rename(cmd.flutter_packages_dir)

        cmd.apply_extension_settings()

        options = cmd.template_data["_options"]
        assert options["android_compile_options"]["isCoreLibraryDesugaringEnabled"] == (
            "true"
        )
        assert options["android_gradle_dependencies"] == DESUGARING
        assert cmd.warnings == []

    def test_reapplying_does_not_repeat_extension_settings(self, tmp_path):
        """Applying twice gives the same options as applying once."""
        _install(
            tmp_path / "build/site-packages",
            "flet-x",
            {
                "flet_x/flet-extension.toml": (
                    f"[android]\ngradle_dependencies = '{DESUGARING}'"
                )
            },
        )
        cmd = self._command(
            tmp_path,
            {"tool.flet.android.gradle_dependencies": 'implementation("a:a:1")'},
        )

        cmd.apply_extension_settings()
        cmd.apply_extension_settings()

        assert cmd.template_data["_options"]["android_gradle_dependencies"] == (
            f'{DESUGARING}\nimplementation("a:a:1")'
        )

    def test_invalid_extension_fails_the_build(self, tmp_path):
        """An invalid file stops the build with its message."""
        _install(
            tmp_path / "build/site-packages",
            "flet-x",
            {"flet_x/flet-extension.toml": "[tool.flet]\n"},
        )
        with pytest.raises(ValueError, match="tool.flet prefix"):
            self._command(tmp_path, {}).apply_extension_settings()
