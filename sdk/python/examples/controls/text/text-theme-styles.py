import flet
from flet import ListView, Page, Text


def main(page: Page):
    page.title = "Text theme styles"
    page.scroll = "adaptive"

    page.add(
        Text("Display Large", style="displayLarge"),
        Text("Display Medium", style="displayMedium"),
        Text("Display Small", style="displaySmall"),
        Text("Headline Large", style="headlineLarge"),
        Text("Headline Medium", style="headlineMedium"),
        Text("Headline Small", style="headlineMedium"),
        Text("Title Large", style="titleLarge"),
        Text("Title Medium", style="titleMedium"),
        Text("Title Small", style="titleSmall"),
        Text("Label Large", style="labelLarge"),
        Text("Label Medium", style="labelMedium"),
        Text("Label Small", style="labelSmall"),
        Text("Body Large", style="bodylLarge"),
        Text("Body Medium", style="bodyMedium"),
        Text("Body Small", style="bodySmall"),
    )


flet.app(target=main)
