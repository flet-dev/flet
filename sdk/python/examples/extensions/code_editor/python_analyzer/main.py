import ast
import asyncio

import flet_code_editor as fce

import flet as ft

INVALID_PYTHON = """import os

def greet(name)
    print(f"Hello, {name}!")

greet("World")
"""


async def main(page: ft.Page):
    page.title = "CodeEditor Python analyzer"

    debounce_task = None

    def analyze_python(code):
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as ex:
            issues.append(
                fce.Issue(
                    line=(ex.lineno or 1) - 1,
                    message=ex.msg,
                    type=fce.IssueType.ERROR,
                )
            )
        editor.issues = issues
        editor.update()

    async def debounced_analyze(code):
        await asyncio.sleep(0.5)
        analyze_python(code)

    def on_code_change(e):
        nonlocal debounce_task
        if debounce_task:
            debounce_task.cancel()
        debounce_task = asyncio.ensure_future(debounced_analyze(e.data))

    editor = fce.CodeEditor(
        language=fce.CodeLanguage.PYTHON,
        code_theme=fce.CodeTheme.ATOM_ONE_LIGHT,
        value=INVALID_PYTHON,
        on_change=on_code_change,
        gutter_style=fce.GutterStyle(
            show_errors=True,
            show_line_numbers=True,
            show_folding_handles=True,
            width=80,
        ),
        expand=True,
    )

    page.add(ft.SafeArea(expand=True, content=editor))

    # Run initial analysis
    analyze_python(INVALID_PYTHON)


if __name__ == "__main__":
    ft.run(main)
