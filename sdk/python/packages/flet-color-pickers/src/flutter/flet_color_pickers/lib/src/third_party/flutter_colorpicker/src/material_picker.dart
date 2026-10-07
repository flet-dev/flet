/// Material Color Picker

library material_colorpicker;

import 'package:flutter/gestures.dart';
import 'package:material_ui/material_ui.dart';
import 'utils.dart';

// The Color Picker which contains Material Design Color Palette.
class MaterialPicker extends StatefulWidget {
  const MaterialPicker({
    Key? key,
    required this.pickerColor,
    required this.onColorChanged,
    this.onPrimaryChanged,
    this.enableLabel = false,
    this.portraitOnly = false,
  }) : super(key: key);

  final Color pickerColor;
  final ValueChanged<Color> onColorChanged;
  final ValueChanged<Color>? onPrimaryChanged;
  final bool enableLabel;
  final bool portraitOnly;

  @override
  State<StatefulWidget> createState() => _MaterialPickerState();
}

class _MaterialPickerState extends State<MaterialPicker> {
  final List<List<Color>> _colorTypes = [
    [Colors.red, Colors.redAccent],
    [Colors.pink, Colors.pinkAccent],
    [Colors.purple, Colors.purpleAccent],
    [Colors.deepPurple, Colors.deepPurpleAccent],
    [Colors.indigo, Colors.indigoAccent],
    [Colors.blue, Colors.blueAccent],
    [Colors.lightBlue, Colors.lightBlueAccent],
    [Colors.cyan, Colors.cyanAccent],
    [Colors.teal, Colors.tealAccent],
    [Colors.green, Colors.greenAccent],
    [Colors.lightGreen, Colors.lightGreenAccent],
    [Colors.lime, Colors.limeAccent],
    [Colors.yellow, Colors.yellowAccent],
    [Colors.amber, Colors.amberAccent],
    [Colors.orange, Colors.orangeAccent],
    [Colors.deepOrange, Colors.deepOrangeAccent],
    [Colors.brown],
    [Colors.grey],
    [Colors.blueGrey],
    [Colors.black],
  ];

  List<Color> _currentColorType = [Colors.red, Colors.redAccent];
  Color _currentShading = Colors.transparent;

