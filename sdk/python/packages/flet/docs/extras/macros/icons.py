import json
from pathlib import Path


def render_icon_members(icon_set: str = "material") -> str:
    controls_dir = Path(__file__).resolve().parents[3] / "src" / "flet" / "controls"

    if icon_set == "material":
        json_path = controls_dir / "material" / "icons.json"
        symbol = "ft.Icons"
        xref_prefix = "flet.Icons"
    elif icon_set == "cupertino":
        json_path = controls_dir / "cupertino" / "cupertino_icons.json"
        symbol = "ft.CupertinoIcons"
        xref_prefix = "flet.CupertinoIcons"
    else:
        raise ValueError("icon_set must be either 'material' or 'cupertino'")

    names = sorted(json.loads(json_path.read_text(encoding="utf-8")).keys())[:100]

    lines = [
        f'<a id="{xref_prefix}"></a>',
    ]

    for name in names:
        lines.append(f'<a id="{xref_prefix}.{name}"></a>')
        lines.append(f"### `{symbol}.{name}`")
        lines.append("")

    return "\n".join(lines)
