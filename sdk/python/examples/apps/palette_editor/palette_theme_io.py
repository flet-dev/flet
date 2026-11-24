import ast

from palette_constants import COLOR_ROLE_EXPORT_ORDER, THEME_COLOR_ROLE_NAMES

import flet as ft


def normalize_import_theme_code(code: str) -> str:
    normalized = code.strip()
    if normalized.startswith("```"):
        lines = normalized.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        normalized = "\n".join(lines).strip()
    return normalized


def parse_theme_code_ast(code: str) -> ast.Module:
    normalized = normalize_import_theme_code(code)
    last_error: SyntaxError | None = None
    for _ in range(4):
        try:
            return ast.parse(normalized)
        except SyntaxError as exc:
            last_error = exc
            if not normalized.endswith(")"):
                break
            normalized = normalized[:-1].rstrip()
    assert last_error is not None
    raise ValueError from last_error


def format_color_value(color_value: ft.ColorValue) -> str:
    if hasattr(color_value, "name"):
        return f"ft.Colors.{color_value.name}"
    return repr(color_value)


def build_export_code(theme_color_overrides: dict[str, ft.ColorValue]) -> str:
    lines = ["ft.Theme("]
    for color_role in COLOR_ROLE_EXPORT_ORDER:
        if color_role not in THEME_COLOR_ROLE_NAMES:
            continue
        color_value = theme_color_overrides.get(color_role)
        if color_value is None:
            continue
        lines.append(f"  {color_role}={format_color_value(color_value)},")

    color_scheme_lines: list[str] = []
    for color_role in COLOR_ROLE_EXPORT_ORDER:
        if color_role in THEME_COLOR_ROLE_NAMES:
            continue
        color_value = theme_color_overrides.get(color_role)
        if color_value is None:
            continue
        color_scheme_lines.append(
            f"      {color_role}={format_color_value(color_value)},"
        )

    if color_scheme_lines:
        lines.append("  color_scheme=ft.ColorScheme(")
        lines.extend(color_scheme_lines)
        lines.append("  )")
    lines.append(")")
    return "\n".join(lines)


def get_attribute_path(node: ast.AST) -> list[str] | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return list(reversed(parts))
    return None


def parse_import_color_value(node: ast.AST) -> ft.ColorValue:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    attr_path = get_attribute_path(node)
    if attr_path and len(attr_path) == 3 and attr_path[:2] == ["ft", "Colors"]:
        color_name = attr_path[2]
        if hasattr(ft.Colors, color_name):
            return getattr(ft.Colors, color_name)
    raise ValueError


def parse_import_theme_code(code: str) -> dict[str, ft.ColorValue]:
    tree = parse_theme_code_ast(code)

    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
        raise ValueError

    theme_call = tree.body[0].value
    if not isinstance(theme_call, ast.Call):
        raise ValueError

    theme_path = get_attribute_path(theme_call.func)
    if theme_path != ["ft", "Theme"]:
        raise ValueError

    parsed_overrides: dict[str, ft.ColorValue] = {}
    color_scheme_call: ast.Call | None = None
    for keyword in theme_call.keywords:
        if keyword.arg in THEME_COLOR_ROLE_NAMES:
            parsed_overrides[keyword.arg] = parse_import_color_value(keyword.value)
            continue
        if keyword.arg == "color_scheme" and isinstance(keyword.value, ast.Call):
            color_scheme_call = keyword.value
    if color_scheme_call is None and not parsed_overrides:
        raise ValueError

    if color_scheme_call is not None:
        color_scheme_path = get_attribute_path(color_scheme_call.func)
        if color_scheme_path != ["ft", "ColorScheme"]:
            raise ValueError

        for keyword in color_scheme_call.keywords:
            if keyword.arg not in COLOR_ROLE_EXPORT_ORDER:
                raise ValueError
            parsed_overrides[keyword.arg] = parse_import_color_value(keyword.value)

    return parsed_overrides
