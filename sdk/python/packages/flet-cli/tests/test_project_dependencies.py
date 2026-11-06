"""Tests for project_dependencies module."""

from pathlib import Path

import pytest

from flet_cli.utils.project_dependencies import (
    FLET_PACKAGES,
    FletVersionConflictError,
    get_poetry_dependencies,
    get_project_dependencies,
    override_dependencies,
    pin_flet_dependencies,
    read_requirements,
    read_requirements_file_text,
    requirements_use_hashes,
)

# ---------------------------------------------------------------------------
# get_poetry_dependencies
# ---------------------------------------------------------------------------


class TestGetPoetryDependencies:
    def test_none_returns_none(self):
        assert get_poetry_dependencies(None) is None

    def test_empty_dict(self):
        assert get_poetry_dependencies({}) == []

    def test_python_excluded(self):
        assert get_poetry_dependencies({"python": "^3.10"}) == []

    def test_exact_version(self):
        result = get_poetry_dependencies({"packaging": "26.0"})
        assert result == ["packaging==26.0"]

    def test_caret(self):
        result = get_poetry_dependencies({"urllib3": "^2.6.0"})
        assert result == ["urllib3 >=2.6.0"]

    def test_tilde(self):
        result = get_poetry_dependencies({"setuptools": "~82.0.0"})
        assert result == ["setuptools~=82.0.0"]

    def test_tilde_equals_passthrough(self):
        result = get_poetry_dependencies({"setuptools": "~=82.0.0"})
        assert result == ["setuptools~=82.0.0"]

    def test_wildcard(self):
        result = get_poetry_dependencies({"boto3": "*"})
        assert result == ["boto3"]

    def test_less_than(self):
        result = get_poetry_dependencies({"chardet": "<6"})
        assert result == ["chardet <6"]

    def test_less_than_equal(self):
        result = get_poetry_dependencies({"requests": "<=2.32.4"})
        assert result == ["requests <=2.32.4"]

    def test_greater_than_equal(self):
        result = get_poetry_dependencies({"certifi": ">=2026.1.4"})
        assert result == ["certifi >=2026.1.4"]

    def test_range_constraint(self):
        result = get_poetry_dependencies({"pydantic": ">=2.9.0,<3.0.0"})
        # _windows_safe ensures spaces before < and >
        assert "pydantic" in result[0]
        assert " >=" in result[0]
        assert " <" in result[0]

    def test_not_equal_combined(self):
        result = get_poetry_dependencies({"pandas": ">=2.3,!=2.3.3"})
        assert "pandas" in result[0]
        assert " >=" in result[0]
        assert "!=" in result[0]

    def test_spaces_in_version_stripped(self):
        result = get_poetry_dependencies({"chardet": "  <  6  "})
        assert result == ["chardet <6"]

    def test_dict_version(self):
        result = get_poetry_dependencies(
            {"scipy": {"version": "^1.16", "optional": True}}
        )
        assert result == ["scipy >=1.16"]

    def test_dict_version_with_markers(self):
        result = get_poetry_dependencies(
            {"pywin32": {"version": ">=310", "markers": "sys_platform == 'win32'"}}
        )
        assert result == ["pywin32 >=310; sys_platform == 'win32'"]

    def test_dict_git(self):
        result = get_poetry_dependencies(
            {"numpy": {"git": "https://github.com/numpy/numpy.git", "branch": "main"}}
        )
        assert result == ["numpy @ git+https://github.com/numpy/numpy.git@main"]

    def test_dict_git_ssh(self):
        result = get_poetry_dependencies(
            {"mylib": {"git": "git@github.com:org/repo.git", "tag": "v1.0"}}
        )
        assert result == ["mylib @ git@github.com:org/repo.git@v1.0"]

    def test_dict_git_subdirectory(self):
        result = get_poetry_dependencies(
            {
                "mylib": {
                    "git": "https://github.com/org/mono.git",
                    "branch": "main",
                    "subdirectory": "packages/mylib",
                }
            }
        )
        assert "subdirectory=packages/mylib" in result[0]

    def test_dict_path(self):
        result = get_poetry_dependencies({"mylib": {"path": "../mylib"}})
        assert result == ["../mylib"]

    def test_dict_url(self):
        result = get_poetry_dependencies(
            {"mylib": {"url": "https://example.com/mylib.tar.gz"}}
        )
        assert result == ["https://example.com/mylib.tar.gz"]

    def test_dict_unsupported_raises(self):
        with pytest.raises(ValueError, match="Unsupported"):
            get_poetry_dependencies({"bad": {"extras": ["foo"]}})

    def test_sorted_output(self):
        result = get_poetry_dependencies({"zlib": "1.0", "aiohttp": "3.0"})
        assert result == ["aiohttp==3.0", "zlib==1.0"]

    def test_multiple_deps(self):
        deps = {
            "python": "^3.10",
            "boto3": "*",
            "chardet": "<6",
            "packaging": "26.0",
        }
        result = get_poetry_dependencies(deps)
        assert "boto3" in result
        assert any("chardet" in r for r in result)
        assert any("packaging" in r for r in result)
        # python should be excluded
        assert not any("python" in r for r in result)


