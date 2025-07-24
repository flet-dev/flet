While Flet controls leverage many built-in Flutter widgets, enabling the creation of complex applications, not all Flutter widgets or third-party packages can be directly supported by the Flet team or included within the core Flet framework.

To address this, the Flet framework provides an extensibility mechanism. This allows you to incorporate widgets and APIs from your own custom Flutter packages or [third-party libraries](https://pub.dev/packages?sort=popularity) directly into your Flet application.

In this guide, you will learn how to create Flet extension from template and then customize it to integrate 3rd-party Flutter package into your Flet app or share it with community.

### Prerequisites

To integrate custom Flutter package into Flet you need to have basic understanding of how to create Flutter apps and packages in Dart language and have Flutter development environment configured. See [Flutter Getting Started](https://docs.flutter.dev/get-started/install) for more information about Flutter and Dart.

## Create Flet extension from template

Flet now makes it easy to create and build projects with your custom controls based on Flutter widgets or Flutter 3rd-party packages. In the example below, we will be creating a custom Flet extension based on the [flutter_spinkit](https://pub.dev/packages/flutter_spinkit) package.

1. Create new virtual enviroment and [install Flet](/docs/getting-started/#virtual-environment) there.

2. Create new Flet extension project from template:

```
flet create --template extension --project-name flet-spinkit
```

A project with new FletSpinkit control will be created. The control is just a Flutter Text widget with text property, which we will customize later.

3. Build your app.

Flet project created from extension template has `examples/flet_spinkit_example` folder with the example app.

When in the folder where your `pyproject.toml` for the app is (`examples/flet_spinkit_example`), run `flet build` command, for example, for macos:

```
flet build macos -v
```

Open the app and see the new custom Flet Control:

```
open build/macos/flet-spinkit-example.app
```

<img src="/img/docs/extending-flet/example.png" className="screenshot-30" />

4. Change your app.

Once the project was built for desktop once, you can make changes to your python files and run it without re-building.

First, if you are not using uv, install dependencies from pyproject.toml:

```
pip install .
```
or
```
poetry install
```

Now you can make changes to your example app main.py:

```
import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Container(
            height=150,
            width=300,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.PINK_200,
            content=FletSpinkit(
                tooltip="My new PINK FletSpinkit Control tooltip",
                value="My new PINK FletSpinkit Flet Control",
            ),
        ),
    )


ft.app(main)
```

and run:

```
flet run
```

<img src="/img/docs/extending-flet/example-pink.png" className="screenshot-30" />

5. Re-build your app.

When you make any changes to your flutter package, you need to re-build:

```
flet build macos -v
```

If you need to debug, run this command:

```
build/macos/flet-spinkit-example.app/Contents/MacOS/flet-spinkit-example --debug
```

## Integrate 3rd-party Flutter package

Let's integrate [flutter_spinkit](https://pub.dev/packages/flutter_spinkit) package into our Flet app.

1. Add dependency.

Go to `src/flutter/flet_spinkit` folder and run this command to add dependency to `flutter_spinkit` to `pubspec.yaml`:

```
flutter pub add flutter_spinkit
```

Read more information about using Flutter packages [here](https://docs.flutter.dev/packages-and-plugins/using-packages).

2. Modify `dart` file.

In the `src/flutter/flet_spinkit/lib/src/flet_spinkit.dart` file, add import statement and replace Text widget with `SpinKitRotatingCircle` widget:

```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class FletSpinkitControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const FletSpinkitControl({
    super.key,
    required this.parent,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    Widget myControl = SpinKitRotatingCircle(
      color: Colors.red,
      size: 100.0,
    );


    return constrainedControl(context, myControl, parent, control);
  }
}
```

3. Rebuild your example app.

Go to `examples/flet_spinkit_example`, clear cache and rebuild your app:

```
flet build macos -v
```

4. Run your app:

<img src="/img/docs/extending-flet/spinkit1.gif" className="screenshot-30" />

## Flet extension structure

After creating new Flet project from extension template, you will see the following folder structure:

```
├── LICENSE
├── mkdocs.yml
├── README.md
├── docs
│   └── index.md
│   └── FletSpinkit.md
├── examples
│   └── flet_spinkit_example
│       ├── README.md
│       ├── pyproject.toml
│       └── src
│           └── main.py
├── pyproject.toml
└── src
    ├── flet_spinkit
    │   ├── __init__.py
    │   └── flet_spinkit.py
    └── flutter
        └── flet_spinkit
            ├── CHANGELOG.md
            ├── LICENSE
            ├── README.md
            ├── lib
            │   ├── flet_spinkit.dart
            │   └── src
            │       ├── create_control.dart
            │       └── flet_spinkit.dart
            └── pubspec.yaml
```

Flet extension consists of:
* **package**, located in `src` folder
* **example app**, located in `examples/flet-spinkit_example` folder
* **docs**, located in `docs` folder

### Package

Package is the component that will be used in your app. It contists of two parts: Python and Flutter.

#### Python

##### flet_spinkit.py

Here you create Flet Python control - a Python class that you use in your Flet app.

The minumal requirements for this class is that it has to be inherited from Flet `Control` and it has to
have `_get_control_name` method that will return the control name. This name should be the same as `args.control.type`
we check in the `create_control.dart` file.

#### Flutter

##### pubspec.yaml

A yaml file containing metadata that specifies the package's dependencies.

There is already a dependency to `flet` created from template. You need to add there a dependency to Flutter package for which you are creating your extension.

##### flet_spinkit.dart

Two methods are exported:
* `createControl` - called to create a widget that corresponds to a control on Python side.
* `ensureInitialized` - called once on Flet program start.

##### src/create_control.dart

Creates Flutter widget based on control names returned by the Control's `_get_control_name()` function. This mechanism iterates through all third-party packages and returns the first matching widget.

##### src/flet_spinkit.dart

Here you create Flutter "wrapper" widget that will build Flutter widget or API that you want to use in your Flet app.

Wrapper widget passes the state of Python control down to a Flutter widget, that will be displayed on a page, and provides an API to route events from Flutter widget back to Python control.

### Example app

##### src/main.py

Python program that uses Flet Python control.

##### pyproject.toml

Here you specify dependency to your package, which can be:

* **Path dependency**

Absolute path to your Flet extension folder, for example:

```
dependencies = [
  "flet-spinkit @ file:///Users/user-name/projects/flet-spinkit",
  "flet>=0.26.0",
]
```

* **Git dependency**

Link to git repository, for example:

```
dependencies = [
  "flet-ads @ git+https://github.com/flet-dev/flet-ads.git",
  "flet>=0.26.0",
]
```

* **PyPi dependency**

Name of the package published on pypi.org, for example:

```
dependencies = [
  "flet-ads",
  "flet>=0.26.0",
]
```

### Docs

If you are planning to share your extension with community, you can easily generate documenation from your source code using [mkdocs](https://www.mkdocs.org/).

Flet extension comes with `docs` folder containing initial files for your documentation and `mkdocs.yml`.

Run the following command to see how your docs look locally:

```
mkdocs serve
```

Open http://127.0.0.1:8000 in your browser:

<img src="/img/docs/extending-flet/mkdocs.png" className="screenshot-50" />

Once your documentation is ready, if your package is hosted on GitHub, your can run the following command to host your documentation on GitHub pages:

```
mkdocs gh-deploy
```

You may find [this guide](https://realpython.com/python-project-documentation-with-mkdocs/#step-5-build-your-documentation-with-mkdocs) helpful to get started with mkdocs.

## Customize properties

In the example above, Spinkit control creates a hardcoded Flutter widget. Now let's customize its properties.

### Common properties

Generally, there are two types of controls in Flet:

1. Visual controls that are added to the app/page surface, such as FletSpinkit.

2. Non-visual controls that can be:

    * popup controls (dialogs, pickers, panels etc.).

    * services that are added to `overlay`, such as Video or Audio.

Flet `Control` class has properties common for all controls such as `visible`, `opacity` and `tooltip`, to name a few.

Flet `ConstrainedControl` class is inherited from `Control` and has many additional properties such as `top` and `left` for its position within Stack and a bunch of animation properties.

When creating non-visual control, your Python control should be inherited from ['Control](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/control.py). Then, to be able to use `Control` properties in your app, you need to add them to the constructor of your Python Control. In its dart counterpart (`src/flet_spinkit.dart`) use `baseControl()` to wrap your Flutter widget.

When creating visual control, your Python control should be inherited from [`ConstrainedControl`](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/constrained_control.py). In its dart counterpart (`src/flet_spinkit.dart`) use `constrainedControl()`  to wrap your Flutter widget.

Then, to be able to use `Control` and `ConstrainedControl` properties in your app, you need to add them to the constructor of your Python Control.

See reference for the common Control properties [here](https://flet.dev/docs/controls).

If you have created your extension project from Flet extension template, your Python Control is already inherited from `ConstrainedControl` and you can use its properties in your example app:

```python
import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Stack(
            [
                ft.Container(height=200, width=200, bgcolor=ft.Colors.BLUE_100),
                FletSpinkit(opacity=0.5, tooltip="Spinkit tooltip", top=0, left=0),
            ]
        )
    )


ft.app(main)
```

<img src="/img/docs/extending-flet/spinkit2.gif" className="screenshot-30" />

### Control-specific properties

Now that you have taken full advantage of the properties Flet `Control` and `ConstrainedControl` offer, let's define the properties that are specific to the new Control you are building.

In the FletSpinkit example, let's define its `color` and `size`.

In Python class, define new `color` and `size` properties:

```python
from enum import Enum
from typing import Any, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.types import ColorEnums, ColorValue


class FletSpinkit(ConstrainedControl):
    """
    FletSpinkit Control.
    """

    def __init__(
        self,
        #
        # Control
        #
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # ConstrainedControl
        #
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        #
        # FletSpinkit specific
        #
        color: Optional[ColorValue] = None,
        size: OptionalNumber = None,
    ):
        ConstrainedControl.__init__(
            self,
            tooltip=tooltip,
            opacity=opacity,
            visible=visible,
            data=data,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )

        self.color = color
        self.size = size

    def _get_control_name(self):
        return "flet_spinkit"

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # size
    @property
    def size(self):
        return self._get_attr("size")

    @size.setter
    def size(self, value):
        self._set_attr("size", value)
```

In `src/flet_spinkit.dart` file, use helper methods `attrColor` and `attrDouble` to access color and size values:

```dart
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class FletSpinkitControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const FletSpinkitControl({
    super.key,
    required this.parent,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    var color = control.attrColor("color", context);
    var size = control.attrDouble("size");
    Widget myControl = SpinKitRotatingCircle(
      color: color,
      size: size ?? 100,
    );


    return constrainedControl(context, myControl, parent, control);
  }
}
```

Use `color` and `size` properties in your app:

```python
import flet as ft

from flet_spinkit import FletSpinkit


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Stack(
            [
                ft.Container(height=200, width=200, bgcolor=ft.Colors.BLUE_100),
                FletSpinkit(
                    opacity=0.5,
                    tooltip="Spinkit tooltip",
                    top=0,
                    left=0,
                    color=ft.Colors.YELLOW,
                    size=150,
                ),
            ]
        )
    )


ft.app(main)
```

Re-build and run:

<img src="/img/docs/extending-flet/spinkit3.gif" className="screenshot-20" />

You can find source code for this example [here](https://github.com/flet-dev/flet-spinkit).

#### Examples for different types of properties and events

##### Enum properties

For example, `clip_behaviour` for `AppBar`.

In [Python](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/app_bar.py):

```python
# clip_behavior
@property
def clip_behavior(self) -> Optional[ClipBehavior]:
    return self._get_attr("clipBehavior")

@clip_behavior.setter
def clip_behavior(self, value: Optional[ClipBehavior]):
    self._set_attr(
        "clipBehavior",
        value.value if isinstance(value, ClipBehavior) else value,
    )
```

In [Dart](https://github.com/flet-dev/flet/blob/main/packages/flet/lib/src/controls/app_bar.dart):

```dart
var clipBehavior = Clip.values.firstWhere(
    (e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("clipBehavior", "")!.toLowerCase(),
    orElse: () => Clip.none);
```
##### Json properties

For example, `shape` property for `Card`.

In [Python](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/card.py):

```python
def before_update(self):
    super().before_update()
    self._set_attr_json("shape", self.__shape)

# shape
@property
def shape(self) -> Optional[OutlinedBorder]:
    return self.__shape

@shape.setter
def shape(self, value: Optional[OutlinedBorder]):
    self.__shape = value
```

In [Dart](https://github.com/flet-dev/flet/blob/main/packages/flet/lib/src/controls/card.dart):

```dart
var shape = parseOutlinedBorder(control, "shape")
```

##### Children

For example, `content` for `AlertDialog`:

In [Python](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/alert_dialog.py):

```python
    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children
```

In [Dart](https://github.com/flet-dev/flet/blob/main/packages/flet/lib/src/controls/alert_dialog.dart):

```dart
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
```

##### Events

For example, `on_click` event for `ElevatedButton`.

In [Python](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet/src/flet/core/elevated_button.py):

```python
# on_click
@property
def on_click(self):
    return self._get_event_handler("click")

@on_click.setter
def on_click(self, handler):
    self._add_event_handler("click", handler)
```

In [Dart](https://github.com/flet-dev/flet/blob/main/packages/flet/lib/src/controls/elevated_button.dart):

```dart
Function()? onPressed = !disabled
    ? () {
        debugPrint("Button ${widget.control.id} clicked!");
        if (url != "") {
        openWebBrowser(url,
            webWindowName: widget.control.attrString("urlTarget"));
        }
        widget.backend.triggerControlEvent(widget.control.id, "click");
    }
    : null;
```

## Examples

Flet has controls that are implemented as [built-in extensions](/docs/extend/built-in-extensions) and could serve as a starting point for your own controls.
