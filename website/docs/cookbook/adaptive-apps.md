---
title: "Adaptive apps"
---

Flet framework allows you to develop adaptive apps which means having a single codebase that
will deliver different look depending on the device's platform.

Below is the example of a very simple app that has a different look on iOS and Android platforms:

```python
import flet as ft

def main(page):

    page.adaptive = True

    page.appbar = ft.AppBar(
        leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
        title=ft.Text("Adaptive AppBar"),
        actions=[
            ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Bookmark",
            ),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.CupertinoColors.SYSTEM_GREY2, width=0)
        ),
    )

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Checkbox(value=False, label="Dark Mode"),
                    ft.Text("First field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Text("Second field:"),
                    ft.TextField(keyboard_type=ft.KeyboardType.TEXT),
                    ft.Switch(label="A switch"),
                    ft.FilledButton(content=ft.Text("Adaptive button")),
                    ft.Text("Text line 1"),
                    ft.Text("Text line 2"),
                    ft.Text("Text line 3"),
                ]
            )
        )
    )

ft.run(main)
```

By setting just `page.adaptive = True` you can make you app looking awesome on both iOS and Android devices:

<div class="grid cards" markdown>

-   **iPhone**

    ---
    <img alt="iPhone" src="/docs/assets/cookbook/adaptive-apps/iphone.png" style={{width: "80%"}} />

-   **Android**

    ---
    <img alt="Android" src="/docs/assets/cookbook/adaptive-apps/android.png" style={{width: "80%"}} />

</div>

## Material and Cupertino controls

