import ast
import re

import flet as ft

ROWS = range(1, 5)
COLUMNS = ("A", "B", "C", "D")
CELL_REF_RE = re.compile(r"\b([A-D][1-4])\b")


INITIAL_FORMULAS = {
    "A1": "12",
    "B1": "8",
    "C1": "=A1+B1",
    "A2": "3",
    "B2": "=C1/2",
    "D4": "=A1+A2+B1",
}


class FormulaError(Exception):
    pass


def format_value(value: object) -> str:
    if value == "":
        return ""
    if isinstance(value, (int, float)):
        rounded = round(float(value), 2)
        if rounded.is_integer():
            return str(int(rounded))
        return f"{rounded:.2f}".rstrip("0").rstrip(".")
    return str(value)


def evaluate_expression(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return evaluate_expression(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = evaluate_expression(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)
    ):
        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left / right
    raise FormulaError("Only +, -, *, / and parentheses are supported.")


def main(page: ft.Page):
    page.title = "7GUIs - Cells"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    formulas = INITIAL_FORMULAS.copy()
    selected_cell = "A1"

    def evaluate_cell(
        cell_id: str, cache: dict[str, object], stack: set[str]
    ) -> object:
        if cell_id in cache:
            return cache[cell_id]
        if cell_id in stack:
            raise FormulaError("Circular reference detected.")

        raw = formulas.get(cell_id, "").strip()
        if raw == "":
            cache[cell_id] = ""
            return ""

        if not raw.startswith("="):
            try:
                value = float(raw)
            except ValueError:
                value = raw
            cache[cell_id] = value
            return value

        expression = raw[1:].upper()

        def replace_reference(match: re.Match[str]) -> str:
            ref = match.group(1)
            value = evaluate_cell(ref, cache, stack | {cell_id})
            if value == "":
                return "0"
            if isinstance(value, (int, float)):
                return str(value)
            raise FormulaError(f"{ref} is not numeric.")

        replaced = CELL_REF_RE.sub(replace_reference, expression)
        try:
            parsed = ast.parse(replaced, mode="eval")
        except SyntaxError as exc:
            raise FormulaError("Formula syntax is invalid.") from exc

        value = evaluate_expression(parsed)
        cache[cell_id] = value
        return value

    def display_value(cell_id: str) -> str:
        try:
            return format_value(evaluate_cell(cell_id, {}, set()))
        except FormulaError:
            return "#ERR"
        except ZeroDivisionError:
            return "#DIV/0"

    def select_cell(cell_id: str):
        nonlocal selected_cell
        selected_cell = cell_id
        formula_field.value = formulas.get(cell_id, "")
        refresh_ui()

    def apply_formula(e):
        formulas[selected_cell] = formula_field.value.strip()
        refresh_ui()

    def build_data_cell(cell_id: str) -> ft.DataCell:
        is_selected = cell_id == selected_cell
        return ft.DataCell(
            show_edit_icon=True,
            on_tap=lambda e, cell_id=cell_id: select_cell(cell_id),
            content=ft.Container(
                width=90,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_100 if is_selected else ft.Colors.WHITE,
                border=ft.Border.all(
                    2 if is_selected else 1,
                    ft.Colors.BLUE_500 if is_selected else ft.Colors.BLACK_12,
                ),
                content=ft.Text(
                    display_value(cell_id) or " ",
                    weight=ft.FontWeight.W_600 if is_selected else None,
                ),
            ),
        )

    def build_table() -> ft.DataTable:
        columns = [ft.DataColumn(label=ft.Text(""))]
        columns.extend(ft.DataColumn(label=ft.Text(column)) for column in COLUMNS)

        rows: list[ft.DataRow] = []
        for row in ROWS:
            cells = [ft.DataCell(ft.Text(str(row), weight=ft.FontWeight.W_600))]
            for column in COLUMNS:
                cell_id = f"{column}{row}"
                cells.append(build_data_cell(cell_id))
            rows.append(ft.DataRow(cells=cells))

        return ft.DataTable(
            heading_row_color=ft.Colors.BLUE_GREY_50,
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK_12),
            columns=columns,
            rows=rows,
        )

    def refresh_ui():
        selected_label.value = f"Selected cell: {selected_cell}"
        computed_label.value = f"Computed value: {display_value(selected_cell)}"
        formula_field.value = formulas.get(selected_cell, "")
        table_host.content = build_table()
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=760,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.GREEN_50,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    tight=True,
                    spacing=18,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Cells", size=28, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "A small spreadsheet with cell references and live recalculation.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                formula_field := ft.TextField(
                                    label="Formula",
                                    width=320,
                                    value=formulas.get(selected_cell, ""),
                                    on_submit=apply_formula,
                                ),
                                ft.FilledButton(
                                    "Apply",
                                    icon=ft.Icons.CHECK,
                                    on_click=apply_formula,
                                ),
                            ],
                        ),
                        selected_label := ft.Text(weight=ft.FontWeight.W_700),
                        computed_label := ft.Text(color=ft.Colors.BLUE_GREY_700),
                        ft.Text(
                            "Use plain text, numbers, or expressions like =A1+B2/2.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Container(
                            padding=16,
                            border_radius=20,
                            bgcolor=ft.Colors.WHITE,
                            content=(table_host := ft.Container()),
                        ),
                    ],
                ),
            )
        )
    )
    refresh_ui()


if __name__ == "__main__":
    ft.run(main)
