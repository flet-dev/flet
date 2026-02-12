import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

class MultipleChoiceBlockPickerControl extends StatefulWidget {
  final Control control;

  const MultipleChoiceBlockPickerControl({super.key, required this.control});

  @override
  State<MultipleChoiceBlockPickerControl> createState() =>
      _MultipleChoiceBlockPickerControlState();
}

class _MultipleChoiceBlockPickerControlState
    extends State<MultipleChoiceBlockPickerControl> {
  List<Color> _pickerColors = [Colors.black];

  void _onColorsChanged(List<Color> colors) {
    setState(() {
      _pickerColors = colors;
    });
    final colorsHex = colors.map((color) => color.toHex()).toList();
    widget.control.updateProperties({"colors": colorsHex}, notify: true);
    widget.control.triggerEvent("colors_change", colorsHex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("MultipleChoiceBlockPickerControl build: ${widget.control.id}");

    final rawColors = widget.control.get("colors");
    final theme = Theme.of(context);
    final parsedColors = <Color>[];
    if (rawColors is List) {
      for (final raw in rawColors) {
        final parsed = parseColor(raw?.toString(), theme);
        if (parsed != null) {
          parsedColors.add(parsed);
        }
      }
    }
    if (parsedColors.isNotEmpty) {
      _pickerColors = parsedColors;
    } else if (_pickerColors.isEmpty) {
      _pickerColors = [Colors.black];
    }

    final rawAvailableColors = widget.control.get("available_colors");
    final availableColors = <Color>[];
    if (rawAvailableColors is List) {
      for (final raw in rawAvailableColors) {
        final parsed = parseColor(raw?.toString(), theme);
        if (parsed != null) {
          availableColors.add(parsed);
        }
      }
    }

    final picker = availableColors.isNotEmpty
        ? MultipleChoiceBlockPicker(
            pickerColors: _pickerColors,
            onColorsChanged: _onColorsChanged,
            availableColors: availableColors,
          )
        : MultipleChoiceBlockPicker(
            pickerColors: _pickerColors,
            onColorsChanged: _onColorsChanged,
          );

    return LayoutControl(control: widget.control, child: picker);
  }
}
