"""In-memory icon search across Material and Cupertino icon sets."""

from __future__ import annotations

import json
from collections import defaultdict
from importlib import resources

import yaml


class IconStore:
    def __init__(self):
        # Load icon JSON files from the flet package
        material_path = resources.files("flet") / "controls" / "material" / "icons.json"
        cupertino_path = (
            resources.files("flet") / "controls" / "cupertino" / "cupertino_icons.json"
        )

        with resources.as_file(material_path) as p:
            self._material: dict[str, int] = json.loads(p.read_text("utf-8"))

        with resources.as_file(cupertino_path) as p:
            self._cupertino: dict[str, int] = json.loads(p.read_text("utf-8"))

        # Load synonym data from flet_mcp/data/icons.yml
        synonyms_path = resources.files("flet_mcp") / "data" / "icons.yml"
        with resources.as_file(synonyms_path) as p:
            self._synonyms_yaml: dict = yaml.safe_load(p.read_text("utf-8")) or {}

        # Build a flat lookup: lowercase base name -> list of synonym keywords
        self._synonym_map: dict[str, list[str]] = {}
        for _category, icons in self._synonyms_yaml.items():
            if not isinstance(icons, dict):
                continue
            for base_name, keywords in icons.items():
                key = str(base_name).lower().replace(" ", "_")
                if isinstance(keywords, list):
                    self._synonym_map[key] = [str(k).lower() for k in keywords]

        # Inverted index: keyword -> set of (family, icon_name)
        self._index: dict[str, set[tuple[str, str]]] = defaultdict(set)

        # Track which (family, icon_name) pairs have synonym-contributed keywords
        self._synonym_entries: set[tuple[str, str, str]] = set()

        self._build_index()

    def _build_index(self):
        for icon_name in self._material:
            self._index_icon("material", icon_name)
        for icon_name in self._cupertino:
            self._index_icon("cupertino", icon_name)

    def _index_icon(self, family: str, icon_name: str):
        entry = (family, icon_name)
        tokens = icon_name.lower().split("_")
        for token in tokens:
            if token:
                self._index[token].add(entry)

        # Look up synonyms by the lowercase underscored name
        lookup_key = icon_name.lower()
        synonyms = self._synonym_map.get(lookup_key, [])
        for keyword in synonyms:
            self._index[keyword].add(entry)
            self._synonym_entries.add((family, icon_name, keyword))

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

                icon_tokens = set(icon_name.lower().split("_"))

                # Check if this token matched via synonym
                is_synonym = (fam, icon_name, token) in self._synonym_entries
                if is_synonym:
                    candidates[entry] += 5
                else:
                    candidates[entry] += 10

        # Bonus for exact full-name match
        query_as_name = "_".join(query_tokens).upper()
        for entry in list(candidates):
            if entry[1] == query_as_name:
                candidates[entry] += 100

        # Bonus: all query tokens present in icon name tokens
        for entry in list(candidates):
            icon_tokens = set(entry[1].lower().split("_"))
            synonym_keywords = {
                kw
                for f, n, kw in self._synonym_entries
                if f == entry[0] and n == entry[1]
            }
            all_tokens = icon_tokens | synonym_keywords
            if all(qt in all_tokens for qt in query_tokens):
                # Already scored per-token above; the per-token +10/+5 covers this
                pass

        sorted_results = sorted(candidates.items(), key=lambda x: -x[1])

        results: list[str] = []
        for (fam, icon_name), _score in sorted_results:
            if len(results) >= limit:
                break
            if fam == "material":
                results.append(f"Icons.{icon_name}")
            else:
                results.append(f"CupertinoIcons.{icon_name}")

        return results
