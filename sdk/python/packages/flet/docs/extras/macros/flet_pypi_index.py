from __future__ import annotations

import concurrent.futures
import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable
from functools import lru_cache
from html.parser import HTMLParser

try:
    from packaging.utils import parse_sdist_filename, parse_wheel_filename
    from packaging.version import InvalidVersion, Version
except Exception:  # pragma: no cover
    parse_sdist_filename = None  # type: ignore[assignment]
    parse_wheel_filename = None  # type: ignore[assignment]
    InvalidVersion = Exception  # type: ignore[assignment]
    Version = None  # type: ignore[assignment]


DEFAULT_PYPI_FLET_DEV_BASE_URL = "https://pypi.flet.dev/"
DEFAULT_USER_AGENT = "flet-docs-pypi-index-macro/0.1 (+https://flet.dev)"

ProjectIndexEntry = tuple[tuple[str, ...], tuple[str, ...]]  # (versions, platforms)
ProjectIndex = dict[str, ProjectIndexEntry]
IndexFetchResult = tuple[str, ProjectIndex, tuple[tuple[str, str], ...]]


class _AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._current: dict[str, object] | None = None
        self.anchors: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        self._current = {
            "href": attributes.get("href") or "",
            "text": "",
            "attrs": attributes,
        }

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        self._current["text"] = f"{self._current['text']}{data}"

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current is None:
            return
        self.anchors.append(self._current)
        self._current = None


