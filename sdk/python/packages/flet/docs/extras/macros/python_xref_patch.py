"""
Runtime patches for `mkdocstrings-python-xref` integration in Flet docs.

These patches are intentionally narrow and docs-only:
- keep handler extensions active during reference checks;
- ensure relative crossrefs inside extension-inserted admonitions are rewritten.
"""

import re
from typing import Any, Optional, Union

__all__ = ["patch_python_xref"]


def patch_python_xref() -> None:
    """
    Patch python_xref internals for compatibility with
    `flet.utils.griffe_deprecations.py`.

    Applies two idempotent monkey patches:
    - `_check_ref` uses handler options so Griffe extensions are preserved.
    - `substitute_relative_crossrefs` rewrites parsed admonition contents.
    """

    try:
        import mkdocstrings_handlers.python_xref.crossref as crossref
        import mkdocstrings_handlers.python_xref.handler as handler
        from griffe import Alias, DocstringSectionAdmonition, GriffeError, Object
        from mkdocstrings_handlers.python_xref.handler import PythonRelXRefHandler
    except Exception:
        # Docs dependencies are optional outside docs builds.
        return

    original_substitute = handler.substitute_relative_crossrefs

    def _iter_objects(obj: Any):
        """
        Yield an object tree, resolving aliases when possible.

        This mirrors python_xref traversal so we can post-process every
        object's parsed docstring sections.
        """
        if isinstance(obj, Alias):
            try:
                obj = obj.target
            except GriffeError:
                # Unresolved alias: skip, consistent with python_xref behavior.
                return

        yield obj
        for member in obj.members.values():
            if isinstance(member, (Alias, Object)):  # pragma: no branch
                yield from _iter_objects(member)

    def _rewrite_admonition_refs(
        obj: Any,
        checkref=None,
        incompatible_refs=None,
    ) -> None:
        """
        Rewrite relative crossrefs inside the admonition section text.

        The upstream substitution step rewrites only `doc.value`.
        This helper extends that logic to admonition payload text used by
        our deprecation extension.
        """
        for doc_obj in _iter_objects(obj):
            doc = doc_obj.docstring
            if doc is None:
                continue

            for section in doc.parsed:
                if not isinstance(section, DocstringSectionAdmonition):
                    continue

                value = getattr(section, "value", None)
                if value is None:
                    continue

                text_attr = (
                    "description" if hasattr(value, "description") else "contents"
                )
                text = getattr(value, text_attr, None)
                if not isinstance(text, str) or "[" not in text:
                    continue

                # Reuse python_xref's own parser/rewriter so behavior stays aligned
                # with upstream relative-crossref semantics.
                rewritten = crossref._RE_CROSSREF.sub(  # noqa: SLF001
                    crossref._RelativeCrossrefProcessor(  # noqa: SLF001
                        doc,
                        checkref=checkref,
                        incompatible_refs=incompatible_refs,
                    ),
                    text,
                )
                setattr(value, text_attr, rewritten)

    def _check_ref(
        self,
        ref: str,
        exclude: Optional[list[Union[str, re.Pattern]]] = None,
    ) -> bool:
        """
        Check whether a cross-reference target can be collected.

        Unlike upstream implementation, this uses handler-configured options
        so Griffe extensions remain active during reference checks.
        """
        exclude_patterns = exclude or []
        for ex in exclude_patterns:
            if re.match(ex, ref):
                return True
        try:
            self.collect(ref, self.get_options({}))
            return True
        except Exception:
            return False

    if not getattr(PythonRelXRefHandler, "_flet_check_ref_patched", False):
        PythonRelXRefHandler._check_ref = _check_ref
        PythonRelXRefHandler._flet_check_ref_patched = True

    if getattr(handler, "_flet_substitute_relative_crossrefs_patched", False):
        return

    def substitute_relative_crossrefs(
        obj: Any,
        checkref=None,
        incompatible_refs=None,
    ) -> None:
        """
        Run upstream substitution and then patch admonition section text.

        Keeping this as a wrapper avoids reimplementing python_xref logic and
        minimizes maintenance when upstream behavior changes.
        """
        original_substitute(
            obj,
            checkref=checkref,
            incompatible_refs=incompatible_refs,
        )
        _rewrite_admonition_refs(
            obj,
            checkref=checkref,
            incompatible_refs=incompatible_refs,
        )

    # Keep both modules in sync: handler imports the symbol at module load time.
    crossref.substitute_relative_crossrefs = substitute_relative_crossrefs
    handler.substitute_relative_crossrefs = substitute_relative_crossrefs

    handler._flet_substitute_relative_crossrefs_patched = True
