import json
import re
from pathlib import Path
from typing import Optional

from flet.controls.types import WebRenderer


def patch_index_html(
    index_path: str,
    base_href: str,
    websocket_endpoint_path: Optional[str] = None,
    app_name: Optional[str] = None,
    app_description: Optional[str] = None,
    pyodide: bool = False,
    pyodide_pre: bool = False,
    pyodide_script_path: str = "",
    web_renderer: WebRenderer = WebRenderer.AUTO,
    use_color_emoji: bool = False,
    route_url_strategy: str = "path",
    no_cdn: bool = False,
):
    with open(index_path, encoding="utf-8") as f:
        index = f.read()

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        pyodideCode = f"""
        <script>
            var micropipIncludePre = {str(pyodide_pre).lower()};
            var pythonModuleName = "{module_name}";
        </script>
        """
        index = index.replace("<!-- pyodideCode -->", pyodideCode)
    index = index.replace("%FLET_WEB_PYODIDE%", str(pyodide).lower())
    index = index.replace(
        "<!-- webRenderer -->",
        f'<script>webRenderer="{web_renderer.value}";</script>',
    )
    index = index.replace(
        "<!-- useColorEmoji -->",
        f"<script>useColorEmoji={str(use_color_emoji).lower()};</script>",
    )
    index = index.replace("%FLET_ROUTE_URL_STRATEGY%", route_url_strategy)

    index = index.replace(
        "<!-- noCdn -->",
        f"<script>noCdn={str(no_cdn).lower()};</script>",
    )

    if base_href:
        base_url = base_href.strip("/").strip()
        index = index.replace(
            '<base href="/">',
            '<base href="{}">'.format("/" if base_url == "" else f"/{base_url}/"),
        )
    if websocket_endpoint_path:
        index = re.sub(
            r"\<meta name=\"flet-websocket-endpoint-path\" content=\"(.+)\">",
            rf'<meta name="flet-websocket-endpoint-path" '
            f'content="{websocket_endpoint_path}">',
            index,
        )
    if app_name:
        index = re.sub(
            r"\<meta name=\"apple-mobile-web-app-title\" content=\"(.+)\">",
            rf'<meta name="apple-mobile-web-app-title" content="{app_name}">',
            index,
        )
        index = re.sub(
            r"\<title>(.+)</title>",
            rf"<title>{app_name}</title>",
            index,
        )
    if app_description:
        index = re.sub(
            r"\<meta name=\"description\" content=\"(.+)\">",
            rf'<meta name="description" content="{app_description}">',
            index,
        )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index)


def patch_manifest_json(
    manifest_path: str,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
    background_color: Optional[str] = None,
    theme_color: Optional[str] = None,
):
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.loads(f.read())

    if app_name:
        manifest["name"] = app_name
        manifest["short_name"] = app_name

    if app_short_name:
        manifest["short_name"] = app_short_name

    if app_description:
        manifest["description"] = app_description

    if background_color:
        manifest["background_color"] = background_color

    if theme_color:
        manifest["theme_color"] = theme_color

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, indent=2))


def patch_font_manifest_json(manifest_path: str):
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.loads(f.read())

    manifest.append({"family": "Roboto", "fonts": [{"asset": "fonts/roboto.woff2"}]})

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, indent=2))
