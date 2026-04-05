"""Tests for project_dependencies module."""

import pytest

from flet_cli.utils.project_dependencies import (
    get_poetry_dependencies,
    get_project_dependencies,
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
