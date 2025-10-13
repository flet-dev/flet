import flet as ft


class Settings:
    def __init__(
        self, waste_size=3, deck_passes_allowed=1000, card_back="/images/card_back0.png"
    ):
        self.waste_size = waste_size
        self.deck_passes_allowed = deck_passes_allowed
        self.card_back = card_back


class SettingsDialog(ft.AlertDialog):
    def __init__(self, settings, on_settings_applied):
        super().__init__()
        self.on_settings_applied = on_settings_applied
        self.settings = settings
        self.modal = True
        self.title = ft.Text("Solitaire Settings")
        self.waste_size = ft.RadioGroup(
            value=self.settings.waste_size,
            content=ft.Row(
                controls=[
                    ft.Radio(value=1, label="One card"),
                    ft.Radio(value=3, label="Three cards"),
                ]
            ),
        )
        self.deck_passes_allowed = ft.RadioGroup(
            value=self.settings.deck_passes_allowed,
            content=ft.Row(
                controls=[
                    ft.Radio(value=3, label="Three"),
                    ft.Radio(value=1000, label="Unlimited"),
                ]
            ),
        )
        self.generate_card_backs()

        self.content = ft.Column(
            controls=[
                ft.Text("Waste pile size:"),
                self.waste_size,
                ft.Text("Passes through the deck:"),
                self.deck_passes_allowed,
                ft.Row(controls=self.card_backs),
                ft.Checkbox(
                    label="New game will be started when settings are updated.",
                    value=True,
                    disabled=True,
                ),
            ],
            tight=True,
        )
        self.actions = [
            ft.TextButton("Cancel", on_click=self.cancel),
            ft.FilledButton("Apply settings", on_click=self.apply_settings),
        ]

    def generate_card_backs(self):
        self.card_backs = []
        for i in range(4):
            self.card_backs.append(
                ft.Container(
                    width=70,
                    height=100,
                    content=ft.Image(src=f"/images/card_back{i}.png"),
                    border_radius=ft.border_radius.all(6),
                    on_click=self.choose_card_design,
                    data=i,
                )
            )
        self.selected_card = self.card_backs[0]

    def choose_card_design(self, e):
        for card in self.card_backs:
            if card.data != e.control.data:
                card.border = None
        e.control.border = ft.border.all(3)
        self.selected_card = e.control
        self.update()

    def cancel(self, e):
        self.waste_size.value = self.settings.waste_size
        self.deck_passes_allowed.value = self.settings.deck_passes_allowed
        self.open = False
        self.update()

    def apply_settings(self, e):
        self.open = False
        self.settings.waste_size = int(self.waste_size.value)
        self.settings.deck_passes_allowed = int(self.deck_passes_allowed.value)
        self.settings.card_back = self.selected_card.content.src
        self.on_settings_applied(self.settings)
        self.update()