# ---------------------------------------------------------------------------
# get_project_dependencies
# ---------------------------------------------------------------------------


class TestGetProjectDependencies:
    def test_none_returns_none(self):
        assert get_project_dependencies(None) is None

    def test_empty_list(self):
        assert get_project_dependencies([]) == []

    def test_simple_dep(self):
        result = get_project_dependencies(["boto3"])
        assert result == ["boto3"]

    def test_exact_version(self):
        result = get_project_dependencies(["packaging==26.0"])
        assert result == ["packaging==26.0"]

    def test_gte(self):
        result = get_project_dependencies(["flet>=0.82.0"])
        assert result == ["flet >=0.82.0"]

    def test_lt_gets_space(self):
        result = get_project_dependencies(["chardet<6"])
        assert result == ["chardet <6"]

    def test_lte_gets_space(self):
        result = get_project_dependencies(["requests<=2.32.4"])
        assert result == ["requests <=2.32.4"]

    def test_gt_gets_space(self):
        result = get_project_dependencies(["chardet>3"])
        assert result == ["chardet >3"]

    def test_combined_constraints(self):
        result = get_project_dependencies(["pydantic>=2.9.0,<3.0.0"])
        assert len(result) == 1
        dep = result[0]
        assert "pydantic" in dep
        assert " <" in dep or " >" in dep

    def test_not_equal(self):
        result = get_project_dependencies(["pandas>=2.3,!=2.3.3"])
        assert len(result) == 1
        assert " >=" in result[0]
        assert "!=" in result[0]

    def test_compatible_release(self):
        result = get_project_dependencies(["setuptools~=82.0.0"])
        assert result == ["setuptools~=82.0.0"]

    def test_extras(self):
        result = get_project_dependencies(["uvicorn[standard]>=0.42.0"])
        dep = result[0]
        assert "uvicorn" in dep
        assert "[standard]" in dep
        assert " >=" in dep

    def test_markers_preserved(self):
        result = get_project_dependencies(['pywin32>=310; sys_platform == "win32"'])
        assert len(result) == 1
        assert "sys_platform" in result[0]
        assert "win32" in result[0]
        assert " >=" in result[0]

    def test_url_dep(self):
        result = get_project_dependencies(
            ["numpy @ git+https://github.com/numpy/numpy.git@main"]
        )
        assert len(result) == 1
        assert "git+https://github.com/numpy/numpy.git@main" in result[0]

    def test_extra_spaces_normalized(self):
        result = get_project_dependencies(["chardet   <  6"])
        assert result == ["chardet <6"]

    def test_sorted_and_deduplicated(self):
        result = get_project_dependencies(["zlib>=1.0", "aiohttp>=3.0", "zlib>=1.0"])
        assert result[0].startswith("aiohttp")
        assert len(result) == 2

    def test_downstream_compatible(self):
        """Output must be parseable by packaging.requirements.Requirement,
        since build_base.py does Requirement(dep).name on our output."""
        from packaging.requirements import Requirement

        deps = [
            "flet>=0.82.0",
            "chardet<6",
            "pydantic>=2.9.0,<3.0.0",
            'pywin32>=310; sys_platform == "win32"',
            "uvicorn[standard]>=0.42.0",
        ]
        result = get_project_dependencies(deps)
        for dep in result:
            req = Requirement(dep)
            assert req.name  # must parse without error


