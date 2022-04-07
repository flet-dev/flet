# Flet Roadmap

## Sprint 1

* Controls
  * Layout
    * [ ] Container
    * Row (flex - default mode, wrap)
    * Column (flex - default mode, wrap)
    * Stack
    * ListView
    * GridView
  * Base controls
    * Text
    * Icon
    * Image (+custom assets directory for Flet server [see here](https://docs.flutter.dev/development/platform-integration/web-images)).
    * ProgressBar
    * ProgressRing
  * Buttons
    * ElevatedButton
    * OutlinedButton
    * TextButton
    * IconButton
  * Forms
    * TextField
    * Checkbox
    * Radio
    * Dropdown
    * Slider
    * Switch
  * Dialogs, alerts and panels
    * Banner
    * SnackBar
    * AlertDialog

* Python Guide
  * Deployment (+how to change favicon.ico)
    * Deployment to Replit
    * Deployment to Fly.io

## Sprint 2

* Controls
  * Layout
    * Row (responsive)
    * Column (responsive)


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
    <tr><th colspan="4">Base controls</th></tr>
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
    <tr><th colspan="4">Forms</th></tr>
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

[Full list of Material colors](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/colors.dart)

## Icons

[Full list of Material icons](https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart)

## Page

Properties:

- title
- design (S2) - `material` (default), `cupertino`, `fluent`, `macos`.
- themeMode - `system` (default), `light`, `dark` ([more info](https://stackoverflow.com/questions/60232070/how-to-implement-dark-mode-in-flutter))
- horizontalAlignment - `start` (default), `center`, `end`, `stretch`
- verticalAlignment - `start`, `end`, `center`, `spaceBetween`, `spaceAround`, `spaceEvenly`.
- spacing - gap between adjacent items, default
- color - background color
- windowWidth - current window width
- windowHeight - current window height

## Control

Base control class.

Properties:

- id
- visible
- disabled

- Expanded (int) - The control is forced to fill the available space inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Expanded).
- Flexible (int) - The child can be at most as large as the available space (but is allowed to be smaller) inside Row or Column. Flex factor specified by the property. Default is 1. The property has affect only for direct descendants of Row and Column controls. (Wrap control into Flexible with fit=FlexFit.loose).

The only difference if you use Flexible instead of Expanded, is that Flexible lets its child have the same or smaller width than the Flexible itself, while Expanded forces its child to have the exact same width of the Expanded. But both Expanded and Flexible ignore their children’s width when sizing themselves.

- width - wrap into SizedBox
- height - wrap into SizedBox
- minHeight - wrap into ConstrainedBox
- maxHeight - wrap into ConstrainedBox
- minWidth - wrap into ConstrainedBox
- maxWidth - wrap into ConstrainedBox

- fit
- fitAlign - Wrap into FittedBox

- opacity - allows to specify transparency of the control, hide it completely or blend with another if used with Stack. 0.0 - hidden, 1.0 - fully visible. See https://api.flutter.dev/flutter/widgets/Opacity-class.html.

- marging
- padding

More info:

- https://api.flutter.dev/flutter/widgets/Expanded-class.html
- https://api.flutter.dev/flutter/widgets/Flexible-class.html

## Container

Docs: https://api.flutter.dev/flutter/widgets/Container-class.html

- color (background color - `decoration: BoxDecoration.color`)
- alignment - `topLeft`, `topCenter`, `topRight`, `centerLeft`, `center`, `centerRight`, `bottomLeft`, `bottomCenter`, `bottomRight`
- borderColor
- borderWidth
- borderStyle - `solid`, `node`
- borderRadius
- verticalScroll
- horizontalScroll
- autoScroll - `end`, `start` ([example](https://stackoverflow.com/questions/43485529/programmatically-scrolling-to-the-end-of-a-listview)).

## Row

Docs: https://api.flutter.dev/flutter/widgets/Row-class.html

- spacing - gap between adjacent items (SizedBox)
- wrap - switch to "Wrap" control
- runSpacing - gap between runs

## Column

Docs: https://api.flutter.dev/flutter/widgets/Column-class.html

- spacing - gap between adjacent items (SizedBox)
- wrap - switch to "Wrap" control
- runSpacing - gap between runs

## Stack

Docs: https://api.flutter.dev/flutter/widgets/Stack-class.html

## ListView

Docs: https://api.flutter.dev/flutter/widgets/ListView-class.html

## GridView

Docs: https://api.flutter.dev/flutter/widgets/GridView-class.html

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

## SplitView

Docs: https://pub.dev/packages/split_view

## Text

Docs: https://api.flutter.dev/flutter/material/Text-class.html

Selectable text docs: https://api.flutter.dev/flutter/material/SelectableText-class.html

TextTheme: https://api.flutter.dev/flutter/material/TextTheme-class.html

- value
- textAlign - `center`, `end`, `justify`, `left`, `right`, `start` (for RTL and LTR texts)
- size
- bold (weight=w700)
- weight
- italic
- themeStyle ([more details](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/text_theme.dart))
- pre (P2) - [more info](https://stackoverflow.com/questions/64145307/full-list-of-font-families-provided-with-flutter)
- color
- bgColor
- overflow - (TextOverflow) `clip`, `ellipsis`, `fade`, `visible`
- selectable


## Icon

Docs: https://api.flutter.dev/flutter/widgets/Icon-class.html

Icons list: https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart

Properties:

- Name ([The list of icons](https://api.flutter.dev/flutter/material/Icons-class.html))
- Color ([more](https://api.flutter.dev/flutter/dart-ui/Color-class.html))
- Size

## Image

Docs: https://api.flutter.dev/flutter/widgets/Image-class.html

Properties:

- Width
- Height
- Src
- SemanticLabel (Alt)
- Repeat: noRepeat, repeat, repeatX, repeatY
- Opacity
- Fit: contain, cover, fill, fitHeight, fitWidth, none, scaleDown
- Border? (inside Container)

## TextField

Docs: https://api.flutter.dev/flutter/material/TextField-class.html

Example: https://gallery.flutter.dev/#/demo/text-field
