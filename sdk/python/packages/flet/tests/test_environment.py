import os
from unittest.mock import patch

from flet.utils.environment import without_host_python_config

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
    env = without_host_python_config(HOST_ENV)

    assert "PYTHONPATH" not in env
    assert "PYTHONHOME" not in env
    assert "PYTHONEXECUTABLE" not in env


def test_user_site_packages_is_disabled():
    # Opt-out, so it must be set rather than removed - a host user site dir
    # matching the embedded interpreter's version leaks in otherwise.
    assert without_host_python_config(HOST_ENV)["PYTHONNOUSERSITE"] == "1"


def test_build_env_is_preserved():
    env = without_host_python_config(HOST_ENV)

    for name in (
        "PATH",
        "FLET_TEST_FLUTTER_EXE",
        "FLET_TEST_DEVICE_MODE",
        "SERIOUS_PYTHON_SITE_PACKAGES",
        "SP_NATIVE_SET",
    ):
        assert env[name] == HOST_ENV[name]


def test_missing_vars_are_not_an_error():
    assert without_host_python_config({"PATH": "/usr/bin"}) == {
        "PATH": "/usr/bin",
        "PYTHONNOUSERSITE": "1",
    }


def test_source_mapping_is_not_mutated():
    source = dict(HOST_ENV)
    without_host_python_config(source)

    assert source == HOST_ENV


def test_defaults_to_os_environ():
    with patch.dict(os.environ, HOST_ENV, clear=True):
        env = without_host_python_config()

        assert "PYTHONPATH" not in env
        assert env["PATH"] == HOST_ENV["PATH"]
        # The live environment of the *host* process is left alone.
        assert os.environ["PYTHONPATH"] == HOST_ENV["PYTHONPATH"]
        assert "PYTHONNOUSERSITE" not in os.environ
