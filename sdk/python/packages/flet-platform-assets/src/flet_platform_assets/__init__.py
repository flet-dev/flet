"""Generate app icons and splash screens for every platform Flet builds for.

Rendering is separate from writing. :func:`render_icons` is pure - it takes an
image and returns images, without touching the filesystem or emitting log
output - so a UI can preview results before anything is built. :func:`write`
is the only function that persists anything.

Diagnostics are data: anything worth telling the user lands in
:attr:`RenderResult.warnings` rather than being printed, so the caller decides
how to surface it.

    >>> from flet_platform_assets import load_source, render_icons, write
    >>> source, pre_rendered = load_source("assets/icon.png")
    >>> result = render_icons(source, platform="web", pre_rendered=pre_rendered)
    >>> [a.relative_path for a in result.assets][:2]
    ['web/favicon.png', 'web/icons/Icon-192.png']
"""

from ._icons import (
    ANDROID_ADAPTIVE_SIZES,
    ANDROID_MIPMAP_SIZES,
    DEFAULT_SPECS,
    LINUX_HICOLOR_SIZES,
    WINDOWS_ICO_SIZES,
    render_icons,
    web_targets_from_manifest,
)
from ._models import (
    AssetSpec,
    IconOptions,
    RenderedAsset,
    RenderResult,
    SplashOptions,
    Target,
)
from ._source import SourceError, load_source, square
from ._write import write

__all__ = [
    "ANDROID_ADAPTIVE_SIZES",
    "ANDROID_MIPMAP_SIZES",
    "AssetSpec",
    "DEFAULT_SPECS",
    "IconOptions",
    "LINUX_HICOLOR_SIZES",
    "RenderResult",
    "RenderedAsset",
    "SourceError",
    "SplashOptions",
    "Target",
    "WINDOWS_ICO_SIZES",
    "load_source",
    "render_icons",
    "square",
    "web_targets_from_manifest",
    "write",
]