def _normalize_base_url(base_url: str) -> str:
    base_url = base_url.strip()
    if not base_url:
        raise ValueError("base_url must not be empty")
    if not base_url.startswith(("http://", "https://")):
        raise ValueError("base_url must be an http(s) URL")
    if not base_url.endswith("/"):
        base_url += "/"
    parts = urllib.parse.urlsplit(base_url)
    path = parts.path or "/"
    if not path.endswith("/"):
        path += "/"
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def _candidate_simple_root_urls(base_url: str) -> list[str]:
    base_url = _normalize_base_url(base_url)
    parts = urllib.parse.urlsplit(base_url)
    path = parts.path or "/"
    normalized_path = path.rstrip("/")

    candidates = [base_url]
    if normalized_path == "/simple":
        candidates.append(
            urllib.parse.urlunsplit((parts.scheme, parts.netloc, "/", "", ""))
        )
    elif normalized_path in ("", "/"):
        candidates.append(
            urllib.parse.urlunsplit((parts.scheme, parts.netloc, "/simple/", "", ""))
        )

    out: list[str] = []
    seen: set[str] = set()
    for url in candidates:
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def _fetch_text(url: str, *, timeout_s: float, user_agent: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def _parse_anchor_text_and_href(html: str) -> list[tuple[str, str]]:
    parser = _AnchorCollector()
    parser.feed(html)
    out: list[tuple[str, str]] = []
    for a in parser.anchors:
        text = str(a.get("text") or "").strip()
        href = str(a.get("href") or "").strip()
        if not text and not href:
            continue
        out.append((text, href))
    return out


def _list_projects(simple_index_html: str) -> list[str]:
    projects: set[str] = set()
    for text, href in _parse_anchor_text_and_href(simple_index_html):
        candidate = (text or href).strip().strip("/").strip()
        if candidate:
            projects.add(candidate)
    return sorted(projects)


def _filename_from_href_or_text(text: str, href: str) -> str:
    if text:
        return text
    parsed = urllib.parse.urlsplit(href)
    return urllib.parse.unquote(parsed.path.rsplit("/", 1)[-1])


def _version_from_filename(filename: str) -> str | None:
    filename = filename.strip()
    if not filename:
        return None

    if filename.endswith(".whl") and parse_wheel_filename is not None:
        try:
            _, version, _, _ = parse_wheel_filename(filename)
        except Exception:
            return None
        return str(version)

    if parse_sdist_filename is not None:
        try:
            _, version = parse_sdist_filename(filename)
        except Exception:
            return None
        return str(version)

    return None


def _platforms_from_wheel_tags(tags) -> set[str]:
    platforms: set[str] = set()
    for tag in tags:
        platform_tag = getattr(tag, "platform", "")
        if not platform_tag:
            continue
        if platform_tag == "any":
            platforms.update({"android", "ios"})
            continue
        platform_lower = platform_tag.lower()
        if "android" in platform_lower:
            platforms.add("android")
        if "ios" in platform_lower or "iphone" in platform_lower:
            platforms.add("ios")
    return platforms


def _platform_suffix(project_platforms: set[str]) -> str:
    if project_platforms == {"android"}:
        return " (Android only)"
    if project_platforms == {"ios"}:
        return " (iOS only)"
    return ""


def _sorted_versions(versions: Iterable[str]) -> list[str]:
    versions_set = {v.strip() for v in versions if v.strip()}
    if not versions_set:
        return []

    if Version is None:
        return sorted(versions_set)

    valid: list[tuple[Version, str]] = []
    invalid: list[str] = []
    for v in versions_set:
        try:
            valid.append((Version(v), v))
        except InvalidVersion:
            invalid.append(v)

    valid.sort(key=lambda t: t[0], reverse=True)
    invalid.sort()
    return [v for _, v in valid] + invalid


def _format_md(
    packages: dict[str, list[str]],
    platforms: dict[str, set[str]],
    resolved_base_url: str,
) -> str:
    lines = ["| Package | Versions |", "|---|---|"]
    for name, versions in packages.items():
        project_url = urllib.parse.urljoin(
            resolved_base_url, f"{urllib.parse.quote(name)}/"
        )
        project_platforms = platforms.get(name) or set()
        platform_suffix = _platform_suffix(project_platforms)
        versions_cell = ", ".join(versions) if versions else ""
        package_cell = f"[`{name}`]({project_url}){platform_suffix}"
        lines.append(f"| {package_cell} | {versions_cell} |")
    return "\n".join(lines) + "\n"


@lru_cache(maxsize=8)
def _fetch_packages_and_versions_cached(
    base_url: str,
    timeout_s: float,
    workers: int,
    limit_projects: int | None,
    user_agent: str,
) -> IndexFetchResult:
    last_error: Exception | None = None
    resolved_base_url: str | None = None
    projects: list[str] = []

    for candidate in _candidate_simple_root_urls(base_url):
        try:
            candidate_html = _fetch_text(
                candidate, timeout_s=timeout_s, user_agent=user_agent
            )
        except Exception as e:
            last_error = e
            continue

        candidate_projects = _list_projects(candidate_html)
        if not candidate_projects:
            last_error = ValueError(f"No projects found at {candidate}")
            continue

        resolved_base_url = candidate
        projects = candidate_projects
        break

    if resolved_base_url is None:
        if last_error is not None:
            raise last_error
        raise ValueError("Failed to resolve a simple index base URL")

    if limit_projects is not None:
        projects = projects[: max(0, limit_projects)]

    results: ProjectIndex = {}
    errors: list[tuple[str, str]] = []

    def fetch_one(project: str) -> tuple[str, tuple[str, ...], tuple[str, ...]]:
        project_url = urllib.parse.urljoin(resolved_base_url, f"{project}/")
        html = _fetch_text(project_url, timeout_s=timeout_s, user_agent=user_agent)
        versions: set[str] = set()
        project_platforms: set[str] = set()
        for text, href in _parse_anchor_text_and_href(html):
            filename = _filename_from_href_or_text(text, href)
            if filename.endswith(".whl") and parse_wheel_filename is not None:
                try:
                    _, version, _, tags = parse_wheel_filename(filename)
                except Exception:
                    continue
                versions.add(str(version))
                project_platforms.update(_platforms_from_wheel_tags(tags))
                continue
            version = _version_from_filename(filename)
            if version is not None:
                versions.add(version)
        return (
            project,
            tuple(_sorted_versions(versions)),
            tuple(sorted(project_platforms)),
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        future_to_project = {executor.submit(fetch_one, p): p for p in projects}
        for future in concurrent.futures.as_completed(future_to_project):
            project = future_to_project[future]
            try:
                project, versions, project_platforms = future.result()
            except Exception as e:
                errors.append((project, f"{type(e).__name__}: {e}"))
                continue
            results[project] = (versions, project_platforms)

    return resolved_base_url, dict(sorted(results.items())), tuple(errors)


def render_pypi_flet_dev_packages_versions(
    base_url: str = DEFAULT_PYPI_FLET_DEV_BASE_URL,
    *,
    timeout_s: float = 20.0,
    workers: int = 12,
    limit_projects: int | None = None,
    max_versions: int | None = None,
    user_agent: str = DEFAULT_USER_AGENT,
    output_format: str = "md",
    strict: bool = False,
) -> str:
    """Render a packages+versions listing from a PEP-503 'simple' index.

    Args:
        base_url: Index base URL. This can be either `/` or `/simple/`.
        timeout_s: Per-request timeout.
        workers: Parallel fetches for per-project pages.
        limit_projects: Optional cap on number of projects (useful for local testing).
        max_versions: Optional cap on number of versions per project (latest first).
        user_agent: HTTP User-Agent header.
        output_format: One of: "md", "json", "text".
        strict: If True, raise on fetch failures;
            else render partial results + a warning block.
    """
    try:
        resolved_base_url, packages_raw, errors = _fetch_packages_and_versions_cached(
            base_url=base_url,
            timeout_s=timeout_s,
            workers=workers,
            limit_projects=limit_projects,
            user_agent=user_agent,
        )
    except Exception as e:
        if strict:
            raise
        message = f"{type(e).__name__}: {e}"
        if output_format == "json":
            rendered = json.dumps(
                {
                    "packages": {},
                    "platforms": {},
                    "errors": [{"project": "__index__", "error": message}],
                },
                indent=2,
                sort_keys=True,
            )
            return rendered + "\n"
        if output_format == "text":
            return f"ERROR: {message}\n"
        return "\n".join(
            [
                "!!! warning",
                f"    Failed to fetch package index from `{base_url}`.",
                f"    {message}",
                "",
            ]
        )

    packages: dict[str, list[str]] = {}
    platforms: dict[str, set[str]] = {}
    for name, (versions, project_platforms) in packages_raw.items():
        packages[name] = list(versions)
        platforms[name] = set(project_platforms)
    if max_versions is not None:
        cap = max(0, max_versions)
        packages = {name: versions[:cap] for name, versions in packages.items()}

    if output_format == "json":
        rendered = json.dumps(
            {
                "packages": packages,
                "platforms": {name: sorted(vals) for name, vals in platforms.items()},
                "errors": [{"project": name, "error": err} for name, err in errors],
            },
            indent=2,
            sort_keys=True,
        )
        return rendered + "\n"

    if output_format == "text":
        rendered = "\n".join(
            f"{name}{_platform_suffix(platforms.get(name) or set())}: {', '.join(versions) if versions else '(no versions)'}"
            for name, versions in packages.items()
        )
        rendered += "\n"
        if errors:
            rendered += f"\nWarnings: {len(errors)} project(s) failed:\n"
            rendered += (
                "\n".join(f"- {name}: {err}" for name, err in errors[:10]) + "\n"
            )
            if len(errors) > 10:
                rendered += f"... and {len(errors) - 10} more\n"
        return rendered

    rendered = _format_md(packages, platforms, resolved_base_url)
    if errors:
        message = (
            f"Failed to fetch {len(errors)} project page(s) from `{resolved_base_url}`"
        )
        if strict:
            raise RuntimeError(message)
        details = "\n".join(f"    - `{name}`: {err}" for name, err in errors[:10])
        if len(errors) > 10:
            details += f"\n    - ... and {len(errors) - 10} more"
        rendered += "\n".join(
            [
                "",
                "!!! warning",
                f"    {message}.",
                "    ",
                details,
                "",
            ]
        )

    return rendered


if __name__ == "__main__":
    try:
        print(
            render_pypi_flet_dev_packages_versions(
                DEFAULT_PYPI_FLET_DEV_BASE_URL,
                limit_projects=10,
                max_versions=5,
            )
        )
    except (urllib.error.URLError, ValueError) as e:
        raise SystemExit(f"ERROR: {e}") from e
