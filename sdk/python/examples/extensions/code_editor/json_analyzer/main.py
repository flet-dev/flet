import asyncio
import json

import flet_code_editor as fce

import flet as ft

INVALID_JSON = """{
  "name": "flet"
  "version": 1
}"""


async def main(page: ft.Page):
    page.title = "CodeEditor JSON analyzer"

    debounce_task = None

    def analyze_json(code):
        issues = []
        try:
            json.loads(code)
        except json.JSONDecodeError as ex:
            issues.append(
                fce.Issue(
                    line=ex.lineno - 1,
                    message=ex.msg,
                    type=fce.IssueType.ERROR,
                )
            )
        editor.issues = issues
        editor.update()

    async def debounced_analyze(code):
        await asyncio.sleep(0.5)
        analyze_json(code)

    def on_code_change(e):
        nonlocal debounce_task
        if debounce_task:
            debounce_task.cancel()
        debounce_task = asyncio.ensure_future(debounced_analyze(e.data))

    editor = fce.CodeEditor(
        language=fce.CodeLanguage.JSON,
        code_theme=fce.CodeTheme.ATOM_ONE_LIGHT,
        value=INVALID_JSON,
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
    analyze_json(INVALID_JSON)


if __name__ == "__main__":
    ft.run(main)
