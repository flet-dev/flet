import json
from pathlib import Path
from typing import Literal


def _material_ligature_and_class(name: str) -> tuple[str, str]:
    """
    Convert a Material icon constant name into preview text and CSS class.

    Args:
        name: Material icon enum member name (for example `HOME_OUTLINED`).

    Returns:
        A tuple of `(ligature_text, css_class)` used by docs icon preview HTML.
    """

    if name.endswith("_OUTLINED"):
        return name[: -len("_OUTLINED")].lower(), "flet-icon-preview-material-outlined"
    if name.endswith("_ROUNDED"):
        return name[: -len("_ROUNDED")].lower(), "flet-icon-preview-material-rounded"
    if name.endswith("_SHARP"):
        return name[: -len("_SHARP")].lower(), "flet-icon-preview-material-sharp"
    return name.lower(), "flet-icon-preview-material"


def render_icon_members(icon_set: str = Literal["material", "cupertino"]) -> str:
    """
    Render markdown sections for all icon members in a selected icon set.

    Generates headings with stable anchor IDs plus inline HTML previews used by
    `types/icons.md` and `types/cupertinoicons.md`.

    Args:
        icon_set: Icon collection to render (`"material"` or `"cupertino"`).

    Returns:
        Markdown/HTML content listing icon names, encoded values, and previews.

    Raises:
        ValueError: If `icon_set` is not `"material"` or `"cupertino"`.
    """

    # Resolve control asset files relative to this docs macro module.
    controls_dir = Path(__file__).resolve().parents[3] / "src" / "flet" / "controls"

    if icon_set == "material":
        json_path = controls_dir / "material" / "icons.json"
        xref_prefix = "flet.Icons"
        render_preview = True
        codepoint_map = {}
    elif icon_set == "cupertino":
        json_path = controls_dir / "cupertino" / "cupertino_icons.json"
        codepoint_json_path = (
            controls_dir / "cupertino" / "cupertino_icons_codepoints.json"
        )
        xref_prefix = "flet.CupertinoIcons"
        render_preview = True
        # Flet stores packed icon IDs; docs previews need real Cupertino font codepoints
        codepoint_map = json.loads(codepoint_json_path.read_text(encoding="utf-8"))
    else:
        raise ValueError("icon_set must be either 'material' or 'cupertino'")

    icon_map = json.loads(json_path.read_text(encoding="utf-8"))
    names = sorted(icon_map.keys())

    lines = [
        # top-level anchor so xrefs to flet.Icons / flet.CupertinoIcons resolve
        f'<a id="{xref_prefix}"></a>',
    ]

    for name in names:
        value = icon_map[name]
        # Each icon gets its own anchor (for example: flet.Icons.ADD).
        heading_id = f"{xref_prefix}.{name}"
        lines.append(f"### `{name} = {value}` {{ #{heading_id} }}")
        if render_preview:
            if icon_set == "material":
                ligature, preview_class = _material_ligature_and_class(name)
                lines.append(
                    f'<span class="flet-icon-preview {preview_class}" '
                    f'title="{name}">{ligature}</span>'
                )
            else:
                codepoint = codepoint_map.get(name)
                if codepoint is None:
                    lines.append(
                        '<span class="flet-icon-preview-missing">'
                        "preview unavailable</span>"
                    )
                else:
                    # Use the real codepoint character for Cupertino previews.
                    lines.append(
                        f'<span class="flet-icon-preview flet-icon-preview-cupertino" '
                        f'title="{name}">{chr(codepoint)}</span>'
                    )
        lines.append("")

    return "\n".join(lines)
