import json
import re
from pathlib import Path
from typing import Optional

from flet.controls.types import RouteUrlStrategy, WebRenderer


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
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: bool = False,
):
    with open(index_path, encoding="utf-8") as f:
        index = f.read()

    app_config = []

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        app_config.append("flet.pyodide = true;")
        app_config.append(f"flet.micropipIncludePre = {str(pyodide_pre).lower()};")
        app_config.append(f'flet.pythonModuleName = "{module_name}";')

    app_config.append(f"flet.noCdn={str(no_cdn).lower()};")
    app_config.append(f'flet.webRenderer="{web_renderer.value}";')
    app_config.append(f'flet.routeUrlStrategy="{route_url_strategy.value}";')

    if websocket_endpoint_path:
        app_config.append(f'flet.webSocketEndpoint="{websocket_endpoint_path}";')

    index = index.replace(
        "<!-- fletAppConfig -->",
        "<script>\n{}\n</script>".format("\n".join(app_config)),
    )

    if base_href:
        base_url = base_href.strip("/").strip()
        index = index.replace(
            '<base href="/">',
            '<base href="{}">'.format("/" if base_url == "" else f"/{base_url}/"),
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
