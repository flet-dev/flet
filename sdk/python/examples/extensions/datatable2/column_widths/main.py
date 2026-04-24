import flet as ft
import flet_datatable2 as fdt


def main(page: ft.Page):
    def cell_text(value: str) -> ft.Text:
        """A helper to truncate any overflowing cell text with an ellipsis."""
        return ft.Text(value, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1)

    page.add(
        ft.SafeArea(
            expand=True,
            content=fdt.DataTable2(
                expand=True,
                min_width=600,
                columns=[
                    # Absolute pixel width — best for predictable, short fields.
                    fdt.DataColumn2(label="Name", fixed_width=140),
                    # Relative size S — compact, auto-fits the remaining space.
                    fdt.DataColumn2(label="Role", size=fdt.DataColumnSize.S),
                    # Relative size L — takes the lion's share of what's left.
                    fdt.DataColumn2(label="Recent work", size=fdt.DataColumnSize.L),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(cell_text("Alice Nakamura")),
                            ft.DataCell(cell_text("Engineer")),
                            ft.DataCell(
                                cell_text(
                                    "Led the migration of our checkout service "
                                    "to a set of composable workers, cutting "
                                    "p99 latency in half."
                                )
                            ),
                        ]
                    ),
                    ft.DataRow(
                        cells=[
                            # Longer than 140px — shows ellipsis in a fixed column.
                            ft.DataCell(cell_text("Bartholomew Laurent-Fitzgerald")),
                            ft.DataCell(cell_text("Designer")),
                            ft.DataCell(
                                cell_text(
                                    "Rebuilt the onboarding flow and maintains "
                                    "the internal design-system token registry."
                                )
                            ),
                        ]
                    ),
                    ft.DataRow(
                        cells=[
                            ft.DataCell(cell_text("Chen")),
                            ft.DataCell(cell_text("PM")),
                            ft.DataCell(
                                cell_text("Owns the Platform Reliability roadmap.")
                            ),
                        ]
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
