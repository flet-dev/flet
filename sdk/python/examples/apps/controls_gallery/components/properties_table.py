import flet as ft


class SourceCode(ft.Text):
    def __init__(self, control):
        super().__init__()
        self.control = control
        # self.update_source_code(control)

    def did_mount(self):
        self.update_source_code(self.control)

    def update_source_code(self, control):
        # for property in self.properties:
        #     if type(getattr(self.control, property["name"])).__name__ == "str":
        #         property_value = f"""'{getattr(self.control, property["name"])}'"""
        #     else:
        #         property_value = getattr(self.control, property["name"])
        #     text = text + f"{property["name"]}={property_value}, "
        # control_name = type(self.control).__name__
        print(control)

        # code = f"""ft.{control_name}({text})"""
        # self.value = code
        self.update()


class PropertyName(ft.Row):
    def __init__(self, name, description="Description"):
        super().__init__()
        self.controls = [
            ft.Text(name),
            ft.Icon(
                name=ft.Icons.INFO_OUTLINE, tooltip=ft.Tooltip(message=description)
            ),
        ]


class PropertiesList(ft.ListView):
    def __init__(self, properties, control, top_control=None):
        super().__init__()
        self.properties = properties
        self.control = control
        self.divider_thickness = 3
        self.width = 500
        self.auto_scroll = True
        if top_control is None:
            self.top_control = control
        else:
            self.top_control = top_control
        self.controls = self.get_properties_list()

    def get_dataclass_tile(self, property, object):
        def switch_changed(e):
            if e.control.value:
                setattr(self.control, property["name"], object)
            else:
                setattr(self.control, property["name"], None)
            self.top_control.update()

        if getattr(self.control, property["name"]) is None:
            switch_value = False
        else:
            switch_value = True
        switch = ft.Switch(
            value=switch_value,
            on_change=switch_changed,
            tooltip=ft.Tooltip(f"Set/Unset {property['name']} property"),
        )

        return ft.ExpansionTile(
            bgcolor=ft.Colors.OUTLINE_VARIANT,
            title=PropertyName(
                name=property["name"], description=property["description"]
            ),
            controls=[
                ft.Row(controls=[switch], alignment=ft.MainAxisAlignment.START),
                PropertiesList(
                    properties=property["properties"],
                    control=object,
                    top_control=self.top_control,
                ),
            ],
        )

    def get_properties_list(self):
        controls = []

        for property in self.properties:

            def add_list_item(e, property=property):
                items_list = getattr(self.control, property["name"])
                if items_list is None:
                    items_list = []
                dataclass_type = property["dataclass"]
                # adding new item to a list
                items_list.append(dataclass_type())
                # updating property with the new list
                setattr(self.control, property["name"], items_list)
                self.controls = self.get_properties_list()
                self.update()

            value = getattr(self.control, property["name"])

            if "list" in property["value_type"]:
                list_items = []
                n = 0
                if value is not None:
                    for _ in value:

                        def delete_item(e, property=property):
                            items_list = getattr(self.control, property["name"])
                            # removing item from the list
                            items_list.remove(items_list[e.control.data])
                            # updating property with the new list
                            setattr(self.control, property["name"], items_list)
                            # removing the tile
                            e.control.parent.parent.parent.controls.remove(
                                e.control.parent.parent
                            )
                            self.update()
                            self.control.update()

                        list_items.append(
                            ft.ExpansionTile(
                                bgcolor=ft.Colors.OUTLINE_VARIANT,
                                title=ft.Text(f"{property['name']}{n + 1}"),
                                controls=[
                                    PropertiesList(
                                        properties=property["properties"],
                                        # control=ft.TextSpan(text="Span 1 Text"),
                                        control=value[n],
                                        top_control=self.top_control,
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                ft.Icons.DELETE,
                                                on_click=delete_item,
                                                tooltip=ft.Tooltip(
                                                    f"Delete {property['name']}{n + 1}"
                                                ),
                                                data=n,
                                            )
                                        ]
                                    ),
                                ],
                            )
                        )
                        n += 1
                controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                        margin=5,
                        padding=5,
                        border_radius=3,
                        content=ft.Column(
                            [
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(property["name"]),
                                        ft.IconButton(
                                            icon=ft.Icons.ADD, on_click=add_list_item
                                        ),
                                        # list_items,
                                    ],
                                )
                            ]
                            + list_items,
                        ),
                    )
                )
            elif property["value_type"] == "dataclass":
                if value is None:
                    dataclass_type = property["dataclass"]
                    value = dataclass_type()
                    print(value)
                    # setting badge = ft.Badge()
                    # setattr(self.control, property["name"], value)
                controls.append(self.get_dataclass_tile(property, value))
            else:
                controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                        margin=5,
                        padding=5,
                        border_radius=3,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # ft.Text(property["name"]),
                                PropertyName(
                                    name=property["name"],
                                    description=property["description"],
                                ),
                                self.get_value_control(property),
                            ],
                        ),
                    )
                )

        return controls

    def value_changed(self, e):
        print(f"Control: {self.control}!")
        print(f"Top Control: {self.top_control}!")
        print(f"Property: {e.control.data}!")

        print(f"Value: {e.control.value}!")

        setattr(self.control, e.control.data, e.control.value)
        self.top_control.update()

    def get_value_control(self, property):
        value = getattr(self.control, property["name"])

        if property["value_type"] == "str":
            return ft.TextField(
                border_color=ft.Colors.SECONDARY,
                content_padding=3,
                value=value,
                data=property["name"],
                on_change=self.value_changed,
            )
        elif property["value_type"] == "number":
            return ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(property["min"]),
                    ft.Slider(
                        min=property["min"],
                        max=property["max"],
                        label="{value}%",
                        value=value,
                        data=property["name"],
                        on_change=self.value_changed,
                    ),
                    ft.Text(property["max"]),
                ],
            )
        elif property["value_type"] == "bool":
            return ft.Checkbox(
                value=value,
                data=property["name"],
                on_change=self.value_changed,
            )
        elif property["value_type"] == "enum":
            options = []

            options_list = property["values"]
            for item in options_list:
                options.append(ft.dropdown.Option(item.value))

            return ft.Dropdown(
                options=options,
                value=value,
                data=property["name"],
                on_select=self.value_changed,
            )
        elif property["value_type"] == "dataclass":
            if value is None:
                print("This dataclass value is None")

            properties_list = PropertiesList(
                properties=property["properties"], control=value
            )

            return properties_list
            # ft.Container(bgcolor=ft.Colors.YELLOW, width=30, height=30)
        else:
            return ft.Text("Something's wrong with the type")
