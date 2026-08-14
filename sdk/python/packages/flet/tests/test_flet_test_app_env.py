import os
from unittest.mock import patch

from flet.testing.flet_test_app import _flutter_subprocess_env

# A host environment as an IDE-launched pytest run sees it: PyCharm's debugger
# and sitecustomize helpers on PYTHONPATH, a Homebrew interpreter's PYTHONHOME,
# plus the variables `flet test` sets for the native build phase.
HOST_ENV = {
    "PATH": "/usr/local/bin:/usr/bin",
    "PYTHONPATH": "/Applications/PyCharm.app/Contents/plugins/python/helpers/pydev",
    "PYTHONHOME": "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework",
    "PYTHONEXECUTABLE": "/opt/homebrew/bin/python3.13",
    "FLET_TEST_FLUTTER_EXE": "/opt/flutter/bin/flutter",
    "FLET_TEST_DEVICE_MODE": "1",
    "SERIOUS_PYTHON_SITE_PACKAGES": "/tmp/app/site-packages",
    "SP_NATIVE_SET": "1",
}


def test_host_python_config_is_stripped():
    with patch.dict(os.environ, HOST_ENV, clear=True):
        env = _flutter_subprocess_env()

    assert "PYTHONPATH" not in env
    assert "PYTHONHOME" not in env
    assert "PYTHONEXECUTABLE" not in env


def test_user_site_packages_is_disabled():
    # Opt-out, so it must be set rather than removed - a host user site dir
    # matching the embedded interpreter's version leaks in otherwise.
    with patch.dict(os.environ, HOST_ENV, clear=True):
        assert _flutter_subprocess_env()["PYTHONNOUSERSITE"] == "1"


def test_build_env_is_preserved():
    with patch.dict(os.environ, HOST_ENV, clear=True):
        env = _flutter_subprocess_env()

    for name in (
        "PATH",
        "FLET_TEST_FLUTTER_EXE",
        "FLET_TEST_DEVICE_MODE",
        "SERIOUS_PYTHON_SITE_PACKAGES",
        "SP_NATIVE_SET",
    ):
        assert env[name] == HOST_ENV[name]


def test_missing_vars_are_not_an_error():
    with patch.dict(os.environ, {"PATH": "/usr/bin"}, clear=True):
        env = _flutter_subprocess_env()

    assert env == {"PATH": "/usr/bin", "PYTHONNOUSERSITE": "1"}


def test_host_environ_is_not_mutated():
    with patch.dict(os.environ, HOST_ENV, clear=True):
        _flutter_subprocess_env()

        assert os.environ["PYTHONPATH"] == HOST_ENV["PYTHONPATH"]
        assert os.environ["PYTHONHOME"] == HOST_ENV["PYTHONHOME"]
        assert "PYTHONNOUSERSITE" not in os.environ