# ---------------------------------------------------------------------------
# read_requirements_file_text
# ---------------------------------------------------------------------------


class TestReadRequirementsFileText:
    def test_plain_file(self, tmp_path):
        """Returns the file's text when it includes no other files."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet\nhttpx==0.28.1\n")
        assert read_requirements_file_text(reqs) == "flet\nhttpx==0.28.1\n"

    def test_follows_requirement_and_constraint_includes(self, tmp_path):
        """Reads files included with every `-r`/`-c` spelling, relative paths."""
        (tmp_path / "sub").mkdir()
        reqs = tmp_path / "requirements.txt"
        reqs.write_text(
            "flet\n-r sub/a.txt\n--requirement=b.txt\n-cc.txt\n--constraint d.txt\n"
        )
        (tmp_path / "sub" / "a.txt").write_text("pkg-a\n-r nested.txt\n")
        (tmp_path / "sub" / "nested.txt").write_text("pkg-nested\n")
        (tmp_path / "b.txt").write_text("pkg-b\n")
        (tmp_path / "c.txt").write_text("pkg-c<2\n")
        (tmp_path / "d.txt").write_text("pkg-d<3\n")

        text = read_requirements_file_text(reqs)

        for name in ["pkg-a", "pkg-nested", "pkg-b", "pkg-c<2", "pkg-d<3"]:
            assert name in text

    def test_include_cycle_read_once(self, tmp_path):
        """Reads each file once when files include each other."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet\n-r other.txt\n")
        (tmp_path / "other.txt").write_text("httpx\n-r requirements.txt\n")
        text = read_requirements_file_text(reqs)
        assert text.count("flet\n") == 1
        assert text.count("httpx\n") == 1

    def test_urls_and_missing_files_skipped(self, tmp_path):
        """Skips included URLs and files that don't exist."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet\n-r https://example.com/r.txt\n-r missing.txt\n")
        assert read_requirements_file_text(reqs) == reqs.read_text()

    def test_editing_an_included_file_changes_text(self, tmp_path):
        """Changes when only an included file is edited."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet\n-r more.txt\n")
        more = tmp_path / "more.txt"
        more.write_text("httpx\n")
        before = read_requirements_file_text(reqs)
        more.write_text("httpx\ntabulate\n")
        assert read_requirements_file_text(reqs) != before

    @pytest.mark.parametrize(
        "include",
        [
            '-r "more requirements.txt"',
            "-c 'more requirements.txt'",
            '--requirement="more requirements.txt"',
            "--constraint='more requirements.txt'",
            '-r"more requirements.txt"',
            '-r \\\n  "more requirements.txt"',
            '--constraint=\\\n"more requirements.txt"',
            '-r "more requirements.txt"\\',
        ],
    )
    def test_editing_pip_style_include_changes_text(self, tmp_path, include):
        reqs = tmp_path / "requirements.txt"
        reqs.write_text(f"flet\n{include}\n")
        more = tmp_path / "more requirements.txt"
        more.write_text("httpx==0.27.0\n")
        before = read_requirements_file_text(reqs)

        more.write_text("httpx==0.28.1\n")

        after = read_requirements_file_text(reqs)
        assert "httpx==0.27.0" in before
        assert "httpx==0.28.1" in after
        assert before != after

    def test_environment_variable_include(self, tmp_path, monkeypatch):
        reqs = tmp_path / "requirements.txt"
        reqs.write_text('-r "${REQUIREMENTS_DIR}/more.txt"\n')
        directory = tmp_path / "requirements files"
        directory.mkdir()
        monkeypatch.setenv("REQUIREMENTS_DIR", str(directory))
        more = directory / "more.txt"
        more.write_text("httpx==0.27.0\n")
        before = read_requirements_file_text(reqs)

        more.write_text("httpx==0.28.1\n")

        assert "httpx==0.28.1" in read_requirements_file_text(reqs)
        assert read_requirements_file_text(reqs) != before

    def test_changing_environment_include_target_changes_text(
        self, tmp_path, monkeypatch
    ):
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("-r ${REQUIREMENTS_FILE}\n")
        for name, package in [("a.txt", "httpx"), ("b.txt", "tabulate")]:
            (tmp_path / name).write_text(package)
        monkeypatch.setenv("REQUIREMENTS_FILE", "a.txt")
        before = read_requirements_file_text(reqs)

        monkeypatch.setenv("REQUIREMENTS_FILE", "b.txt")

        assert read_requirements_file_text(reqs) != before

    def test_comment_continuation_does_not_hide_include(self, tmp_path):
        reqs = tmp_path / "requirements.txt"
        reqs.write_text('# comment \\\n-r "more.txt" # inline comment\n')
        (tmp_path / "more.txt").write_text("httpx\n")

        assert "httpx\n" in read_requirements_file_text(reqs)

    def test_multiple_includes_on_one_option_line(self, tmp_path):
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("-r more.txt -c constraints.txt\n")
        (tmp_path / "more.txt").write_text("httpx\n")
        (tmp_path / "constraints.txt").write_text("httpx<1\n")

        text = read_requirements_file_text(reqs)
        assert "httpx\n" in text
        assert "httpx<1\n" in text

    def test_symlink_includes_are_relative_to_supplied_path(self, tmp_path):
        directory = tmp_path / "shared"
        directory.mkdir()
        shared = directory / "requirements.txt"
        shared.write_text("-r more.txt\n")
        reqs = tmp_path / "requirements.txt"
        try:
            reqs.symlink_to(shared)
        except OSError:
            pytest.skip("Creating symlinks is unavailable")
        (tmp_path / "more.txt").write_text("httpx\n")

        assert "httpx\n" in read_requirements_file_text(reqs)


