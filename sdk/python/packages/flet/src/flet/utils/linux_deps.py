"""Canonical Linux apt dependency sets used by Flet workflows."""

from typing import Final

linux_build_dependencies: Final[tuple[str, ...]] = (
    "clang",
    "ninja-build",
    "libgtk-3-dev",
    "libasound2-dev",
    "libmpv-dev",
    "mpv",
    "libgstreamer1.0-dev",
    "libgstreamer-plugins-base1.0-dev",
    "libgstreamer-plugins-bad1.0-dev",
    "gstreamer1.0-plugins-base",
    "gstreamer1.0-plugins-good",
    "gstreamer1.0-plugins-bad",
    "gstreamer1.0-plugins-ugly",
    "gstreamer1.0-libav",
    "gstreamer1.0-tools",
    "gstreamer1.0-x",
    "gstreamer1.0-alsa",
    "gstreamer1.0-gl",
    "gstreamer1.0-gtk3",
    "gstreamer1.0-qt5",
    "gstreamer1.0-pulseaudio",
    "pkg-config",
    "libsecret-1-0",
    "libsecret-1-dev",
)
"""Linux apt packages required to build a Flet Linux app."""

linux_build_dependencies_apt: Final[str] = " ".join(linux_build_dependencies)
"""`linux_build_dependencies` as a shell-ready, space-separated string."""

linux_client_dependencies: Final[tuple[str, ...]] = (
    "lld",
    "llvm",
    "binutils",
    "clang",
    "cmake",
    "ninja-build",
    "pkg-config",
    "libgtk-3-dev",
    "libasound2-dev",
    "libunwind-dev",
    "libsecret-1-0",
    "libsecret-1-dev",
    "libmpv-dev",
    "mpv",
    "libgstreamer1.0-dev",
    "libgstreamer-plugins-base1.0-dev",
    "libgstreamer-plugins-bad1.0-dev",
    "gstreamer1.0-plugins-base",
    "gstreamer1.0-plugins-good",
    "gstreamer1.0-plugins-bad",
    "gstreamer1.0-plugins-ugly",
    "gstreamer1.0-libav",
    "gstreamer1.0-tools",
    "gstreamer1.0-x",
    "gstreamer1.0-alsa",
    "gstreamer1.0-gl",
    "gstreamer1.0-gtk3",
    "gstreamer1.0-qt5",
    "gstreamer1.0-pulseaudio",
)
"""Linux apt packages used to build Flet Linux client binaries in CI."""


linux_client_dependencies_apt: Final[str] = " ".join(linux_client_dependencies)
"""`linux_client_dependencies` as a shell-ready, space-separated string."""
