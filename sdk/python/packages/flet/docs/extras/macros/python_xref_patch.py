import re
from typing import Optional


def patch_python_xref_check_ref():
    """
    Patch python_xref cross-reference checks to preserve handler extensions.

    `python_xref` calls `collect(..., PythonOptions())` when checking refs.
    That fallback path may bypass configured Griffe extensions and cause
    extension-produced metadata (for example deprecation admonitions) to be
    missing in rendered docs.

    This patch keeps the same behavior, but resolves options via
    `self.get_options({})` so configured extensions are always applied.
    """

    try:
        from mkdocstrings_handlers.python_xref.handler import PythonRelXRefHandler
    except Exception:
        return

    if getattr(PythonRelXRefHandler, "_flet_check_ref_patched", False):
        return

    def _check_ref(
        self,
        ref: str,
        exclude: Optional[list[str | re.Pattern]] = None,
    ) -> bool:
        exclude_patterns = exclude or []
        for ex in exclude_patterns:
            if re.match(ex, ref):
                return True
        try:
            self.collect(ref, self.get_options({}))
            return True
        except Exception:
            return False

    PythonRelXRefHandler._check_ref = _check_ref
    PythonRelXRefHandler._flet_check_ref_patched = True
