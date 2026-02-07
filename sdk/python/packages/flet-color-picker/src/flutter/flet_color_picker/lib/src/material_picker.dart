import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

class MaterialPickerControl extends StatefulWidget {
  final Control control;

  const MaterialPickerControl({super.key, required this.control});

  @override
  State<MaterialPickerControl> createState() => _MaterialPickerControlState();
}

class _MaterialPickerControlState extends State<MaterialPickerControl> {
  Color _pickerColor = Colors.black;

  void _onColorChanged(Color color) {
    setState(() {
      _pickerColor = color;
    });
    final colorHex = color.toHex();
    widget.control.updateProperties({"picker_color": colorHex}, notify: true);
    widget.control.triggerEvent("color_change", colorHex);
  }

  void _onPrimaryChanged(Color color) {
    final colorHex = color.toHex();
    widget.control.triggerEvent("primary_change", colorHex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("MaterialPickerControl build: ${widget.control.id}");

    final controlColor =
        widget.control.getColor("picker_color", context) ?? Colors.black;
    if (controlColor.value != _pickerColor.value) {
      _pickerColor = controlColor;
    }

    final picker = MaterialPicker(
      pickerColor: _pickerColor,
      onColorChanged: _onColorChanged,
      onPrimaryChanged: _onPrimaryChanged,
      enableLabel: widget.control.getBool("enable_label", false)!,
      portraitOnly: widget.control.getBool("portrait_only", false)!,
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