  List<Map<Color, String>> _shadingTypes(List<Color> colors) {
    List<Map<Color, String>> result = [];

    for (Color colorType in colors) {
      if (colorType == Colors.grey) {
        result.addAll([50, 100, 200, 300, 350, 400, 500, 600, 700, 800, 850, 900]
            .map((int shade) => {Colors.grey[shade]!: shade.toString()})
            .toList());
      } else if (colorType == Colors.black || colorType == Colors.white) {
        result.addAll([
          {Colors.black: ''},
          {Colors.white: ''}
        ]);
      } else if (colorType is MaterialAccentColor) {
        result.addAll([100, 200, 400, 700].map((int shade) => {colorType[shade]!: 'A$shade'}).toList());
      } else if (colorType is MaterialColor) {
        result.addAll([50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
            .map((int shade) => {colorType[shade]!: shade.toString()})
            .toList());
      } else {
        result.add({const Color(0x00000000): ''});
      }
    }

    return result;
  }

  @override
  void initState() {
    for (List<Color> _colors in _colorTypes) {
      _shadingTypes(_colors).forEach((Map<Color, String> color) {
        if (widget.pickerColor.value == color.keys.first.value) {
          return setState(() {
            _currentColorType = _colors;
            _currentShading = color.keys.first;
          });
        }
      });
    }
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    bool _isPortrait = MediaQuery.of(context).orientation == Orientation.portrait || widget.portraitOnly;

    Widget _colorList() {
      return Container(
        clipBehavior: Clip.hardEdge,
        decoration: const BoxDecoration(),
        child: Container(
          margin: _isPortrait ? const EdgeInsets.only(right: 10) : const EdgeInsets.only(bottom: 10),
          width: _isPortrait ? 60 : null,
          height: _isPortrait ? null : 60,
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            boxShadow: [BoxShadow(color: (Theme.of(context).brightness == Brightness.light) ? (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38 : Colors.black38, blurRadius: 10)],
            border: _isPortrait
                ? Border(right: BorderSide(color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38, width: 1))
                : Border(top: BorderSide(color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38, width: 1)),
          ),
          child: ScrollConfiguration(
            behavior: ScrollConfiguration.of(context).copyWith(dragDevices: PointerDeviceKind.values.toSet()),
            child: ListView(
              scrollDirection: _isPortrait ? Axis.vertical : Axis.horizontal,
              children: [
                _isPortrait
                    ? const Padding(padding: EdgeInsets.only(top: 7))
                    : const Padding(padding: EdgeInsets.only(left: 7)),
                ..._colorTypes.map((List<Color> _colors) {
                  Color _colorType = _colors[0];
                  return GestureDetector(
                    onTap: () {
                      if (widget.onPrimaryChanged != null) widget.onPrimaryChanged!(_colorType);
                      setState(() => _currentColorType = _colors);
                    },
                    child: Container(
                      color: const Color(0x00000000),
                      padding:
                      _isPortrait ? const EdgeInsets.fromLTRB(0, 7, 0, 7) : const EdgeInsets.fromLTRB(7, 0, 7, 0),
                      child: Align(
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          width: 25,
                          height: 25,
                          decoration: BoxDecoration(
                            color: _colorType,
                            shape: BoxShape.circle,
                            boxShadow: _currentColorType == _colors
                                ? [
                              _colorType == Theme.of(context).cardColor
                                  ? BoxShadow(
                                color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38,
                                blurRadius: 10,
                              )
                                  : BoxShadow(
                                color: _colorType,
                                blurRadius: 10,
                              ),
                            ]
                                : null,
                            border: _colorType == Theme.of(context).cardColor
                                ? Border.all(color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38, width: 1)
                                : null,
                          ),
                        ),
                      ),
                    ),
                  );
                }),
                _isPortrait
                    ? const Padding(padding: EdgeInsets.only(top: 5))
                    : const Padding(padding: EdgeInsets.only(left: 5)),
              ],
            ),
          ),
        ),
      );
    }

    Widget _shadingList() {
      return ScrollConfiguration(
        behavior: ScrollConfiguration.of(context).copyWith(dragDevices: PointerDeviceKind.values.toSet()),
        child: ListView(
          scrollDirection: _isPortrait ? Axis.vertical : Axis.horizontal,
          children: [
            _isPortrait
                ? const Padding(padding: EdgeInsets.only(top: 15))
                : const Padding(padding: EdgeInsets.only(left: 15)),
            ..._shadingTypes(_currentColorType).map((Map<Color, String> color) {
              final Color _color = color.keys.first;
              return GestureDetector(
                onTap: () {
                  setState(() => _currentShading = _color);
                  widget.onColorChanged(_color);
                },
                child: Container(
                  color: const Color(0x00000000),
                  margin: _isPortrait ? const EdgeInsets.only(right: 10) : const EdgeInsets.only(bottom: 10),
                  padding: _isPortrait ? const EdgeInsets.fromLTRB(0, 7, 0, 7) : const EdgeInsets.fromLTRB(7, 0, 7, 0),
                  child: Align(
                    child: AnimatedContainer(
                      curve: Curves.fastOutSlowIn,
                      duration: const Duration(milliseconds: 500),
                      width:
                      _isPortrait ? (_currentShading == _color ? 250 : 230) : (_currentShading == _color ? 50 : 30),
                      height: _isPortrait ? 50 : 220,
                      decoration: BoxDecoration(
                        color: _color,
                        boxShadow: _currentShading == _color
                            ? [
                          (_color == Colors.white) || (_color == Colors.black)
                              ? BoxShadow(
                            color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38,
                            blurRadius: 10,
                          )
                              : BoxShadow(
                            color: _color,
                            blurRadius: 10,
                          ),
                        ]
                            : null,
                        border: (_color == Colors.white) || (_color == Colors.black)
                            ? Border.all(color: (Theme.of(context).brightness == Brightness.light) ? Colors.grey[300]! : Colors.black38, width: 1)
                            : null,
                      ),
                      child: widget.enableLabel
                          ? _isPortrait
                          ? Row(
                        children: [
                          Text(
                            '  ${color.values.first}',
                            style: TextStyle(color: useWhiteForeground(_color) ? Colors.white : Colors.black),
                          ),
                          Expanded(
                            child: Align(
                              alignment: Alignment.centerRight,
                              child: Text(
                                '#${(_color.toString().replaceFirst('Color(0xff', '').replaceFirst(')', '')).toUpperCase()}  ',
                                style: TextStyle(
                                  color: useWhiteForeground(_color) ? Colors.white : Colors.black,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                        ],
                      )
                          : AnimatedOpacity(
                        duration: const Duration(milliseconds: 300),
                        opacity: _currentShading == _color ? 1 : 0,
                        child: Container(
                          padding: const EdgeInsets.only(top: 16),
                          alignment: Alignment.topCenter,
                          child: Text(
                            color.values.first,
                            style: TextStyle(
                              color: useWhiteForeground(_color) ? Colors.white : Colors.black,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                            softWrap: false,
                          ),
                        ),
                      )
                          : const SizedBox(),
                    ),
                  ),
                ),
              );
            }),
            _isPortrait
                ? const Padding(padding: EdgeInsets.only(top: 15))
                : const Padding(padding: EdgeInsets.only(left: 15)),
          ],
        ),
      );
    }

    if (_isPortrait) {
      return SizedBox(
        width: 350,
        height: 500,
        child: Row(
          children: <Widget>[
            _colorList(),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                child: _shadingList(),
              ),
            ),
          ],
        ),
      );
    } else {
      return SizedBox(
        width: 500,
        height: 300,
        child: Column(
          children: <Widget>[
            _colorList(),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: _shadingList(),
              ),
            ),
          ],
        ),
      );
    }
  }
}
