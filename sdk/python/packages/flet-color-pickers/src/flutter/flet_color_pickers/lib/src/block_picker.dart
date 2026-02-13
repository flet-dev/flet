import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

class BlockPickerControl extends StatefulWidget {
  final Control control;

  const BlockPickerControl({super.key, required this.control});

  @override
  State<BlockPickerControl> createState() => _BlockPickerControlState();
}

class _BlockPickerControlState extends State<BlockPickerControl> {
  Color _pickerColor = Colors.black;

  void _onColorChanged(Color color) {
    setState(() {
      _pickerColor = color;
    });
    final colorHex = color.toHex();
    widget.control.updateProperties({"color": colorHex}, notify: true);
    widget.control.triggerEvent("color_change", colorHex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("BlockPickerControl build: ${widget.control.id}");

    final controlColor =
        widget.control.getColor("color", context) ?? Colors.black;
    if (controlColor.value != _pickerColor.value) {
      _pickerColor = controlColor;
    }

    final rawColors = widget.control.get("available_colors");
    final theme = Theme.of(context);
    final availableColors = <Color>[];
    if (rawColors is List) {
      for (final raw in rawColors) {
        final parsed = parseColor(raw?.toString(), theme);
        if (parsed != null) {
          availableColors.add(parsed);
        }
      }
    }
    final picker = availableColors.isNotEmpty
        ? BlockPicker(
            pickerColor: _pickerColor,
            onColorChanged: _onColorChanged,
            availableColors: availableColors,
          )
        : BlockPicker(
            pickerColor: _pickerColor,
            onColorChanged: _onColorChanged,
          );

    return LayoutControl(control: widget.control, child: picker);
  }
}
