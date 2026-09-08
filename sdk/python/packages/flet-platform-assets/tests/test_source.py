"""Tests concerning loading and normalising a user's source image.

These cover the awkward inputs a real user supplies - an EXIF-rotated phone
photo, a palette PNG, an animated GIF, a banner that is not square.
"""

import pytest
from flet_platform_assets import SourceError, load_source, square
from flet_platform_assets._source import MAX_SOURCE_SIZE
from PIL import Image


def save(img: Image.Image, path, **kwargs) -> str:
    img.save(path, **kwargs)
    return str(path)


class TestLoadSource:
    """Everything downstream assumes a square-ish RGBA image."""

    def test_rgba_png_round_trips(self, tmp_path):
        path = save(
            Image.new("RGBA", (512, 512), (255, 0, 85, 255)), tmp_path / "i.png"
        )
        img, pre_rendered = load_source(path)
        assert img.mode == "RGBA"
        assert img.size == (512, 512)
        assert pre_rendered is False

    def test_palette_png_is_converted(self, tmp_path):
        """A palette source would otherwise composite as mode P."""
        path = save(
            Image.new("RGB", (256, 256), (255, 0, 85)).convert("P"), tmp_path / "p.png"
        )
        img, _ = load_source(path)
        assert img.mode == "RGBA"

    def test_cmyk_jpeg_is_converted(self, tmp_path):
        path = save(Image.new("CMYK", (256, 256), (0, 255, 200, 0)), tmp_path / "c.jpg")
        img, _ = load_source(path)
        assert img.mode == "RGBA"

    def test_animated_gif_uses_the_first_frame(self, tmp_path):
        first = Image.new("RGB", (64, 64), (255, 0, 85))
        second = Image.new("RGB", (64, 64), (0, 0, 255))
        path = tmp_path / "a.gif"
        first.save(path, save_all=True, append_images=[second])
        img, _ = load_source(path)
        assert img.mode == "RGBA"
        assert img.getpixel((0, 0))[:3] == (255, 0, 85)

    def test_oversized_source_is_reduced_once(self, tmp_path):
        path = save(
            Image.new("RGBA", (4096, 4096), (255, 0, 85, 255)), tmp_path / "big.png"
        )
        img, _ = load_source(path)
        assert max(img.size) == MAX_SOURCE_SIZE

    def test_ico_yields_its_largest_frame_and_is_pre_rendered(self, tmp_path):
        path = tmp_path / "i.ico"
        Image.new("RGBA", (256, 256), (255, 0, 85, 255)).save(
            path, sizes=[(16, 16), (256, 256)]
        )
        img, pre_rendered = load_source(path)
        assert pre_rendered is True
        assert img.size == (256, 256)

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(SourceError, match="not found"):
            load_source(tmp_path / "nope.png")

    def test_non_image_raises(self, tmp_path):
        path = tmp_path / "x.png"
        path.write_text("this is not a png")
        with pytest.raises(SourceError, match="could not read"):
            load_source(path)


class TestSquare:
    """Padding rather than stretching or cropping: neither loses artwork."""

    def test_already_square_is_untouched(self):
        img = Image.new("RGBA", (128, 128))
        out, warning = square(img)
        assert out is img
        assert warning is None

    def test_banner_is_padded_and_centred(self):
        img = Image.new("RGBA", (200, 100), (255, 0, 85, 255))
        out, warning = square(img)
        assert out.size == (200, 200)
        assert out.getpixel((100, 100))[3] == 255
        assert out.getpixel((100, 5))[3] == 0
        assert "not square" in warning
