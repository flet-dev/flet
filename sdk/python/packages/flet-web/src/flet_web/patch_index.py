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
    """
    Patch Flutter web `index.html` with Flet runtime and app metadata settings.

    The file is read, updated in memory, and written back to `index_path`.
    This function updates base href, injects Flet app config script, and can
    optionally replace title/description metadata.

    Args:
        index_path: Path to `index.html`.
        base_href: Base URL prefix used by the web app.
        websocket_endpoint_path: Optional websocket endpoint path.
        app_name: Optional app name used for page title and iOS web-app title meta.
        app_description: Optional app description meta content.
        pyodide: Whether to enable Pyodide mode in injected runtime config.
        pyodide_pre: Whether pre-release micropip packages are allowed.
        pyodide_script_path: Path to Python entry script for Pyodide apps.
        web_renderer: Web renderer mode for the frontend runtime.
        route_url_strategy: URL strategy used by frontend routing.
        no_cdn: Whether CDN asset loading should be disabled.
    """

    with open(index_path, encoding="utf-8") as f:
        index = f.read()

    base_url = "/"
    if base_href:
        base_url = base_href.strip("/").strip()
        base_url = "/" if base_url == "" else f"/{base_url}/"

    index = index.replace(
        '<base href="/">',
        f'<base href="{base_url}">',
    )

    app_config = []

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        app_config.append("flet.pyodide = true;")
        app_config.append(f"flet.micropipIncludePre = {str(pyodide_pre).lower()};")
        app_config.append(f'flet.pythonModuleName = "{module_name}";')

    app_config.append(f"flet.noCdn={str(no_cdn).lower()};")
    app_config.append(f'flet.webRenderer="{web_renderer.value}";')
    app_config.append(f'flet.routeUrlStrategy="{route_url_strategy.value}";')
    app_config.append(f'flet.entrypointBaseUrl="{base_url}";')
    app_config.append(f'flet.assetBase="{base_url}";')

    if websocket_endpoint_path:
        app_config.append(f'flet.webSocketEndpoint="{websocket_endpoint_path}";')

    index = index.replace(
        "<!-- fletAppConfig -->",
        "<script>\n{}\n</script>".format("\n".join(app_config)),
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
    """
    Patch selected fields in a web app `manifest.json`.

    The manifest is loaded as JSON, updated with provided values, and written
    back to `manifest_path`.

    Args:
        manifest_path: Path to `manifest.json`.
        app_name: Optional app full name. Also sets `short_name` unless
            `app_short_name` is explicitly provided.
        app_short_name: Optional app short name override.
        app_description: Optional manifest description.
        background_color: Optional app background color.
        theme_color: Optional browser UI theme color.
    """

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
    """
    Append bundled Roboto font entry to Flutter's `FontManifest.json`.

    Args:
        manifest_path: Path to `FontManifest.json`.
    """

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.loads(f.read())

    manifest.append({"family": "Roboto", "fonts": [{"asset": "fonts/roboto.woff2"}]})

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(manifest, indent=2))
