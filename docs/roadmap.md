# Flet Roadmap

## Sprint 1

* Controls
  * Common
    * [ ] Control
    * [x] Page
  * Layout
    * [x] Container
    * [x] Row (flex - default mode, wrap)
    * [x] Column (flex - default mode, wrap)
    * [x] Stack
    * [x] ListView
    * [x] GridView
    * [x] Divider
    * [x] VerticalDivider
  * App structure and navigation
    * [x] Tabs
    * [ ] AppBar
    * [ ] NavigationRail
  * Basic controls
    * [x] Text
    * [x] Icon
    * [x] Image (+custom assets directory for Flet server [see here](https://docs.flutter.dev/development/platform-integration/web-images)).
    * [x] CircleAvatar
    * [x] ProgressBar
    * [x] ProgressRing
  * Buttons
    * [x] ElevatedButton
    * [x] FilledButton
    * [x] FilledTonalButton
    * [x] OutlinedButton
    * [x] TextButton
    * [x] IconButton
    * [x] FloatingActionButton
    * [x] PopupMenuButton
  * Input and selections
    * [x] TextField
    * [x] Dropdown
    * [x] Checkbox
    * [x] RadioGroup and Radio
    * [x] Slider
    * [x] Switch
  * Dialogs, alerts and panels
    * [x] Banner
    * [x] SnackBar
    * [x] AlertDialog

* Flet Client
  * [x] Web
  * [x] Windows ("client" mode - started from Python)
  * [x] macOS ("client" mode - started from Python)

* Flet Daemon
  * [x] "assets" directory with static content

* Samples apps
  * [x] Counter
  * [x] To-Do
  * [x] Icon browser
  * [ ] Chat

* Website
  * [ ] Controls S1 reference
  * [x] Introduction
  * [ ] Home page
  * [ ] Blog post
  * [ ] Python Guide
    * Deployment (+how to change favicon.ico)
      * [x] Deployment to Replit
      * [x] Deployment to Fly.io

## Sprint 2

* Authentication
* Controls
  * Navigation
    * NavigationDrawer
    * NavigationBar
  * Layout
    * Row (responsive)
    * Column (responsive)
  * Behavior
    * Visual Density ([more](https://api.flutter.dev/flutter/material/VisualDensity-class.html))
    * Early detection of layout issues (like enabling scrolling in unbounded controls) with [Layout Builder](https://api.flutter.dev/flutter/widgets/LayoutBuilder-class.html).
    * Scroll speed on Windows Desktop [The issue](https://github.com/flutter/flutter/issues/67985)

* Flet Client
  * Web
    * [Loading splash](https://docs.flutter.dev/development/platform-integration/web/initialization)
  * [ ] Windows ("host" mode with hot reload)
  * [ ] macOS ("host" mode with hot reload)

## Year 2022

* Grids
* Charts
* Navigation controls and Routing
* Responsive layout
* Adaptive controls
* Animations
* PubSub
* DB

## Controls

<table>
    <tr>
        <th>✓ Status</th>
        <th>Flet</th>
        <th>Pglet</th>
        <th>Sprint</th>
    </tr>
    <tr><th colspan="4">Layout</th></tr>
    <tr>
        <td>✓</td>
        <td>Container</td>
        <td>Stack</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Row</td>
        <td>Stack horizontal=True</td>
        <td>S1 (flex, wrap)</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Column</td>
        <td>Stack horizontal=False</td>
        <td>S1 (flex, wrap)</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Stack</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>ListView</td>
        <td>Stack horizontal=False</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Divider</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>Spacer</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>GridView</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td><a href="https://pub.dev/packages/split_view">SplitView</a></td>
        <td>SplitStack</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>Card</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr><th colspan="4">Basic controls</th></tr>
    <tr>
        <td>✓</td>
        <td>Text</td>
        <td>Text</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Markdown</td>
        <td>Text markdown=True</td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Icon</td>
        <td>Icon</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Image</td>
        <td>Image</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>CircleAvatar</td>
        <td>Persona</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Chip</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td><a href="https://stackoverflow.com/questions/43583411/how-to-create-a-hyperlink-in-flutter-widget">To-Do</a></td>
        <td>Link</td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>ProgressBar</td>
        <td>Progress</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>ProgressRing</td>
        <td>Spinner</td>
        <td>S1</td>
    </tr>
    <tr><th colspan="4">Buttons</th></tr>
    <tr>
        <td>✓</td>
        <td>ElevatedButton</td>
        <td>Button primary=True</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>OutlinedButton</td>
        <td>Button primary=False</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>TextButton</td>
        <td>Button action=True</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>IconButton</td>
        <td>Button icon={icon_name}</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>PopupMenuButton</td>
        <td>Button with MenuItems</td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>FloatingActionButton</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr><th colspan="4">Input and selections</th></tr>
    <tr>
        <td>✓</td>
        <td>Checkbox</td>
        <td>Checkbox</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Radio</td>
        <td>ChoiceGroup</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Dropdown</td>
        <td>Dropdown</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>-</td>
        <td>ComboBox</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>DatePicker</td>
        <td>DatePicker</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>TimePicker</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>[Example]</td>
        <td>SearchBox</td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Slider</td>
        <td>Slider</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>TextField</td>
        <td>Textbox</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Switch</td>
        <td>Toggle</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td><a href="https://pub.dev/packages/flutter_spinbox">SpinBox</a></td>
        <td>SpinButton</td>
        <td></td>
    </tr>
    <tr><th colspan="4">Dialogs, alerts, and panels</th></tr>
    <tr>
        <td>✓</td>
        <td>Banner</td>
        <td>Message</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>SnackBar</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr>
        <td>✓</td>
        <td>AlertDialog</td>
        <td>Dialog</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>SimpleDialog</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>BottomSheet</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>ExpansionPanel</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr><th colspan="4">App structure and navigation</th></tr>
    <tr>
        <td></td>
        <td>Appbar</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>BottomNavigationBar</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>Drawer</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>TabBar</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>✓</td>
        <td>Tabs</td>
        <td>Tabs</td>
        <td></td>
    </tr>
    <tr><th colspan="4">Grids</th></tr>
    <tr>
        <td></td>
        <td>DataTable</td>
        <td>Grid</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>Table</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr><th colspan="4">Utility controls</th></tr>
    <tr>
        <td></td>
        <td>-</td>
        <td>Html</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>-</td>
        <td>IFrame</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td>-</td>
        <td>Persona</td>
        <td></td>
    </tr>
</table>

## Clients (Flet View)

* Web - S1
* Windows - S1
* macOS - S1
* iOS
* Android

## Colors

* [Full list of Material colors](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/colors.dart)
* [Themed colors](https://api.flutter.dev/flutter/material/ColorScheme-class.html)
* [Material color roles](https://m3.material.io/styles/color/the-color-system/color-roles)

## Icons

[Full list of Material icons](https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart)

## Control

Base control class.

Properties:

- visible
- disabled

- expand (int) - The control is forced to fill the available space inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Expanded).
- flex (S2) (int) - The child can be at most as large as the available space (but is allowed to be smaller) inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Flexible with fit=FlexFit.loose).

The only difference if you use Flexible instead of Expanded, is that Flexible lets its child have the same or smaller width than the Flexible itself, while Expanded forces its child to have the exact same width of the Expanded. But both Expanded and Flexible ignore their children’s width when sizing themselves.

- width - wrap into SizedBox
- height - wrap into SizedBox
- minHeight (S2) - wrap into ConstrainedBox
- maxHeight (S2) - wrap into ConstrainedBox
- minWidth (S2) - wrap into ConstrainedBox
- maxWidth (S2) - wrap into ConstrainedBox

- fit (S2)
- fitAlign (S2) - Wrap into FittedBox

- opacity - allows to specify transparency of the control, hide it completely or blend with another if used with Stack. 0.0 - hidden, 1.0 - fully visible. See https://api.flutter.dev/flutter/widgets/Opacity-class.html.

More info:

- https://api.flutter.dev/flutter/widgets/Expanded-class.html
- https://api.flutter.dev/flutter/widgets/Flexible-class.html

## ListView

Docs:

* https://api.flutter.dev/flutter/widgets/ListView-class.html
* https://docs.flutter.dev/cookbook/lists/basic-list

Properties:

- scrollDirection - `vertical` (default), `horizontal`.
- padding
- spacing
- autoScroll - scroll to end on items update

### ListTile (S2)

Docs: https://api.flutter.dev/flutter/material/ListTile-class.html

Properties:

- contentPadding
- ...

## GridView

Docs: https://api.flutter.dev/flutter/widgets/GridView-class.html

Properties:

- scrollDirection - `vertical` (default), `horizontal`.
- padding
- runsCount
- spacing
- runSpacing

## Card

Docs: https://api.flutter.dev/flutter/widgets/Card-class.html

## Divider

Docs: https://api.flutter.dev/flutter/widgets/Divider-class.html

Properties:

- height
- thickness
- indent
- endIndent
- color

## Text

Docs: https://api.flutter.dev/flutter/material/Text-class.html

Selectable text docs: https://api.flutter.dev/flutter/material/SelectableText-class.html

TextTheme: https://api.flutter.dev/flutter/material/TextTheme-class.html

- value
- textAlign - `center`, `end`, `justify`, `left`, `right`, `start` (for RTL and LTR texts)
- size
- weight - `bold`, `normal`, `w100`, `w200`, ... [see all](https://api.flutter.dev/flutter/dart-ui/FontWeight-class.html)
- italic
- style ([more details](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/text_theme.dart))
- pre (S2) - [more info](https://stackoverflow.com/questions/64145307/full-list-of-font-families-provided-with-flutter)
- color
- bgColor
- overflow - (TextOverflow) `clip`, `ellipsis`, `fade`, `visible`
- selectable
- tooltip
- noWrap

## Icon

Docs: https://api.flutter.dev/flutter/widgets/Icon-class.html

Icons list: https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart

Properties:

- semanticLabel (S2) - Text to announce in accessibility modes

## Image

Docs: https://api.flutter.dev/flutter/widgets/Image-class.html

Properties:

- opacity (S2) - override control's opacity
- semanticLabel (S2)

## RadioGroup

Properties:

- value - selected value
- content

Events:

- change

## Radio

Docs: https://api.flutter.dev/flutter/material/Radio-class.html

Properties:

- label
- labelPosition
- value - radio's value
- tooltip
- autofocus

Events:

- focus
- blur

## Slider

Docs: https://api.flutter.dev/flutter/material/Switch-class.html

Properties:

- value
- label - use `{value}`
- min
- max
- divisions
- tooltip
- autofocus

Events:

- change
- focus
- blur

## Switch

Docs: https://api.flutter.dev/flutter/material/Switch-class.html

Properties:

- label
- labelPosition
- value
- tooltip
- autofocus

Events:

- change
- focus
- blur

## Checkbox

Docs: https://api.flutter.dev/flutter/material/Checkbox-class.html

Properties:

- value
- tristate
- label
- labelPosition
- tooltip
- autofocus

Events:

- change
- focus
- blur

## Dropdown

Docs: https://api.flutter.dev/flutter/material/DropdownButtonFormField-class.html

Properties:

- label
- icon
- border
- filled
- hintText
- helperText
- counterText
- errorText
- prefix: Control
- suffix: Control
- tooltip

- value
- options
- autofocus

Events:

- change
- focus
- blur

## TextField

Docs: https://api.flutter.dev/flutter/material/TextFormField-class.html

Properties:

- label
- icon
- border
- filled
- hintText
- helperText
- counterText
- errorText
- prefix: Control
- suffix: Control
- tooltip
- autofocus

- value
- keyboardType
- multiline
- minLines
- maxLines
- password
- canRevealPassword - true/false
- readOnly
- shiftEnter
- textAlign

Events:

- change
- focus
- blur

## AlertDialog

Docs: https://api.flutter.dev/flutter/material/AlertDialog-class.html

Properties:

- open - bool
- modal - true/false (barrierDismissible)
- title (Control)
- titlePadding
- content (Control)
- contentPadding
- actions (Controls)
- actionsPadding
- actionsAlignment (mainAxisAlignment)

Events:

- dismiss - fires when non-modal dialog is dismissed by clicking an area outside it.

## Banner

Docs: https://api.flutter.dev/flutter/material/MaterialBanner-class.html

Properties:

- open - bool
- leading (Control)
- leadingPadding
- content (Control)
- contentPadding
- actions (Controls)
- forceActionsBelow
- bgColor

## SnackBar

Docs: https://api.flutter.dev/flutter/material/SnackBar-class.html

Properties:

- open
- removeCurrentSnackBar
- content (Control)
- action - action button label
- duration (S2)
- behavior (S2)
- bgColor (S2)
- margin (S2)
- padding (S2)
- width (S2)

Events:

- action - when action button clicked

## Tabs

Properties:

- tabs
- value
- animationDuration - in milliseconds

Events:

- change

### Tab

- key
- text
- tabContent
- content
- icon

## SplitView

Docs: https://pub.dev/packages/split_view
