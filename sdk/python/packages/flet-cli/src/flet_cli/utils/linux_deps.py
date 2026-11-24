"""Canonical Linux apt dependencies used by Flet workflows."""

from typing import Final

linux_dependencies: Final[tuple[str, ...]] = (
    "binutils",
    "clang",
    "cmake",
    "gstreamer1.0-alsa",
    "gstreamer1.0-gl",
    "gstreamer1.0-gtk3",
    "gstreamer1.0-libav",
    "gstreamer1.0-plugins-bad",
    "gstreamer1.0-plugins-base",
    "gstreamer1.0-plugins-good",
    "gstreamer1.0-plugins-ugly",
    "gstreamer1.0-pulseaudio",
    "gstreamer1.0-qt5",
    "gstreamer1.0-tools",
    "gstreamer1.0-x",
    "libasound2-dev",
    "libgstreamer-plugins-bad1.0-dev",
    "libgstreamer-plugins-base1.0-dev",
    "libgstreamer1.0-dev",
    "libgtk-3-dev",
    "libmpv-dev",
    "libsecret-1-0",
    "libsecret-1-dev",
    "libunwind-dev",
    "lld",
    "llvm",
    "mpv",
    "ninja-build",
    "pkg-config",
)
"""Linux apt packages required to build Flet Linux apps and client binaries."""