# ---------------------------------------------------------------------------
# read_requirements
# ---------------------------------------------------------------------------


class TestReadRequirements:
    def test_comments_and_blank_lines_skipped(self, tmp_path):
        """Returns only the requirements."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("# comment\n\nflet>=1.0  # inline\nhttpx\n")
        assert read_requirements(reqs) == ["flet>=1.0", "httpx"]

    def test_hash_options_removed(self, tmp_path):
        """Drops the options of a requirement, across continued lines."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet==1.0 \\\n  --hash=sha256:abc\n")
        assert read_requirements(reqs) == ["flet==1.0"]

    def test_requirement_includes_read_and_constraints_skipped(self, tmp_path):
        """Follows `-r` includes, but constraints don't install anything."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("flet\n-r more.txt\n-c constraints.txt\n")
        (tmp_path / "more.txt").write_text("httpx")
        (tmp_path / "constraints.txt").write_text("tabulate<1\n")
        assert read_requirements(reqs) == ["flet", "httpx"]

    def test_requirement_include_of_a_constraints_file_read(self, tmp_path):
        """Treats a `-r` include as requirements even inside a constraints file."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("-c constraints.txt\n")
        (tmp_path / "constraints.txt").write_text("-r local.txt\n")
        (tmp_path / "local.txt").write_text("flet @ file:///work/flet\n")
        assert read_requirements(reqs) == ["flet @ file:///work/flet"]

    def test_file_included_as_constraint_and_requirement_read(self, tmp_path):
        """Keeps the requirements of a file that is also a constraints file."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("-c shared.txt\n-r shared.txt\n")
        (tmp_path / "shared.txt").write_text("httpx\n")
        assert read_requirements(reqs) == ["httpx"]

    @pytest.mark.parametrize("encoding", ["utf-8-sig", "utf-16"])
    def test_byte_order_mark_decoded(self, tmp_path, encoding):
        """Reads files saved with a byte order mark, as pip does."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_bytes("flet>=1\nhttpx\n".encode(encoding))
        assert read_requirements(reqs) == ["flet>=1", "httpx"]

    def test_url_includes(self, tmp_path):
        """Reads `file:` includes, and returns the URL of any other include."""
        (tmp_path / "local.txt").write_text("httpx\n")
        reqs = tmp_path / "requirements.txt"
        reqs.write_text(
            f"-r {(tmp_path / 'local.txt').as_uri()}\n-r https://example.com/r.txt\n"
        )
        assert read_requirements(reqs) == ["https://example.com/r.txt", "httpx"]

    def test_windows_line_endings_normalized(self, tmp_path):
        """Gives the same text for a file with Windows line endings."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_bytes(b"flet>=1\r\nhttpx\r\n")
        assert read_requirements_file_text(reqs) == "flet>=1\nhttpx\n"
        assert read_requirements(reqs) == ["flet>=1", "httpx"]

    def test_editable_target_returned(self, tmp_path):
        """Returns the targets of `-e` options, and drops other options."""
        reqs = tmp_path / "requirements.txt"
        reqs.write_text("--no-cache-dir\n-e ../lib\n--editable=../other\n")
        assert read_requirements(reqs) == ["../lib", "../other"]


# ---------------------------------------------------------------------------
# pin_flet_dependencies
# ---------------------------------------------------------------------------


class TestPinFletDependencies:
    def test_range_pinned(self):
        """Narrows a range that allows the CLI's version."""
        assert pin_flet_dependencies(["flet >=1.0.5"], "1.1.0") == ["flet==1.1.0"]

    def test_extensions_pinned_and_others_untouched(self):
        """Pins packages released with `flet`, and no others."""
        result = pin_flet_dependencies(
            ["flet", "flet-charts", "flet_map>=1", "flet-third-party", "httpx<1"],
            "1.1.0",
        )
        assert result == [
            "flet==1.1.0",
            "flet-charts==1.1.0",
            "flet_map==1.1.0",
            "flet-third-party",
            "httpx<1",
        ]

    def test_extras_and_markers_kept(self):
        """Keeps what a requirement says besides its version."""
        result = pin_flet_dependencies(
            ["flet[all]>=1", "flet-audio; sys_platform == 'win32'"], "1.1.0"
        )
        assert result == [
            "flet[all]==1.1.0",
            'flet-audio==1.1.0; sys_platform == "win32"',
        ]

    @pytest.mark.parametrize(
        "dep", ["flet==0.86.3", "flet<1", "flet-charts==1.0.5", "flet!=1.1.0"]
    )
    def test_excluded_version_raises(self, dep):
        """Fails when a requirement rules out the CLI's version."""
        with pytest.raises(FletVersionConflictError, match="1.1.0"):
            pin_flet_dependencies([dep], "1.1.0")

    def test_excluded_version_with_marker_left_to_pip(self):
        """Keeps a conflicting requirement that may not apply to the target."""
        result = pin_flet_dependencies(
            ["flet>=1", "flet-audio<1; sys_platform == 'win32'"], "1.1.0"
        )
        assert result == ["flet==1.1.0", "flet-audio<1; sys_platform == 'win32'"]

    def test_prerelease_cli_version_allowed(self):
        """Treats the version of a pre-release CLI like any other."""
        assert pin_flet_dependencies(["flet>=1"], "1.1.0.dev4") == ["flet==1.1.0.dev4"]

    @pytest.mark.parametrize(
        "deps",
        [
            [],
            ["httpx"],
            ["flet-charts"],
            ["flet; sys_platform == 'win32'"],
            ["--no-cache-dir"],
        ],
    )
    def test_flet_added_when_not_installed_everywhere(self, deps):
        """Adds `flet` when no requirement installs it on every platform."""
        assert pin_flet_dependencies(deps, "1.1.0")[-1] == "flet==1.1.0"

    @pytest.mark.parametrize(
        "deps",
        [
            ["flet @ file:///src/flet", "flet-charts"],
            ["git+https://github.com/flet-dev/flet#egg=flet", "flet-charts"],
            ["../dist/flet-1.1.0.dev1-py3-none-any.whl", "flet-charts"],
            ["flet-1.0.5-py3-none-any.whl", "flet-charts"],
            ["../flet", "flet-charts"],
            ["..\\packages\\flet\\", "flet-charts"],
            [
                "git+https://github.com/flet-dev/flet@main"
                "#subdirectory=sdk/python/packages/flet",
                "flet-charts",
            ],
            ["https://example.com/flet-1.1.0.tar.gz?x=1", "flet-charts"],
        ],
    )
    def test_flet_from_a_location_left_alone(self, deps):
        """Doesn't touch the requirements when `flet` comes from a path or URL."""
        assert pin_flet_dependencies(deps, "1.1.0") == deps

    def test_flet_location_with_extras_or_marker_left_alone(self):
        """Recognizes a `flet` location followed by extras or a marker."""
        for entry in [
            "flet-1.0.5-py3-none-any.whl[all]",
            "../flet[all]",
            "./flet-1.0.5.tar.gz ; python_version >= '3.10'",
        ]:
            assert pin_flet_dependencies([entry], "1.1.0") == [entry]

    def test_url_include_may_provide_flet(self):
        """Doesn't add `flet` next to an include that can't be read."""
        deps = ["https://example.com/r.txt"]
        assert pin_flet_dependencies(deps, "1.1.0") == deps

    def test_other_location_may_provide_flet(self):
        """Doesn't add `flet` next to a path, which may install it."""
        assert pin_flet_dependencies(["../lib"], "1.1.0") == ["../lib"]

    def test_flet_prefixed_location_is_not_flet(self):
        """Doesn't mistake a path to another `flet-*` package for `flet`."""
        result = pin_flet_dependencies(["../flet-foo", "flet"], "1.1.0")
        assert result == ["../flet-foo", "flet==1.1.0"]

    def test_extension_from_a_location_kept(self):
        """Keeps an extension's own direct reference."""
        result = pin_flet_dependencies(["flet-charts @ file:///x", "flet"], "1.1.0")
        assert result == ["flet-charts @ file:///x", "flet==1.1.0"]

    def test_flet_packages_lists_every_package(self):
        """Lists every package in the repository's `packages` directory."""
        packages = Path(__file__).parents[2]
        assert {
            path.parent.name for path in packages.glob("*/pyproject.toml")
        } == FLET_PACKAGES


# ---------------------------------------------------------------------------
# requirements_use_hashes
# ---------------------------------------------------------------------------


class TestRequirementsUseHashes:
    @pytest.mark.parametrize(
        "text",
        ["flet==1.0 --hash=sha256:abc\n", "--require-hashes\nflet==1.0\n"],
    )
    def test_hash_options_detected(self, text):
        """Detects both ways of turning on hash-checking mode."""
        assert requirements_use_hashes(text)

    @pytest.mark.parametrize("text", ["flet>=1\n# add --hash later\n", "flet>=1\n"])
    def test_comments_ignored(self, text):
        """Doesn't take a comment for an option."""
        assert not requirements_use_hashes(text)


# ---------------------------------------------------------------------------
# override_dependencies
# ---------------------------------------------------------------------------


class TestOverrideDependencies:
    def test_same_package_replaced(self):
        """Replaces requirements of the same package, whatever its spelling."""
        assert override_dependencies(
            ["flet_charts>=1", "httpx", "../lib"], ["flet-charts", "rich"]
        ) == ["httpx", "../lib", "flet-charts", "rich"]
