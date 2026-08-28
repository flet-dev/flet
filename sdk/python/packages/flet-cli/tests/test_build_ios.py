"""Tests for `flet build ipa`."""

import argparse
from pathlib import Path

from flet_cli.commands.build import Command


def make_command(tmp_path: Path, target_platform: str = "ipa") -> Command:
    """
    Build a Command instance for iOS build tests.

    Uses the real constructor so `platforms` — and the status texts the
    build actually reports with — are the production ones.

    Args:
        tmp_path: Test-scoped directory; receives out_dir and flutter_dir.
        target_platform: Platform whose behaviour is under test.

    Returns:
        A command with empty output directories, ready for artifacts to be
            placed into them.
    """
    cmd = Command(argparse.ArgumentParser())
    cmd.target_platform = target_platform
    cmd.out_dir = tmp_path / "out"
    cmd.flutter_dir = tmp_path / "flutter"
    for directory in (cmd.out_dir, cmd.flutter_dir):
        directory.mkdir(parents=True, exist_ok=True)
    return cmd


# ---------------------------------------------------------------------------
# build output reporting
# ---------------------------------------------------------------------------


class TestBuildOutput:
    """What the command reports having produced.

    An unsigned build yields only an `.xcarchive`, so the reported artifact
    comes from what is on disk rather than from the target's usual output.
    """

    def test_reports_xcarchive_when_no_ipa_produced(self, tmp_path):
        """An unsigned build must not announce an .ipa that was never written."""
        cmd = make_command(tmp_path)
        (cmd.out_dir / "MyApp.xcarchive").mkdir()

        assert cmd.built_ipa() is False
        assert cmd.describe_build_output() == ".xcarchive (Xcode archive) for iOS"

    def test_reports_ipa_when_produced(self, tmp_path):
        """A signed build keeps the platform's normal status text."""
        cmd = make_command(tmp_path)
        (cmd.out_dir / "MyApp.ipa").write_bytes(b"")

        assert cmd.built_ipa() is True
        assert cmd.describe_build_output() == cmd.platforms["ipa"]["status_text"]

    def test_ipa_found_before_outputs_are_copied(self, tmp_path):
        """The check also runs right after the build, from the Flutter project."""
        cmd = make_command(tmp_path)
        ipa_dir = cmd.flutter_dir / "build" / "ios" / "ipa"
        ipa_dir.mkdir(parents=True)
        (ipa_dir / "MyApp.ipa").write_bytes(b"")

        assert cmd.built_ipa() is True

    def test_other_platforms_keep_their_status_text(self, tmp_path):
        """The .ipa-specific check must not leak into other targets."""
        cmd = make_command(tmp_path, target_platform="macos")
        assert cmd.describe_build_output() == cmd.platforms["macos"]["status_text"]
