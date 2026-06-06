import os
import shutil
import urllib.request
from pathlib import Path


def get_cache_root() -> Path:
    """Resolve the Flet on-disk cache root.

    Uses `$FLET_CACHE_DIR` if set, otherwise `~/.flet/cache`. The resolved
    path is exported back into the process environment so child processes
    (notably the Gradle build of `serious_python_android`) share the same
    cache root by default.
    """
    root = os.environ.get("FLET_CACHE_DIR")
    cache_root = Path(root).expanduser() if root else Path.home() / ".flet" / "cache"
    os.environ["FLET_CACHE_DIR"] = str(cache_root)
    return cache_root


def get_cached_template_zip(url: str, version: str) -> Path:
    """Return a local path to `flet-build-template.zip` for `version`.

    The build template at a versioned release URL is immutable, so caching
    is a simple "use if present, else download once" — no revalidation.
    """
    cache_path = (
        get_cache_root() / "build-template" / f"v{version}" / "flet-build-template.zip"
    )

    if cache_path.exists() and cache_path.stat().st_size > 0:
        return cache_path

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")

    try:
        with urllib.request.urlopen(url) as resp, open(tmp_path, "wb") as out:
            shutil.copyfileobj(resp, out)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp_path, cache_path)
    except BaseException:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise

    return cache_path
