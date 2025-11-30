import json
import re
from pathlib import Path
from typing import Optional

from flet.controls.types import RouteUrlStrategy, WebRenderer


def _replace_flet_value(index: str, key: str, value: str) -> str:
    """
    Replace a single property inside the `var flet = { ... }` block.
    """
    pattern = rf"({re.escape(key)}\s*:\s*)([^,}}]+)"
    replacement = rf"\1{value}"
    return re.sub(pattern, replacement, index, flags=re.MULTILINE)


def _normalize_base(base_href: str) -> str:
    base_url = base_href.strip("/").strip() if base_href else ""
    return "/" if base_url == "" else f"/{base_url}/"


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

    base = _normalize_base(base_href)
    if base_href:
        index = index.replace('<base href="/">', f'<base href="{base}">')

    app_config = []

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        app_config.append("flet.pyodide = true;")
        app_config.append(f"flet.micropipIncludePre = {str(pyodide_pre).lower()};")
        app_config.append(f"flet.pythonModuleName = {module_name!r};")

    app_config.append(f"flet.noCdn = {str(no_cdn).lower()};")
    app_config.append(f"flet.webRenderer = {web_renderer.value!r};")
    app_config.append(f"flet.routeUrlStrategy = {route_url_strategy.value!r};")

    if websocket_endpoint_path:
        app_config.append(f"flet.webSocketEndpoint={websocket_endpoint_path!r};")

    index = index.replace(
        "<!-- fletAppConfig -->",
        "<script>\n{}\n</script>".format("\n".join(app_config)),
    )

    # Update flet bootstrap object to respect base-url and routing options.
    index = _replace_flet_value(index, "pyodide", str(pyodide).lower())
    index = _replace_flet_value(index, "noCdn", str(no_cdn).lower())
    index = _replace_flet_value(index, "webRenderer", f"{web_renderer.value!r}")
    index = _replace_flet_value(
        index, "routeUrlStrategy", f"{route_url_strategy.value!r}"
    )
    index = _replace_flet_value(index, "entrypointBaseUrl", f"{base!r}")
    index = _replace_flet_value(index, "assetBase", f"{base!r}")
    index = _replace_flet_value(index, "canvasKitBaseUrl", f"'{base}canvaskit/'")
    index = _replace_flet_value(index, "pyodideUrl", f"'{base}pyodide/pyodide.js'")
    if websocket_endpoint_path:
        index = _replace_flet_value(
            index, "webSocketEndpoint", f"{websocket_endpoint_path!r}"
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
