from types import SimpleNamespace

import pytest

from flet import pytest_plugin


class _Reporter:
    def __init__(self):
        self.newlines = 0

    def ensure_newline(self):
        self.newlines += 1


def _config(capture: str, reporter):
    return SimpleNamespace(
        getoption=lambda name, default=None: capture if name == "capture" else default,
        pluginmanager=SimpleNamespace(
            get_plugin=lambda name: reporter if name == "terminalreporter" else None
        ),
    )


@pytest.fixture
def reporter(monkeypatch):
    reporter = _Reporter()
    monkeypatch.setattr(pytest_plugin, "_config", _config("no", reporter))
    return reporter


def test_ensure_newline_ends_progress_line_when_not_capturing(reporter):
    pytest_plugin.ensure_newline()
    assert reporter.newlines == 1


@pytest.mark.parametrize("capture", ["fd", "sys", "tee-sys"])
def test_ensure_newline_keeps_progress_line_when_capturing(monkeypatch, capture):
    reporter = _Reporter()
    monkeypatch.setattr(pytest_plugin, "_config", _config(capture, reporter))
    pytest_plugin.ensure_newline()
    assert reporter.newlines == 0


def test_ensure_newline_outside_pytest(monkeypatch):
    monkeypatch.setattr(pytest_plugin, "_config", None)
    pytest_plugin.ensure_newline()  # no error
