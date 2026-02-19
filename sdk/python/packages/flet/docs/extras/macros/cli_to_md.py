import argparse
import textwrap
from typing import Optional

from flet_cli.cli import get_parser


def render_flet_cli_as_markdown(
    command: str = "",
    subcommands_only: bool = True,
) -> str:
    """Return Markdown for a single argparse command/subcommand (for MkDocs pages).

    Output structure:
    1) Plain description paragraph (dedented, capitalized, period-added)
    2) "Usage" section (always starts with "flet")
    3) "Positional arguments" as titled entries (required-first)
        - Shows **Default:** when present
        - Else shows **Required:** true/false
        - Shows **Possible values:** a, b, c (inline) when choices exist
        - Shows **Value:** only when it adds information (type/nargs) beyond DEST
    4) "Options" as titled entries (Style 1)
        - Title is the canonical flag (prefer long; else short)
        - Shows **Default:** when present
        - Shows **Required:** true only if explicitly required
        - Shows **Possible values:** inline when choices exist
        - Shows **Aliases:** other flags, excluding the title flag
    5) "Subcommands" list (names with first-line description)

    Args:
        command: Space-separated subcommand chain (e.g., "", "create", "doctor").
        subcommands_only: If True and the command has subcommands, list them briefly.

    Returns:
        Markdown string for the selected command/subcommand.
    """

    # ---------------- helpers ----------------
    def _is_suppress(v: object) -> bool:
        """True if argparse 'suppress' sentinel."""
        return v is argparse.SUPPRESS or v == "==SUPPRESS=="

    def _takes_value(a: argparse.Action) -> bool:
        """True if this action consumes a value (not boolean/count/help/version)."""
        return not isinstance(
            a,
            (
                argparse._StoreTrueAction,
                argparse._StoreFalseAction,
                argparse._CountAction,
                argparse._HelpAction,
                argparse._VersionAction,
            ),
        )

    def _all_flags(a: argparse.Action) -> list[str]:
        """All switches for an option, short first then long."""
        shorts = [
            s for s in a.option_strings if s.startswith("-") and not s.startswith("--")
        ]
        longs = [s for s in a.option_strings if s.startswith("--")]
        return shorts + longs if (shorts or longs) else list(a.option_strings)

    def _canonical_heading_flag(a: argparse.Action) -> str:
        """
        Canonical flag for the option heading (prefer long; else short; else dest).
        """
        longs = [s for s in a.option_strings if s.startswith("--")]
        if longs:
            return longs[0]
        shorts = [
            s for s in a.option_strings if s.startswith("-") and not s.startswith("--")
        ]
        if shorts:
            return shorts[0]
        return a.option_strings[0] if a.option_strings else a.dest

    def _clean(s: Optional[str]) -> Optional[str]:
        """Dedent and trim leading/trailing whitespace."""
        return textwrap.dedent(s).strip() if s else s

    def _cap_first(s: Optional[str]) -> Optional[str]:
        """Capitalize first letter and ensure trailing period; do not change grammar."""
        if not s:
            return s
        t = s.strip()
        if not t:
            return t
        t = t[0].upper() + t[1:]
        if t[-1] not in ".!?":
            t += "."
        return t

    def _head(level: int, text: str) -> str:
        """Markdown heading helper."""
        return f"{'#' * level} {text}"

    def _ensure_blank(lines: list[str]) -> None:
        """Append a blank line if the last line is not blank."""
        if lines and lines[-1] != "":
            lines.append("")

    def _format_default(a: argparse.Action) -> Optional[str]:
        """Formatted default if meaningful, else None."""
        if _is_suppress(a.default):
            return None
        if isinstance(a, (argparse._StoreTrueAction, argparse._StoreFalseAction)):
            return f"`{bool(a.default)}`" if bool(a.default) else None
        if isinstance(a, argparse._CountAction):
            return f"`{a.default}`" if a.default not in (None, 0) else None
        if getattr(a, "const", None) is not None and a.default == a.const:
            return None
        if a.default not in (None, "", []):
            return f"`{a.default}`"
        return None

    def _metavar_if_informative(
        a: argparse.Action, *, positional: bool
    ) -> Optional[str]:
        """Return informative metavar or None when redundant.

        - Suppress for flags without values or when choices exist.
        - Suppress when token is just DEST in upper-case and there is no extra info.
        - Include type/nargs adornments when present.
        """
        if not positional and not _takes_value(a):
            return None
        if a.choices:
            return None

        base = a.metavar or (a.dest.upper().replace("-", "_"))
        dest_upper = (a.dest or "").upper().replace("-", "_")

        # nargs adornment
        nargs_suffix = ""
        if a.nargs in ("*", "+"):
            nargs_suffix = a.nargs
        elif isinstance(a.nargs, int) and a.nargs > 1:
            nargs_suffix = f"×{a.nargs}"

        # type adornment
        t = getattr(a, "type", None)
        tname = getattr(t, "__name__", "") if callable(t) else ""
        has_type = bool(tname and tname != "str")

        informative = (nargs_suffix != "") or has_type
        if not informative and base == dest_upper:
            return None

        token = base + nargs_suffix
        if has_type:
            token += f" <{tname}>"
        return token

    def _choices_inline(a: argparse.Action) -> Optional[str]:
        """Inline choices like: `a`, `b`, `c` (stable, sorted if needed)."""
        if not a.choices:
            return None
        # choices might be a set -> make stable (sorted by str)
        try:
            items = list(a.choices)
        except TypeError:
            # If choices isn't iterable in a friendly way, fallback to repr
            items = [a.choices]
        # Sort for stability across runs
        items = sorted(items, key=str)
        return ", ".join(f"`{c}`" for c in items)

    # ---------------- resolve command ----------------
    root = get_parser()
    raw_prog = getattr(root, "prog", None) or "cli"

    def _resolve(
        p: argparse.ArgumentParser, parts: list[str]
    ) -> argparse.ArgumentParser:
        """Walk subcommands like ['build', 'ios'] and return that subparser."""
        if not parts:
            return p
        cur = p
        used: list[str] = []
        for tok in parts:
            used.append(tok)
            subparsers = next(
                (
                    act
                    for act in cur._actions
                    if isinstance(act, argparse._SubParsersAction)
                ),
                None,
            )
            if not subparsers:
                raise ValueError(
                    f"No subcommands under: {' '.join(used[:-1]) or '(root)'}"
                )
            if tok not in subparsers.choices:
                opts = ", ".join(sorted(subparsers.choices.keys()))
                raise ValueError(f"Unknown subcommand '{tok}'. Available: {opts}")
            cur = subparsers.choices[tok]
        return cur

    parts = [p for p in command.split() if p]
    parser = _resolve(root, parts)

    # ---------------- build markdown ----------------
    out: list[str] = []
    heading_level = 2
    section_level = heading_level  # e.g., 2 -> "##"
    entry_level = heading_level + 1  # e.g., 3 -> "###"

    # 1) Description
    desc = _cap_first(_clean(parser.description))
    if desc:
        out.append(desc)
        out.append("")

    # 2) Usage
    usage = parser.format_usage().strip()
    if usage.lower().startswith("usage:"):
        usage = usage[6:].strip()
    usage = usage.replace(raw_prog, "flet", 1)
    out.append(_head(section_level, "Usage"))
    out.append("")
    out.append("```bash")
    out.append(usage)
    out.append("```")

    # 3) Collect actions
    positionals_indexed: list[tuple[int, argparse.Action]] = []
    options: list[argparse.Action] = []
    subparsers = None
    for idx, act in enumerate(parser._actions):
        if isinstance(act, argparse._SubParsersAction):
            subparsers = act
        elif act.option_strings:
            options.append(act)
        else:
            positionals_indexed.append((idx, act))

    # 4) Positional arguments
    if positionals_indexed:
        # required first, stable in original order within groups
        positionals_indexed.sort(key=lambda ia: (0 if ia[1].required else 1, ia[0]))

        out.append("")
        out.append(_head(section_level, "Positional arguments"))
        out.append("")
        for _, a in positionals_indexed:
            title = f"`{a.metavar or a.dest}`"
            out.append(_head(entry_level, title))

            body_lines: list[str] = []
            help_text = _cap_first(_clean(a.help)) or ""
            if help_text:
                body_lines.append(help_text)

            # Choices (inline) OR informative value
            if a.choices:
                _ensure_blank(body_lines)
                body_lines.append(f"**Possible values:** {_choices_inline(a)}")
            else:
                meta = _metavar_if_informative(a, positional=True)
                if meta:
                    _ensure_blank(body_lines)
                    body_lines.append(f"**Value:** `{meta}`")

            default = _format_default(a)
            if default:
                _ensure_blank(body_lines)
                body_lines.append(f"**Default:** {default}")
            else:
                # No default -> explicit required true/false
                _ensure_blank(body_lines)
                body_lines.append(f"**Required:** {'true' if a.required else 'false'}")

            if body_lines:
                out.extend(body_lines)
            out.append("")

    # 5) Options
    if options:
        out.append("")
        out.append(_head(section_level, "Options"))
        out.append("")

        # stable sort by long flag
        def _sort(a: argparse.Action) -> str:
            longs = sorted([s for s in a.option_strings if s.startswith("--")]) or [
                "~" + (sorted(a.option_strings)[0] if a.option_strings else "")
            ]
            return longs[0]

        options = sorted(options, key=_sort)

        for a in options:
            title_flag = _canonical_heading_flag(a)
            out.append(_head(entry_level, f"`{title_flag}`"))

            body_lines: list[str] = []
            help_text = _cap_first(_clean(a.help)) or ""
            if help_text:
                body_lines.append(help_text)

            # Choices (inline) OR informative value
            if a.choices:
                _ensure_blank(body_lines)
                body_lines.append(f"**Possible values:** {_choices_inline(a)}")
            else:
                meta = _metavar_if_informative(a, positional=False)
                if meta:
                    _ensure_blank(body_lines)
                    body_lines.append(f"**Value:** `{meta}`")

            default = _format_default(a)
            if default:
                _ensure_blank(body_lines)
                body_lines.append(f"**Default:** {default}")

            # Only show 'Required: true' for required options
            if getattr(a, "required", False):
                _ensure_blank(body_lines)
                body_lines.append("**Required:** true")

            # Aliases (excluding the title flag)
            aliases = [f for f in _all_flags(a) if f != title_flag]
            if aliases:
                _ensure_blank(body_lines)
                body_lines.append(
                    "**Aliases:** " + ", ".join(f"`{f}`" for f in aliases)
                )

            if body_lines:
                out.extend(body_lines)
            out.append("")

    # 6) Subcommands (list only)
    if subcommands_only and subparsers and subparsers.choices:
        out.append("")
        out.append(_head(section_level, "Subcommands"))
        out.append("")
        for name, sub in sorted(subparsers.choices.items()):
            d = _clean(sub.description) or ""
            first = _cap_first(d.splitlines()[0]) if d else ""
            out.append(f"- [`{name}`](flet-{name}.md): {first}")

    return "\n".join(out)


if __name__ == "__main__":
    print(render_flet_cli_as_markdown("create"))
    print(render_flet_cli_as_markdown("", subcommands_only=True))
