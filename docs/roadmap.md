# Flet Roadmap

## Sprint 1

* Controls
  * Common
    * [ ] Control
    * [ ] Page
  * Layout
    * [ ] Container
    * [ ] Row (flex - default mode, wrap)
    * [ ] Column (flex - default mode, wrap)
    * [ ] Stack
    * [ ] ListView
    * [ ] GridView
  * Basic controls
    * [ ] Text
    * [ ] Icon
    * [ ] Image (+custom assets directory for Flet server [see here](https://docs.flutter.dev/development/platform-integration/web-images)).
    * [ ] ProgressBar
    * [ ] ProgressRing
  * Buttons
    * [ ] ElevatedButton
    * [ ] OutlinedButton
    * [ ] TextButton
    * [ ] IconButton
  * Input and selections
    * [ ] TextField
    * [ ] Checkbox
    * [ ] Radio
    * [ ] Dropdown
    * [ ] Slider
    * [ ] Switch
  * Dialogs, alerts and panels
    * [ ] Banner
    * [ ] SnackBar
    * [ ] AlertDialog

* Flet Client
  * [ ] Web
  * [ ] Windows ("client" mode - started from Python)
  * [ ] macOS ("client" mode - started from Python)

* Flet Daemon
  * [ ] "assets" directory with static content

* Website
  * [ ] Controls S1 reference
  * [ ] Introduction
  * [ ] Blog post
  * [ ] Python Guide
    * Deployment (+how to change favicon.ico)
      * Deployment to Replit
      * Deployment to Fly.io

## Sprint 2

* Controls
  * Layout
    * Row (responsive)
    * Column (responsive)
  * Behavior
    * Complex embeddable values for `padding`, `marging`, etc, e.g. `.padding = { 'left': 10, 'right': 20 }`
    * Visual Density ([more](https://api.flutter.dev/flutter/material/VisualDensity-class.html))

* Flet Client
  * [ ] Windows ("host" mode with hot reload)
  * [ ] macOS ("host" mode with hot reload)

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
        <td></td>
        <td>Container</td>
        <td>Stack</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Row</td>
        <td>Stack horizontal=True</td>
        <td>S1 (flex, wrap)</td>
    </tr>
    <tr>
        <td></td>
        <td>Column</td>
        <td>Stack horizontal=False</td>
        <td>S1 (flex, wrap)</td>
    </tr>
    <tr>
        <td></td>
        <td>Stack</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
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
        <td></td>
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
        <td></td>
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
        <td></td>
        <td>Icon</td>
        <td>Icon</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Image</td>
        <td>Image</td>
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
        <td></td>
        <td>ProgressBar</td>
        <td>Progress</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>ProgressRing</td>
        <td>Spinner</td>
        <td>S1</td>
    </tr>
    <tr><th colspan="4">Buttons</th></tr>
    <tr>
        <td></td>
        <td>ElevatedButton</td>
        <td>Button primary=True</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>OutlinedButton</td>
        <td>Button primary=False</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>TextButton</td>
        <td>Button action=True</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
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
        <td></td>
        <td>FloatingActionButton</td>
        <td>-</td>
        <td></td>
    </tr>
    <tr><th colspan="4">Input and selections</th></tr>
    <tr>
        <td></td>
        <td>Checkbox</td>
        <td>Checkbox</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Radio</td>
        <td>ChoiceGroup</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>Dropdown</td>
        <td>Dropdown</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
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
        <td></td>
        <td>Slider</td>
        <td>Slider</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>TextField</td>
        <td>Textbox</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
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
        <td></td>
        <td>Banner</td>
        <td>Message</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
        <td>SnackBar</td>
        <td>-</td>
        <td>S1</td>
    </tr>
    <tr>
        <td></td>
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

## Icons

[Full list of Material icons](https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart)

## Page

Properties:

- title
- design (S2) - `material` (default), `cupertino`, `fluent`, `macos`.
- themeMode - `system` (default), `light`, `dark` ([more info](https://stackoverflow.com/questions/60232070/how-to-implement-dark-mode-in-flutter))
- verticalAlignment - `start`, `end`, `center`, `spaceBetween`, `spaceAround`, `spaceEvenly`.
- horizontalAlignment - `start` (default), `center`, `end`, `stretch`
- spacing - gap between adjacent items, default
- padding
- bgColor - background color
- windowWidth - current window width
- windowHeight - current window height

Events:

- onClose
- onConnect
- onDisconnect
- onResize

## Control

Base control class.

Properties:

- id
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

- marging
- padding

More info:

- https://api.flutter.dev/flutter/widgets/Expanded-class.html
- https://api.flutter.dev/flutter/widgets/Flexible-class.html

## Container

Docs: https://api.flutter.dev/flutter/widgets/Container-class.html

Properties:

- bgColor (background color - `decoration: BoxDecoration.color`)
- alignment - `topLeft`, `topCenter`, `topRight`, `centerLeft`, `center`, `centerRight`, `bottomLeft`, `bottomCenter`, `bottomRight`
- borderColor
- borderWidth
- borderStyle - `solid`, `none`
- borderRadius
- verticalScroll (S2)
- horizontalScroll (S2)
- autoScroll (S2) - `end`, `start` ([example](https://stackoverflow.com/questions/43485529/programmatically-scrolling-to-the-end-of-a-listview)).
- content - child control of any type

## Row

Docs: https://api.flutter.dev/flutter/widgets/Row-class.html

Properties:

- horizontalAlignment - `start`, `end`, `center`, `spaceBetween`, `spaceAround`, `spaceEvenly`.
- verticalAlignment - `start` (default), `center`, `end`, `stretch`, `baseline`
- spacing - gap between adjacent items (SizedBox)
- wrap - switch to "Wrap" control
- runSpacing - gap between runs
- controls - child controls of any type

## Column

Docs: https://api.flutter.dev/flutter/widgets/Column-class.html

Properties:

- verticalAlignment - `start`, `end`, `center`, `spaceBetween`, `spaceAround`, `spaceEvenly`.
- horizontalAlignment - `start` (default), `center`, `end`, `stretch`
- spacing - gap between adjacent items (SizedBox)
- wrap - switch to "Wrap" control
- runSpacing - gap between runs
- controls - child controls of any type

## Stack

Docs: https://api.flutter.dev/flutter/widgets/Stack-class.html

Properties:

- controls - child controls of any type

## ListView

Docs:

* https://api.flutter.dev/flutter/widgets/ListView-class.html
* https://docs.flutter.dev/cookbook/lists/basic-list

Properties:

- scrollDirection - `vertical` (default), `horizontal`.
- padding

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
- crossAxisCount
- mainAxisSpacing
- crossAxisSpacing

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
- themeStyle ([more details](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/text_theme.dart))
- pre (S2) - [more info](https://stackoverflow.com/questions/64145307/full-list-of-font-families-provided-with-flutter)
- color
- bgColor
- overflow - (TextOverflow) `clip`, `ellipsis`, `fade`, `visible`
- selectable


## Icon

Docs: https://api.flutter.dev/flutter/widgets/Icon-class.html

Icons list: https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart

Properties:

- name ([The list of icons](https://api.flutter.dev/flutter/material/Icons-class.html))
- color ([more](https://api.flutter.dev/flutter/dart-ui/Color-class.html))
- size
- semanticLabel (S2) - Text to announce in accessibility modes

## Image

Docs: https://api.flutter.dev/flutter/widgets/Image-class.html

Properties:

- width - override control's width
- height - override control's height
- src
- repeat: noRepeat, repeat, repeatX, repeatY
- opacity - override control's opacity
- fit: contain, cover, fill, fitHeight, fitWidth, none, scaleDown
- semanticLabel (S2)

## ProgressBar

Docs: https://api.flutter.dev/flutter/material/LinearProgressIndicator-class.html

Properties:

- color
- bgColor
- barHeight
- value
- label
- description

## ProgressRing

Docs: https://api.flutter.dev/flutter/material/CircularProgressIndicator-class.html

Properties:

- color
- bgColor
- strokeWidth
- value
- label
- labelPosition

## TextField

Docs: https://api.flutter.dev/flutter/material/TextField-class.html

Example: https://gallery.flutter.dev/#/demo/text-field

## ElevatedButton

Docs: https://api.flutter.dev/flutter/material/ElevatedButton-class.html

Properties:

- text
- icon
- iconColor
- content - a Control representing custom button content

Events:

- click

## OutlinedButton

Docs: https://api.flutter.dev/flutter/material/OutlinedButton-class.html

Properties:

- text
- icon
- iconColor
- content - a Control representing custom button content

Events:

- click

## TextButton

Docs: https://api.flutter.dev/flutter/material/TextButton-class.html

Properties:

- text
- icon
- iconColor
- content - a Control representing custom button content

Events:

- click

## IconButton

Docs: https://api.flutter.dev/flutter/material/IconButton-class.html

Properties:

- tooltip
- icon
- iconColor
- iconSize
- content - a Control representing custom button content

Events:

- click

## Radio

Docs: https://api.flutter.dev/flutter/material/Radio-class.html

Properties:

- label
- labelPosition
- value

Events:

- change

## Slider

Docs: https://api.flutter.dev/flutter/material/Switch-class.html

Properties:

- value
- min
- max
- divisions

Events:

- change

## Switch

Docs: https://api.flutter.dev/flutter/material/Switch-class.html

Properties:

- label
- labelPosition
- value

Events:

- change

## Checkbox

Docs: https://api.flutter.dev/flutter/material/Checkbox-class.html

Properties:

- label
- labelPosition
- value

Events:

- change

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
- prefixIcon
- prefixText
- suffixIcon
- suffixText

- value
- options

Events:

- change

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
- prefixIcon
- prefixText
- suffixIcon
- suffixText

- value
- keyboardType
- minLines
- maxLines
- password
- readOnly
- textAlign

Events:

- change

## AlertDialog

Docs: https://api.flutter.dev/flutter/material/AlertDialog-class.html

Properties:

- open - bool
- title (Control)
- titlePadding
- content (Control)
- contentPadding
- actions (Controls)
- actionsPadding
- actionsAlignment (mainAxisAlignment)

## Banner

Docs: https://api.flutter.dev/flutter/material/MaterialBanner-class.html

Properties:

- open - bool
- padding
- leading (Control)
- leadingPadding
- content (Control)
- actions (Controls)
- forceActionsBelow
- backgroundColor

## SnackBar

Docs: https://api.flutter.dev/flutter/material/MaterialBanner-class.html

Properties:

- open
- content (Control)
- action (SnackBarAction)
- bgColor (S2)
- margin (S2)
- padding (S2)

## SplitView

Docs: https://pub.dev/packages/split_view