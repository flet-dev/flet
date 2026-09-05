"""Tests concerning the low-level compositing primitives."""

import hashlib

import pytest
from flet_platform_assets._imaging import (
    alpha_extent,
    density_size,
    has_transparent_corners,
    looks_pre_shaped,
    parse_hex_color,
    place,
    save_ico,
    scale_to_fit,
    superellipse_mask,
)
from PIL import Image


class TestSuperellipseMask:
    """The mask went from numpy to a pure-Pillow row loop.

    Both the brand assets and every generated macOS icon are composed through
    it, so a drift here silently restyles every shipped icon. The hash pins
    the exact pixels the numpy version produced.
    """

    def test_golden_hash(self):
        mask = superellipse_mask(256, 5.0)
        digest = hashlib.sha256(mask.tobytes()).hexdigest()
        assert digest == GOLDEN_MASK_256_N5

    def test_is_symmetric(self):
        """Asymmetry would mean the boundary correction favours one side."""
        mask = superellipse_mask(64, 5.0)
        assert mask.tobytes() == mask.transpose(Image.FLIP_LEFT_RIGHT).tobytes()
        assert mask.tobytes() == mask.transpose(Image.FLIP_TOP_BOTTOM).tobytes()

    def test_corners_clear_and_centre_solid(self):
        mask = superellipse_mask(128, 5.0)
        assert mask.getpixel((0, 0)) == 0
        assert mask.getpixel((127, 127)) == 0
        assert mask.getpixel((64, 64)) == 255


class TestPremultipliedDownscale:
    """The fix for the halo bug in flutter_native_splash.

    Averaging non-premultiplied alpha pulls the RGB of fully transparent
    pixels into the visible edge. Padding an opaque white square with
    transparent *black* is the case that exposes it: a naive resize darkens
    the edge, a premultiplied one leaves it white.
    """

    def test_transparent_black_padding_does_not_darken_edges(self):
        canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        canvas.paste(Image.new("RGBA", (256, 256), (255, 255, 255, 255)), (128, 128))

        scaled = scale_to_fit(canvas, 128)

        opaque = [
            px[:3] for px in scaled.convert("RGBA").get_flattened_data() if px[3] == 255
        ]
        assert opaque, "expected the square to survive the downscale"
        assert min(min(px) for px in opaque) > 250, (
            "fully opaque pixels darkened, so alpha was averaged unpremultiplied"
        )


class TestLooksPreShaped:
    """Distinguishes an already-shaped icon from an ordinary logo.

    Transparent corners alone cannot tell them apart - nearly every logo with
    an alpha channel has them - so the check also requires a filled,
    near-square tile.
    """

    def test_shaped_tile_is_detected(self):
        tile = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        art = Image.new("RGBA", (410, 410), (255, 0, 85, 255))
        art.putalpha(superellipse_mask(410, 5.0))
        tile.alpha_composite(art, (51, 51))
        assert looks_pre_shaped(tile) is True

    def test_tall_logo_is_not_detected(self):
        """A logo taller than it is wide is not a tile, whatever its corners."""
        logo = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        logo.paste(Image.new("RGBA", (200, 400), (255, 0, 85, 255)), (156, 56))
        assert has_transparent_corners(logo) is True
        assert looks_pre_shaped(logo) is False

    def test_opaque_square_is_not_detected(self):
        """Scores 1.0 on aspect and fill, but wants a shape applied."""
        square = Image.new("RGBA", (512, 512), (255, 0, 85, 255))
        assert looks_pre_shaped(square) is False

    def test_fully_transparent_is_not_detected(self):
        assert looks_pre_shaped(Image.new("RGBA", (64, 64), (0, 0, 0, 0))) is False


class TestPlace:
    """Placement either flattens onto a background or keeps alpha."""

    def test_background_flattens_to_rgb(self):
        art = Image.new("RGBA", (32, 32), (255, 0, 85, 255))
        assert place(art, 64, bg=(255, 255, 255)).mode == "RGB"

    def test_without_background_keeps_alpha(self):
        art = Image.new("RGBA", (32, 32), (255, 0, 85, 255))
        out = place(art, 64)
        assert out.mode == "RGBA"
        assert out.getpixel((0, 0))[3] == 0


class TestSaveIco:
    """Pillow's ICO writer silently drops sizes larger than the base image."""

    def test_every_requested_size_survives(self, tmp_path):
        sizes = (16, 32, 48, 256)
        images = {s: Image.new("RGBA", (s, s), (255, 0, 85, 255)) for s in sizes}
        path = tmp_path / "app_icon.ico"

        save_ico(path, images)

        with Image.open(path) as ico:
            assert sorted(w for w, _ in ico.ico.sizes()) == sorted(sizes)


class TestDensitySize:
    """Reproduces Dart's `w * density ~/ 4`, which truncates the product."""

    @pytest.mark.parametrize(
        ("width", "density", "expected"),
        [(1024, 1, 256), (1024, 2, 512), (1024, 3, 768), (1024, 4, 1024), (100, 3, 75)],
    )
    def test_matches_dart_truncation(self, width, density, expected):
        assert density_size(width, width, density)[0] == expected


class TestAlphaExtent:
    """How far opaque content reaches from the centre, as a fraction."""

    def test_fully_opaque_has_no_meaningful_extent(self):
        """`None`, not 1.0 - and that is what keeps the Android safe-zone
        warning from firing on every opaque square, where it would mean
        nothing."""
        assert alpha_extent(Image.new("RGBA", (64, 64), (0, 0, 0, 255))) is None

    def test_artwork_touching_an_edge_is_one(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        img.paste(Image.new("RGBA", (64, 32), (0, 0, 0, 255)), (0, 16))
        assert alpha_extent(img) == 1.0

    def test_centred_half_is_half(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        img.paste(Image.new("RGBA", (32, 32), (0, 0, 0, 255)), (16, 16))
        assert alpha_extent(img) == pytest.approx(0.5, abs=0.02)

    def test_fully_transparent_is_zero(self):
        assert alpha_extent(Image.new("RGBA", (64, 64), (0, 0, 0, 0))) == 0.0


class TestParseHexColor:
    """Colours arrive from `pyproject.toml` as strings."""

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("#ffffff", (255, 255, 255)),
            ("ffffff", (255, 255, 255)),
            ("#FF0055", (255, 0, 85)),
            ("#fff", (255, 255, 255)),
        ],
    )
    def test_accepts_common_forms(self, text, expected):
        assert parse_hex_color(text) == expected

    def test_rejects_nonsense(self):
        with pytest.raises(ValueError):
            parse_hex_color("not-a-colour")


GOLDEN_MASK_256_N5 = "b5292727be0257653e20255acaedeaf313b36f3564bf840dfdedac932a3f83ef"
