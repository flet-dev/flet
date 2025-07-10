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

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>iPhone</h3>
    <img src="/img/blog/adaptive/iphone-adaptive-app.png" className="screenshot-60" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>Android</h3>
    <img src="/img/blog/adaptive/android-adaptive-app.png" className="screenshot-60" style={{ width: '57%'}} />
  </div>
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

Note:
    [`adaptive`][flet.AdaptiveControl.adaptive] property can be set for an individual control or
    a container-controls (ex: `Row`, `Column`) that has children controls.
    If a container-control is made adaptive, all its children will be adaptive too,
    unless `adaptive` property is explicitly set to `False` for a child control.

Below is the list of adaptive Material controls and their matching Cupertino controls:

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/alertdialog">AlertDialog</a>
    <img src="/img/docs/adaptive-apps/alertdialog.png" className="screenshot-50" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinoalertdialog">CupertinoAlertDialog</a>
    <img src="/img/docs/adaptive-apps/cupertinoalertdialog.png" className="screenshot-60" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/buttons">Any button in Dialog actions</a>
        <img src="/img/docs/adaptive-apps/dialogactions.png" className="screenshot-30" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
      <a href="/docs/controls/cupertinodialogaction">CupertinoDialogAction</a>
    <img src="/img/docs/adaptive-apps/cupertinodialogactions.png" className="screenshot-40" />
  </div>
</div>


<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/appbar">AppBar</a>
    <img src="/img/docs/adaptive-apps/appbar.png" className="screenshot-60" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinoappbar">CupertinoAppBar</a>
    <img src="/img/docs/adaptive-apps/cupertinoappbar.png" className="screenshot-60" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/navigationbar">NavigationBar</a>
    <img src="/img/docs/adaptive-apps/navigationbar.png" className="screenshot-60" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinonavigationbar">CupertinoNavigationBar</a>
    <img src="/img/docs/adaptive-apps/cupertinonavigationbar.png" className="screenshot-70" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/listtile">ListTile</a>
    <img src="/img/docs/adaptive-apps/listtile.png" className="screenshot-70" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinolisttile">CupertinoListTile</a>
    <img src="/img/docs/adaptive-apps/cupertinolisttile.png" className="screenshot-70" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/textfield">TextField</a>
    <img src="/img/docs/adaptive-apps/textfield.png" className="screenshot-70" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinotextfield">CupertinoTextField</a>
    <img src="/img/docs/adaptive-apps/cupertinotextfield.png" className="screenshot-70" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/checkbox">Checkbox</a>
    <img src="/img/docs/adaptive-apps/checkbox.png" className="screenshot-10" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinocheckbox">CupertinoCheckbox</a>
    <img src="/img/docs/adaptive-apps/cupertinocheckbox.png" className="screenshot-10" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/slider">Slider</a>
    <img src="/img/docs/adaptive-apps/slider.png" className="screenshot-30" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinoslider">CupertinoSlider</a>
    <img src="/img/docs/adaptive-apps/cupertinoslider.png" className="screenshot-30" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/switch">Switch</a>
    <img src="/img/docs/adaptive-apps/switch.png" className="screenshot-10" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinoswitch">CupertinoSwitch</a>
    <img src="/img/docs/adaptive-apps/cupertinoswitch.png" className="screenshot-10" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/radio">Radio</a>
    <img src="/img/docs/adaptive-apps/radio.png" className="screenshot-10" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinoradio">CupertinoRadio</a>
    <img src="/img/docs/adaptive-apps/cupertinoradio.png" className="screenshot-10" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/filledbutton">FilledButton</a>
    <img src="/img/docs/adaptive-apps/filledbutton.png" className="screenshot-20" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinobutton">CupertinoFilledButton</a>
    <img src="/img/docs/adaptive-apps/cupertinofilledbutton.png" className="screenshot-30" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/filledtonalbutton">FilledTonalButton</a>
    <img src="/img/docs/adaptive-apps/filledtonalbutton.png" className="screenshot-20" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinobutton">CupertinoButton</a>
    <img src="/img/docs/adaptive-apps/cupertinobutton-filledtonal.png" className="screenshot-30" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/iconbutton">IconButton</a>
    <img src="/img/docs/adaptive-apps/icon-button.png" className="screenshot-10" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinobutton">CupertinoButton</a>
    <img src="/img/docs/adaptive-apps/icon-button-cupertino.png" className="screenshot-10" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/elevatedbutton">ElevatedButton</a>
    <img src="/img/docs/adaptive-apps/elevatedbutton.png" className="screenshot-20" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/cupertinobutton">CupertinoButton</a>
    <img src="/img/docs/adaptive-apps/cupertinobutton.png" className="screenshot-20" />
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/outlinedbutton">OutlinedButton</a>
    <img src="/img/docs/adaptive-apps/outlinedbutton.png" className="screenshot-20" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
  </div>
</div>

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <a href="/docs/controls/textbutton">TextButton</a>
    <img src="/img/docs/adaptive-apps/textbutton.png" className="screenshot-20" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
  </div>
</div>

## Custom adaptive controls

While Flet offers a number of [controls](#material-and-cupertino-controls) that will be adapted to a platform

automatically using their [`adaptive`][flet.Control.adaptive] property, there will be cases when you need more specific adaptive UI
presentation, for example, using different icon, background color, padding etc. depending on the platform.

With Flet, you can create your own reusable custom controls in Python that will inherit from a Flet control

and implement specific properties you need. In the example below, we are creating a new
`AdaptiveNavigationBarDestination` control that will be displaying different icon on iOS and Android:

```python
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
```

We will use `AdaptiveNavigationBarDestination` in `NavigationBar`:

```python
import flet as ft
from adaptive_navigation_destination import AdaptiveNavigationBarDestination

def main(page):

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

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>iOS</h3>
    <img src="/img/docs/adaptive-apps/navigation-bar-custom-ios.png" className="screenshot-100" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>Android</h3>
    <img src="/img/docs/adaptive-apps/navigation-bar-custom-android.png" className="screenshot-100"/>
  </div>
</div>

/// admonition | Note
You may utilise [reusable controls approach](../cookbook/custom-controls.md) to
adapt your app not only depending on the [`Page.platform`][flet.Page.platform],
but also use [`Page.web`][flet.Page.web] property to have different UI depending on whether the
app is running in a browser or not, or even combine the usage of both properties to have specific
UI for your apps.
///
