# Controls

<table>
    <tr>
        <th>Flet</td>
        <th>Pglet</td>
    </tr>
    <tr><th colspan="2">Layout</th></tr>
    <tr>
        <td>Container</td>
        <td>Stack</td>
    </tr>
    <tr>
        <td>Row</td>
        <td>Stack horizontal=True</td>
    </tr>
    <tr>
        <td>Column</td>
        <td>Stack horizontal=False</td>
    </tr>
    <tr>
        <td>Spacer</td>
        <td>-</td>
    </tr>    
    <tr>
        <td>Expanded</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Stack</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Wrap</td>
        <td>Stack wrap=True</td>
    </tr>
    <tr>
        <td>ListView</td>
        <td>Stack horizontal=False</td>
    </tr>
    <tr>
        <td>Divider</td>
        <td>-</td>
    </tr>    
    <tr>
        <td>GridView</td>
        <td>-</td>
    </tr>
    <tr>
        <td>SplitView</td>
        <td>SplitStack</td>
    </tr>
    <tr>
        <td>Card</td>
        <td>-</td>
    </tr>
    <tr>
        <td>ExpansionPanel</td>
        <td>-</td>
    </tr>
    <tr><th colspan="2">Base controls</th></tr>
    <tr>
        <td>Text</td>
        <td>Text</td>
    </tr>
    <tr>
        <td>Icon</td>
        <td>Icon</td>
    </tr>
    <tr>
        <td>Image</td>
        <td>Image</td>
    </tr>
    <tr>
        <td><a href="https://stackoverflow.com/questions/43583411/how-to-create-a-hyperlink-in-flutter-widget">To-Do</a></td>
        <td>Link</td>
    </tr>
    <tr>
        <td>ProgressBar</td>
        <td>Progress</td>
    </tr>
    <tr>
        <td>ProgressRing</td>
        <td>Spinner</td>
    </tr>
    <tr><th colspan="2">Buttons</th></tr>
    <tr>
        <td>ElevatedButton</td>
        <td>Button primary=True</td>
    </tr>
    <tr>
        <td>OutlinedButton</td>
        <td>Button primary=False</td>
    </tr>
    <tr>
        <td>TextButton</td>
        <td>Button action=True</td>
    </tr>
    <tr>
        <td>IconButton</td>
        <td>Button icon={icon_name}</td>
    </tr>
    <tr>
        <td>PopupMenuButton</td>
        <td>Button with MenuItems</td>
    </tr>    
    <tr>
        <td>Any Button with a custom "child"</td>
        <td>Button compound=True</td>
    </tr>
    <tr><th colspan="2">Forms</th></tr>
    <tr>
        <td>Checkbox</td>
        <td>Checkbox</td>
    </tr>
    <tr>
        <td>Radio</td>
        <td>ChoiceGroup</td>
    </tr>
    <tr>
        <td>Dropdown</td>
        <td>Dropdown</td>
    </tr>
    <tr>
        <td>-</td>
        <td>ComboBox</td>
    </tr>
    <tr>
        <td>DatePicker</td>
        <td>DatePicker</td>
    </tr>
    <tr>
        <td>TimePicker</td>
        <td>-</td>
    </tr>
    <tr>
        <td>-</td>
        <td>SearchBox</td>
    </tr>
    <tr>
        <td>Slider</td>
        <td>Slider</td>
    </tr>
    <tr>
        <td><a href="https://pub.dev/packages/flutter_spinbox">SpinBox</a></td>
        <td>SpinButton</td>
    </tr>
    <tr>
        <td>TextField</td>
        <td>Textbox</td>
    </tr>
    <tr>
        <td>Switch</td>
        <td>Toggle</td>
    </tr>
    <tr><th colspan="2">Utility controls</th></tr>
    <tr>
        <td>-</td>
        <td>Html</td>
    </tr>
    <tr>
        <td>-</td>
        <td>IFrame</td>
    </tr>
    <tr>
        <td>-</td>
        <td>Persona</td>
    </tr>
</table>

## Container

Docs: https://api.flutter.dev/flutter/widgets/Container-class.html

* Padding
* Color (background color)
* Alignment
* Border

## Row

Docs: https://api.flutter.dev/flutter/widgets/Row-class.html

## Column

Docs: https://api.flutter.dev/flutter/widgets/Column-class.html

## Expanded

Docs: https://api.flutter.dev/flutter/widgets/Expanded-class.html

## Stack

Docs: https://api.flutter.dev/flutter/widgets/Stack-class.html

## Wrap

Docs: https://api.flutter.dev/flutter/widgets/Wrap-class.html

## ListView

Docs: https://api.flutter.dev/flutter/widgets/ListView-class.html

## GridView

Docs: https://api.flutter.dev/flutter/widgets/GridView-class.html

## Card

Docs: https://api.flutter.dev/flutter/widgets/Card-class.html

## Spacer

Docs: https://api.flutter.dev/flutter/widgets/Spacer-class.html

## Divider

Docs: https://api.flutter.dev/flutter/widgets/Divider-class.html

## SplitView

Docs: https://pub.dev/packages/split_view

## Text

Docs: https://api.flutter.dev/flutter/material/Text-class.html

Selectable text docs: https://api.flutter.dev/flutter/material/SelectableText-class.html

* Value
* Border? (inside Container)

## Icon

Docs: https://api.flutter.dev/flutter/widgets/Icon-class.html

Properties:

* Name ([The list of icons](https://api.flutter.dev/flutter/material/Icons-class.html))
* Color ([more](https://api.flutter.dev/flutter/dart-ui/Color-class.html))
* Size

## Image

Docs: https://api.flutter.dev/flutter/widgets/Image-class.html

Properties:

* Width
* Height
* Src
* SemanticLabel (Alt)
* Repeat: noRepeat, repeat, repeatX, repeatY
* Opacity
* Fit: contain, cover, fill, fitHeight, fitWidth, none, scaleDown
* Border? (inside Container)

## TextField

Docs: https://api.flutter.dev/flutter/material/TextField-class.html

Example: https://gallery.flutter.dev/#/demo/text-field