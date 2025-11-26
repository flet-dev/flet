import flet as ft


async def main(page: ft.Page):
    page.title = "SemanticsService - Accessibility features"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    async def get_features() -> str:
        features = await ft.SemanticsService().get_accessibility_features()
        return "\n".join(
            [
                f"Accessible navigation: {features.accessible_navigation}",
                f"Bold text: {features.bold_text}",
                f"Disable animations: {features.disable_animations}",
                f"High contrast: {features.high_contrast}",
                f"Invert colors: {features.invert_colors}",
                f"Reduce motion: {features.reduce_motion}",
                f"On/off switch labels: {features.on_off_switch_labels}",
                f"Supports announcements: {features.supports_announcements}",
            ]
        )

    async def refresh_features(e: ft.Event[ft.Button]):
        info.value = await get_features()

    page.add(
        info := ft.Text(await get_features()),
        ft.Button("Refresh features", on_click=refresh_features),
    )


if __name__ == "__main__":
    ft.run(main)
