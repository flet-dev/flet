import json
import re
from pathlib import Path
from typing import Optional

from flet.core.types import WebRenderer


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
):
    with open(index_path, "r") as f:
        index = f.read()

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        pyodideCode = f"""
        <script>
            var micropipIncludePre = {str(pyodide_pre).lower()};
            var pythonModuleName = "{module_name}";
        </script>
        <script src="python.js"></script>
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

    if base_href:
        base_url = base_href.strip("/").strip()
        index = index.replace(
            '<base href="/">',
            '<base href="{}">'.format(
                "/" if base_url == "" else "/{}/".format(base_url)
            ),
        )
    if websocket_endpoint_path:
        index = re.sub(
            r"\<meta name=\"flet-websocket-endpoint-path\" content=\"(.+)\">",
            r'<meta name="flet-websocket-endpoint-path" content="{}">'.format(
                websocket_endpoint_path
            ),
            index,
        )
    if app_name:
        index = re.sub(
            r"\<meta name=\"apple-mobile-web-app-title\" content=\"(.+)\">",
            r'<meta name="apple-mobile-web-app-title" content="{}">'.format(app_name),
            index,
        )
        index = re.sub(
            r"\<title>(.+)</title>",
            r"<title>{}</title>".format(app_name),
            index,
        )
    if app_description:
        index = re.sub(
            r"\<meta name=\"description\" content=\"(.+)\">",
            r'<meta name="description" content="{}">'.format(app_description),
            index,
        )

    with open(index_path, "w") as f:
        f.write(index)


def patch_manifest_json(
    manifest_path: str,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
    background_color: Optional[str] = None,
    theme_color: Optional[str] = None,
):
    with open(manifest_path, "r") as f:
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

    with open(manifest_path, "w") as f:
        f.write(json.dumps(manifest, indent=2))
