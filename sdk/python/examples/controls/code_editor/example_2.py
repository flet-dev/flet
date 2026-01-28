import flet_code_editor as fce

import flet as ft

DART_SAMPLE = """import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(child: Text('Hello CodeEditor')),
      ),
    );
  }
}
"""


def main(page: ft.Page):
    theme = fce.CodeTheme(
        styles={
            "keyword": ft.TextStyle(
                color=ft.Colors.INDIGO_600, weight=ft.FontWeight.W_600
            ),
            "string": ft.TextStyle(color=ft.Colors.RED_700),
            "comment": ft.TextStyle(color=ft.Colors.GREY_600, italic=True),
        }
    )

    text_style = ft.TextStyle(
        font_family="monospace",
        height=1.2,
    )

    gutter_style = fce.GutterStyle(
        text_style=ft.TextStyle(
            font_family="monospace",
            height=1.2,
        ),
        show_line_numbers=True,
        show_folding_handles=True,
        # background_color=ft.Colors.GREY_200,
        # padding=ft.Padding.symmetric(horizontal=8),
        width=180,
    )

    page.add(
        ft.Text("Dart Code Editor Example", size=20),
        fce.CodeEditor(
            language="dart",
            code_theme=theme,
            autocompletion_enabled=True,
            autocompletion_words=[
                "MaterialApp",
                "Scaffold",
                "StatelessWidget",
                "Widget",
            ],
            text=DART_SAMPLE,
            text_style=text_style,
            gutter_style=gutter_style,
            expand=True,
        ),
    )


ft.run(main)
