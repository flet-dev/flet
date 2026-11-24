import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "benchmark: manual performance benchmark")


def pytest_collection_modifyitems(config, items):
    # Auto-skip benchmark tests unless explicitly selected with -m benchmark
    if "benchmark" not in (config.getoption("-m") or ""):
        skip = pytest.mark.skip(reason="benchmark — run with: pytest -m benchmark -s")
        for item in items:
            if "benchmark" in item.keywords:
                item.add_marker(skip)
