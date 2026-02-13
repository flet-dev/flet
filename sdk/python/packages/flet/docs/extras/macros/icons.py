import json
from pathlib import Path


def _material_ligature_and_class(name: str) -> tuple[str, str]:
    if name.endswith("_OUTLINED"):
        return name[: -len("_OUTLINED")].lower(), "flet-icon-preview-material-outlined"
    if name.endswith("_ROUNDED"):
        return name[: -len("_ROUNDED")].lower(), "flet-icon-preview-material-rounded"
    if name.endswith("_SHARP"):
        return name[: -len("_SHARP")].lower(), "flet-icon-preview-material-sharp"
    return name.lower(), "flet-icon-preview-material"


def render_icon_members(icon_set: str = "material") -> str:
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
        f'<a id="{xref_prefix}"></a>',
    ]

    for name in names:
        value = icon_map[name]
        lines.append(f'<a id="{xref_prefix}.{name}"></a>')
        lines.append(f"### `{name} = {value}`")
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
                    lines.append(
                        f'<span class="flet-icon-preview flet-icon-preview-cupertino" '
                        f'title="{name}">{chr(codepoint)}</span>'
                    )
        lines.append("")

    return "\n".join(lines)
