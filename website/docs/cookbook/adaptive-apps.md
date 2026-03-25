---
title: "Adaptive apps"
example_media: "../examples/controls"
---

import {Image} from '@site/src/components/crocodocs';

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

| iPhone | Android |
|:---:|:---:|
| <Image src="/docs/assets/cookbook/adaptive-apps/iphone.png" width="80%" /> | <Image src="/docs/assets/cookbook/adaptive-apps/android.png" width="80%" /> |

## Material and Cupertino controls

Most of Flet controls are based on [Material design](https://m3.material.io/).

There is also a number of iOS-style controls in Flet that are called Cupertino controls.

Cupertino controls usually have a matching Material control that has [`adaptive`](../controls/adaptivecontrol.md#flet.AdaptiveControl-adaptive) property
which defaults to`False`. When using a Material control with `adaptive` property set to `True`,
a different control will
be created depending on the platform, for example:
```python
ft.Checkbox(adaptive=True, value=True, label="Adaptive Checkbox")
```

Flet checks the value of [`Page.platform`](../controls/page.md#flet.Page-platform) property and if it is
`PagePlatform.IOS` or `ft.PagePlatform.MACOS`, Cupertino control will be created;
in all other cases Material control will be created.

:::note[Note]
[`adaptive`](../controls/adaptivecontrol.md#flet.AdaptiveControl-adaptive) property can be set for an individual control or
a container-controls (ex: [`Row`](../controls/row.md), [`Column`](../controls/column.md)) that has children controls.
If a container-control is made adaptive, all its children will be adaptive too,
unless `adaptive` property is explicitly set to `False` for a child control.
:::

<details>
<summary>Material vs Cupertino</summary>

Below is the list of adaptive Material controls and their matching Cupertino controls:

| Material | Cupertino |
|:---:|:---:|
| [`AlertDialog`](../controls/alertdialog.md) | [`CupertinoAlertDialog`](../controls/cupertinoalertdialog.md) |
| <Image src={frontMatter.example_media + '/alert_dialog/media/index.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_alert_dialog/media/adaptive.png'} width="55%" /> |
| [`Dialog actions`](../controls/button.md) | [`CupertinoDialogAction`](../controls/cupertinodialogaction.md) |
| <Image src={frontMatter.example_media + '/alert_dialog/media/adaptive_dialog_action.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_alert_dialog/media/adaptive_dialog_action.png'} width="55%" /> |
| [`AppBar`](../controls/appbar.md) | [`CupertinoAppBar`](../controls/cupertinoappbar.md) |
| <Image src={frontMatter.example_media + '/app_bar/media/index.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_app_bar/media/index.png'} width="55%" /> |
| [`NavigationBar`](../controls/navigationbar/index.md) | [`CupertinoNavigationBar`](../controls/cupertinonavigationbar.md) |
| <Image src={frontMatter.example_media + '/navigation_bar/media/adaptive.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_navigation_bar/media/adaptive.png'} width="55%" /> |
| [`ListTile`](../controls/listtile.md) | [`CupertinoListTile`](../controls/cupertinolisttile.md) |
| <Image src={frontMatter.example_media + '/list_tile/media/index.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_list_tile/media/index.png'} width="55%" /> |
| [`TextField`](../controls/textfield.md) | [`CupertinoTextField`](../controls/cupertinotextfield.md) |
| <Image src={frontMatter.example_media + '/text_field/media/index.png'} width="55%" /> | <Image src={frontMatter.example_media + '/cupertino_text_field/media/index.png'} width="55%" /> |
| [`Checkbox`](../controls/checkbox.md) | [`CupertinoCheckbox`](../controls/cupertinocheckbox.md) |
| <Image src={frontMatter.example_media + '/checkbox/media/index.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_checkbox/media/index.png'} width="45%" /> |
| [`Slider`](../controls/slider.md) | [`CupertinoSlider`](../controls/cupertinoslider.md) |
| <Image src="/docs/test-images/examples/material/golden/macos/slider/image_for_docs.png" width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_slider/media/index.png'} width="45%" /> |
| [`Switch`](../controls/switch.md) | [`CupertinoSwitch`](../controls/cupertinoswitch.md) |
| <Image src={frontMatter.example_media + '/switch/media/index.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_switch/media/index.png'} width="45%" /> |
| [`Radio`](../controls/radio.md) | [`CupertinoRadio`](../controls/cupertinoradio.md) |
| <Image src={frontMatter.example_media + '/radio/media/index.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_radio/media/index.png'} width="45%" /> |
| [`FilledButton`](../controls/filledbutton.md) | [`CupertinoFilledButton`](../controls/cupertinofilledbutton.md) |
| <Image src={frontMatter.example_media + '/filled_button/media/adaptive.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_filled_button/media/adaptive.png'} width="45%" /> |
| [`FilledTonalButton`](../controls/filledtonalbutton.md) | [`CupertinoButton`](../controls/cupertinobutton.md) |
| <Image src={frontMatter.example_media + '/filled_tonal_button/media/adaptive.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_button/media/adaptive_tonal_button.png'} width="45%" /> |
| [`IconButton`](../controls/iconbutton.md) | [`CupertinoButton`](../controls/cupertinobutton.md) |
| <Image src={frontMatter.example_media + '/icon_button/media/adaptive.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_button/media/adaptive_icon_button.png'} width="45%" /> |
| [`Button`](../controls/button.md) / [`OutlinedButton`](../controls/outlinedbutton.md) / [`TextButton`](../controls/textbutton.md) | [`CupertinoButton`](../controls/cupertinobutton.md) |
| <Image src={frontMatter.example_media + '/button/media/adaptive.png'} width="45%" /> <Image src={frontMatter.example_media + '/outlined_button/media/adaptive.png'} width="45%" /> <Image src={frontMatter.example_media + '/text_button/media/adaptive.png'} width="45%" /> | <Image src={frontMatter.example_media + '/cupertino_button/media/adaptive.png'} width="45%" /> |

</details>

## Custom adaptive controls

While Flet offers a number of [controls](#material-and-cupertino-controls) that will be adapted to a platform

automatically using their [`adaptive`](../controls/adaptivecontrol.md#flet.AdaptiveControl-adaptive) property, there will be
cases when you need more specific adaptive UI presentation, for example, using different
icon, background color, padding, etc., depending on the platform.

With Flet, you can create your own reusable custom controls in Python that will inherit from a Flet control
and implement specific properties you need.

In the example below, we are creating a new `AdaptiveNavigationBarDestination`
[custom control](custom-controls.md) that will be displaying different icon on iOS and Android, and use it
as destination for the [`NavigationBar`](../controls/navigationbar/index.md):

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

| iOS | Android |
|:---:|:---:|
| <Image src={frontMatter.example_media + '/navigation_bar/media/adaptive.png'} width="60%" /> | <Image src={frontMatter.example_media + '/navigation_bar/media/adaptive.png'} width="60%" /> |

:::note[Note]
You may utilise [reusable controls approach](../cookbook/custom-controls.md) to
adapt your app not only depending on the [`Page.platform`](../controls/page.md#flet.Page-platform),
but also use [`Page.web`](../controls/page.md#flet.Page-web) property to have different UI depending on whether the
app is running in a browser or not, or even combine the usage of both properties to have specific
UI for your apps.
:::
