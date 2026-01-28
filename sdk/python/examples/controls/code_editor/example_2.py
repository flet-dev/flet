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
            "root": ft.TextStyle(
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.GREY_100,
                font_family="monospace",
                size=24,
                height=1.9,
            ),
            "keyword": ft.TextStyle(
                color=ft.Colors.INDIGO_600, weight=ft.FontWeight.W_600
            ),
            "string": ft.TextStyle(color=ft.Colors.RED_700),
            "comment": ft.TextStyle(color=ft.Colors.GREY_600, italic=True),
        }
    )

    line_number_style = fce.GutterStyle(
        text_style=ft.TextStyle(
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.GREY_100,
            font_family="monospace",
            size=24,
            # height=2.9,
        ),
        show_line_numbers=True,
        show_folding_handles=True,
        # background_color=ft.Colors.GREY_200,
        # padding=ft.Padding.symmetric(horizontal=8),
        width=180,
    )

    page.scroll = ft.ScrollMode.AUTO
    page.add(
        fce.CodeEditor(
            language="dart",
            theme=theme,
            line_number_style=line_number_style,
            autocompletion_enabled=True,
            autocompletion_words=[
                "MaterialApp",
                "Scaffold",
                "StatelessWidget",
                "Widget",
            ],
            text=DART_SAMPLE,
            # expand=True,
        )
    )


ft.run(main)
