"""In-memory icon search across Material and Cupertino icon sets.

Icon names come from the bundled api.json enums; Material synonym tags
and popularity come from the committed `data/icons.json` (Google's own
fonts.google.com search metadata, refreshed via
`python -m flet_mcp.build.icons`). No runtime dependency on the flet
package — flet-mcp consumers install only the MCP runtime.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable


class IconStore:
    def __init__(
        self,
        material: Iterable[str],
        cupertino: Iterable[str],
        material_meta: dict[str, dict] | None = None,
    ):
        """`material` / `cupertino` are icon member names (ADD, TRASH, …).
        `material_meta` maps NAME -> {"tags": [...], "popularity": int}
        (the icons.json payload); missing/empty degrades gracefully to
        name-token search."""
        self._material: list[str] = list(material)
        self._cupertino: list[str] = list(cupertino)
        self._meta: dict[str, dict] = material_meta or {}

        # Inverted index: keyword -> set of (family, icon_name). Name
        # tokens and synonym tags land in the same index and score the
        # same — popularity does the ranking (Google's tags are their
        # search index; a tag hit on ADD must beat a name hit on the
        # obscure ONE_K_PLUS).
        self._index: dict[str, set[tuple[str, str]]] = defaultdict(set)

        self._build_index()

    def _build_index(self):
        for icon_name in self._material:
            self._index_icon("material", icon_name)
        for icon_name in self._cupertino:
            self._index_icon("cupertino", icon_name)

    def _popularity(self, family: str, icon_name: str) -> int:
        if family != "material":
            return 0
        meta = self._meta.get(icon_name) or self._meta.get(_base_name(icon_name))
        return int(meta.get("popularity", 0)) if meta else 0

    def _index_icon(self, family: str, icon_name: str):
        entry = (family, icon_name)
        for token in icon_name.lower().split("_"):
            if token:
                self._index[token].add(entry)

        if family != "material":
            return
        # Tags are recorded for base names; style variants
        # (_OUTLINED/_ROUNDED/_SHARP) inherit their base icon's tags.
        meta = self._meta.get(icon_name) or self._meta.get(_base_name(icon_name))
        for tag in (meta or {}).get("tags", []):
            for word in str(tag).lower().split():
                if word:
                    self._index[word].add(entry)

    def find(
        self,
        query: str,
        family: str | None = None,
        limit: int = 10,
    ) -> list[str]:
        """Search icons by query string.

        Args:
            query: Space-separated search terms.
            family: Optional filter — "material" or "cupertino".
            limit: Maximum number of results to return.

        Returns:
            List of qualified icon names like "Icons.ARROW_BACK"
            or "CupertinoIcons.BACK".
        """
        query_tokens = [t for t in query.lower().split() if t]
        if not query_tokens:
            return []

        # Collect all candidate icons that match at least one token
        candidates: dict[tuple[str, str], float] = defaultdict(float)

        for token in query_tokens:
            for entry in self._index.get(token, set()):
                fam, icon_name = entry
                if family and fam != family:
                    continue
                candidates[entry] += 10

        # Bonus for exact full-name match
        query_as_name = "_".join(query_tokens).upper()
        for entry in list(candidates):
            if entry[1] == query_as_name:
                candidates[entry] += 100

        # Deterministic order: score, then Google's popularity (common
        # icons like ADD outrank obscure ones), then shorter names, then
        # alphabetical — set iteration order must not decide what the
        # model sees.
        sorted_results = sorted(
            candidates.items(),
            key=lambda x: (
                -x[1],
                -self._popularity(*x[0]),
                len(x[0][1]),
                x[0][1],
            ),
        )

        results: list[str] = []
        for (fam, icon_name), _score in sorted_results:
            if len(results) >= limit:
                break
            # Collapse Material style variants (_OUTLINED/_ROUNDED/_SHARP)
            # when their base icon is also a candidate — one icon should
            # not spend several result slots.
            base = _base_name(icon_name)
            if base != icon_name and (fam, base) in candidates:
                continue
            if fam == "material":
                results.append(f"Icons.{icon_name}")
            else:
                results.append(f"CupertinoIcons.{icon_name}")

        return results


def _base_name(icon_name: str) -> str:
    for suffix in ("_OUTLINED", "_ROUNDED", "_SHARP"):
        if icon_name.endswith(suffix):
            return icon_name[: -len(suffix)]
    return icon_name
