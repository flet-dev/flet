# Introduction

{{cookiecutter.control_name}} for Flet.

## Examples

```
import flet as ft

from {{cookiecutter.project_name_underscore}} import {{cookiecutter.control_name}}


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.Alignment.CENTER, bgcolor=ft.Colors.PURPLE_200, content={{cookiecutter.control_name}}(
                    tooltip="My new {{cookiecutter.control_name}} Control tooltip",
                    value = "My new {{cookiecutter.control_name}} Flet Control",
                ),),

    )


ft.run(main)
```

## Classes

[{{cookiecutter.control_name}}]({{cookiecutter.control_name}}.md)
