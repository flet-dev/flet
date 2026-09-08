"""Options, specs and results shared by the icon and splash renderers."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from ._imaging import WHITE

__all__ = [
    "AssetSpec",
    "IconOptions",
    "RenderResult",
    "RenderedAsset",
    "SplashOptions",
    "Target",
]


@dataclass(frozen=True)
class Target:
    """One file to produce.

    Args:
        relative_path: Destination, relative to the Flutter project root.
        size: Side length in pixels.
        opaque: Flatten onto the options' background and emit mode `RGB`.
            Used where a platform rejects an alpha channel.
        frame: Name of a rule in `FRAMING` to apply to this file alone, for a
            target whose mask differs from the rest of its platform. The web
            needs all three cases at once: a favicon is never masked, a
            maskable icon is cropped to a circle, and an apple-touch icon
            becomes an iOS home-screen icon.
    """

    relative_path: str
    size: int
    opaque: bool = False
    frame: str | None = None


@dataclass(frozen=True)
class AssetSpec:
    """Which files a platform wants, and at what sizes.

    Defaults describe a stock Flutter project, so a caller with no project on
    disk - a settings screen previewing icons, for instance - gets sensible
    output. `flet build` overrides them with the list the rendered project
    actually declares, so it never writes a file the project does not
    reference.

    Args:
        targets: Files to produce for this platform.
        ico_sizes: Entry sizes for a Windows `.ico`, if any.
    """

    targets: Sequence[Target] = ()
    ico_sizes: Sequence[int] = ()


@dataclass(frozen=True)
class IconOptions:
    """How to render app icons.

    Args:
        background: Colour behind artwork wherever alpha cannot survive. It
            fills three places: the iOS flatten, which is not optional because
            the App Store rejects an alpha channel; the macOS tile; and the
            opaque web icons - the two maskables and apple-touch. A
            transparent source is expected, so this is the colour the user
            actually sees on Apple platforms.
        macos_style: `"auto"` composes Apple's inset squircle and drop shadow
            unless the source already looks shaped; `"grid"` always composes
            it; `"raw"` places the artwork full-bleed, for a source that has
            its own shape baked in.
        application_id: Linux desktop entry id, used to name the hicolor
            icons.
    """

    background: tuple[int, int, int] = WHITE
    macos_style: str = "auto"
    application_id: str = "com.example.app"


@dataclass(frozen=True)
class SplashOptions:
    """How to render splash screens.

    Args:
        color: Light-mode background, as `#rrggbb`.
        dark_color: Dark-mode background.
        icon_background: Background behind the Android 12 splash icon.
            Setting it changes that icon's canvas from 1152 to 960, per the
            platform spec.
        icon_dark_background: Dark-mode variant of `icon_background`.
        icon_fit: How the Android 12 splash icon is placed. `"contain"` fits
            the artwork inside the circle Android guarantees is visible;
            `"none"` passes it through untouched, which is what
            flutter_native_splash did.
    """

    color: str = "#ffffff"
    dark_color: str = "#222222"
    icon_background: str | None = None
    icon_dark_background: str | None = None
    icon_fit: str = "contain"


@dataclass(frozen=True)
class RenderedAsset:
    """One produced image, not yet written anywhere.

    Args:
        relative_path: Destination, relative to the Flutter project root.
        image: The rendered image.
    """

    relative_path: str
    image: Image.Image

    @property
    def path(self) -> Path:
        """`relative_path` as a `Path`."""
        return Path(self.relative_path)


@dataclass
class RenderResult:
    """Everything a render produced, including anything worth reporting.

    Diagnostics are returned rather than printed so the caller decides how to
    surface them - a build logs them, a settings screen shows them next to
    the offending icon.

    Args:
        assets: The rendered images.
        warnings: Human-readable notes about the source or the result.
        ico: Windows `.ico` entries, keyed by destination then pixel size.
            Kept apart from `assets` because an `.ico` is many images in one
            file.
        stale: Files a previous generator left behind that this render
            replaces. Cookiecutter overwrites but never deletes, so an asset
            that stops being generated - a dark splash after dark mode is
            turned off, a `.webp` after the source changes - would otherwise
            keep being served.
    """

    assets: list[RenderedAsset] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ico: dict[str, dict[int, Image.Image]] = field(default_factory=dict)
    stale: list[str] = field(default_factory=list)

    def add(self, relative_path: str, image: Image.Image) -> None:
        """Append a rendered asset."""
        self.assets.append(RenderedAsset(relative_path, image))

    def warn(self, message: str) -> None:
        """Record a diagnostic."""
        self.warnings.append(message)
