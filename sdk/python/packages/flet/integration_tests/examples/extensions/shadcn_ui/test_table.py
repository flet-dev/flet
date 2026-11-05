import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.table.main as table
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    right = ft.Alignment.CENTER_RIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Table(
            columns=[
                shad.TableColumn("Invoice"),
                shad.TableColumn("Status"),
                shad.TableColumn("Amount", alignment=right),
            ],
            rows=[
                shad.TableRow(
                    cells=[
                        shad.TableCell(invoice),
                        shad.TableCell(status),
                        shad.TableCell(amount),
                    ]
                )
                for invoice, status, amount in [
                    ("INV001", "Paid", "$250.00"),
                    ("INV002", "Pending", "$150.00"),
                    ("INV003", "Unpaid", "$350.00"),
                ]
            ],
            footer=[
                shad.TableCell("Total"),
                shad.TableCell(""),
                shad.TableCell("$750.00"),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": table.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_table(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "table_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("INV003")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text(
            "INV003: Unpaid, $350.00 by Bank Transfer"
        )
    ).count == 1
    flet_app_function.assert_screenshot(
        "table",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["table_initial", "table"], "table_flow", duration=1000
    )