Most of Flet controls are based on [Material design](https://m3.material.io/).

There is also a number of iOS-style controls in Flet that are called Cupertino controls.

Cupertino controls usually have a matching Material control that has [`adaptive`][flet.AdaptiveControl.adaptive] property
which defaults to`False`. When using a Material control with `adaptive` property set to `True`,
a different control will
be created depending on the platform, for example:
```python
ft.Checkbox(adaptive=True, value=True, label="Adaptive Checkbox")
```

Flet checks the value of [`Page.platform`][flet.Page.platform] property and if it is
`PagePlatform.IOS` or `ft.PagePlatform.MACOS`, Cupertino control will be created;
in all other cases Material control will be created.

:::note[Note]
[`adaptive`][flet.AdaptiveControl.adaptive] property can be set for an individual control or
a container-controls (ex: [`Row`][flet.Row], [`Column`][flet.Column]) that has children controls.
If a container-control is made adaptive, all its children will be adaptive too,
unless `adaptive` property is explicitly set to `False` for a child control.
:::

<details>
<summary>Material vs Cupertino</summary>

Below is the list of adaptive Material controls and their matching Cupertino controls:

<div class="grid cards" markdown>

-   [:octicons-arrow-right-24: `AlertDialog`][flet.AlertDialog]

    ---
    <img alt="AlertDialog" src="/docs/examples/controls/alert_dialog/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoAlertDialog`][flet.CupertinoAlertDialog]

    ---
    <img alt="CupertinoAlertDialog" src="/docs/examples/controls/cupertino_alert_dialog/media/adaptive.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `Any button in Dialog actions`][flet.Button]

    ---
    <img alt="Dialog actions" src="/docs/examples/controls/alert_dialog/media/adaptive_dialog_action.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoDialogAction`][flet.CupertinoDialogAction]

    ---
    <img alt="CupertinoDialogAction" src="/docs/examples/controls/cupertino_alert_dialog/media/adaptive_dialog_action.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `AppBar`][flet.AppBar]

    ---
    <img alt="AppBar" src="/docs/examples/controls/app_bar/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoAppBar`][flet.CupertinoAppBar]

    ---
    <img alt="CupertinoAppBar" src="/docs/examples/controls/cupertino_app_bar/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `NavigationBar`][flet.NavigationBar]

    ---
    <img alt="NavigationBar" src="/docs/examples/controls/navigation_bar/media/adaptive.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoNavigationBar`][flet.CupertinoNavigationBar]

    ---
    <img alt="CupertinoNavigationBar" src="/docs/examples/controls/cupertino_navigation_bar/media/adaptive.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `ListTile`][flet.ListTile]

    ---
    <img alt="ListTile" src="/docs/examples/controls/list_tile/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoListTile`][flet.CupertinoListTile]

    ---
    <img alt="CupertinoListTile" src="/docs/examples/controls/cupertino_list_tile/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `TextField`][flet.TextField]

    ---
    <img alt="TextField" src="/docs/examples/controls/text_field/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `CupertinoTextField`][flet.CupertinoTextField]

    ---
    <img alt="CupertinoTextField" src="/docs/examples/controls/cupertino_text_field/media/index.png" style={{width: "85%"}} />

-   [:octicons-arrow-right-24: `Checkbox`][flet.Checkbox]

    ---
    <img alt="Checkbox" src="/docs/examples/controls/checkbox/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoCheckbox`][flet.CupertinoCheckbox]

    ---
    <img alt="CupertinoCheckbox" src="/docs/examples/controls/cupertino_checkbox/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `Slider`][flet.Slider]

    ---
    <img alt="Slider" src="/docs/test-images/examples/material/golden/macos/slider/image_for_docs.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoSlider`][flet.CupertinoSlider]

    ---
    <img alt="CupertinoSlider" src="/docs/examples/controls/cupertino_slider/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `Switch`][flet.Switch]

    ---
    <img alt="Switch" src="/docs/examples/controls/switch/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoSwitch`][flet.CupertinoSwitch]

    ---
    <img alt="CupertinoSwitch" src="/docs/examples/controls/cupertino_switch/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `Radio`][flet.Radio]

    ---
    <img alt="Radio" src="/docs/examples/controls/radio/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoRadio`][flet.CupertinoRadio]

    ---
    <img alt="CupertinoRadio" src="/docs/examples/controls/cupertino_radio/media/index.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `FilledButton`][flet.FilledButton]

    ---
    <img alt="FilledButton" src="/docs/examples/controls/filled_button/media/adaptive.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoFilledButton`][flet.CupertinoFilledButton]

    ---
    <img alt="CupertinoFilledButton" src="/docs/examples/controls/cupertino_filled_button/media/adaptive.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `FilledTonalButton`][flet.FilledTonalButton]

    ---
    <img alt="FilledTonalButton" src="/docs/examples/controls/filled_tonal_button/media/adaptive.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoButton`][flet.CupertinoButton]

    ---
    <img alt="CupertinoButtonTonal" src="/docs/examples/controls/cupertino_button/media/adaptive_tonal_button.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `IconButton`][flet.IconButton]

    ---
    <img alt="IconButton" src="/docs/examples/controls/icon_button/media/adaptive.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoButton`][flet.CupertinoButton]

    ---
    <img alt="CupertinoIconButton" src="/docs/examples/controls/cupertino_button/media/adaptive_icon_button.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `Button`][flet.Button]

    <img alt="Button" src="/docs/examples/controls/button/media/adaptive.png" style={{width: "45%"}} />

    ---
    [:octicons-arrow-right-24: `OutlinedButton`][flet.OutlinedButton]

    <img alt="OutlinedButton" src="/docs/examples/controls/outlined_button/media/adaptive.png" style={{width: "45%"}} />

    ---
    [:octicons-arrow-right-24: `TextButton`][flet.TextButton]

    <img alt="TextButton" src="/docs/examples/controls/text_button/media/adaptive.png" style={{width: "45%"}} />

-   [:octicons-arrow-right-24: `CupertinoButton`][flet.CupertinoButton]

    ---
    <img alt="CupertinoButton" src="/docs/examples/controls/cupertino_button/media/adaptive.png" style={{width: "45%"}} />

</div>

</details>

## Custom adaptive controls

While Flet offers a number of [controls](#material-and-cupertino-controls) that will be adapted to a platform

automatically using their [`adaptive`][flet.AdaptiveControl.adaptive] property, there will be
cases when you need more specific adaptive UI presentation, for example, using different
icon, background color, padding, etc., depending on the platform.

With Flet, you can create your own reusable custom controls in Python that will inherit from a Flet control
and implement specific properties you need.

In the example below, we are creating a new `AdaptiveNavigationBarDestination`
[custom control](custom-controls.md) that will be displaying different icon on iOS and Android, and use it
as destination for the [`NavigationBar`][flet.NavigationBar]:

```python
import flet as ft

class AdaptiveNavigationBarDestination(ft.NavigationBarDestination):
    def __init__(self, ios_icon, android_icon, label):
        super().__init__()
        self._ios_icon = ios_icon
        self._android_icon = android_icon
        self.label = label

    def build(self):
        # we can check for platform in build method because self.page is known
        self.icon = (
            self._ios_icon
            if self.page.platform == ft.PagePlatform.IOS
            or self.page.platform == ft.PagePlatform.MACOS
            else self._android_icon
        )

def main(page: ft.Page):
    page.adaptive = True

    page.navigation_bar = ft.NavigationBar(
        selected_index=2,
        destinations=[
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.PERSON_3_FILL,
                android_icon=ft.Icons.PERSON,
                label="Contacts",
            ),
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.CHAT_BUBBLE_2,
                android_icon=ft.Icons.CHAT,
                label="Chats",
            ),
            AdaptiveNavigationBarDestination(
                ios_icon=ft.cupertino_icons.SETTINGS,
                android_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
    )

    page.update()

ft.run(main)
```

Now the `NavigationBar` and icons within it will look like different on Android and iOS:

<div class="grid cards" markdown>

-   **iOS**

    ---
    <img alt="CupertinoNavigationBar" src="/docs/examples/controls/navigation_bar/media/adaptive.png" style={{width: "90%"}} />

-   **Android**

    ---
    <img alt="CupertinoNavigationBar" src="/docs/examples/controls/navigation_bar/media/adaptive.png" style={{width: "90%"}} />

</div>

:::note[Note]
You may utilise [reusable controls approach](../cookbook/custom-controls.md) to
adapt your app not only depending on the [`Page.platform`][flet.Page.platform],
but also use [`Page.web`][flet.Page.web] property to have different UI depending on whether the
app is running in a browser or not, or even combine the usage of both properties to have specific
UI for your apps.
:::
