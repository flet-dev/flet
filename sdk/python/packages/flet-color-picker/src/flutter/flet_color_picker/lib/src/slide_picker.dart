import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

class SlidePickerControl extends StatefulWidget {
  final Control control;

  const SlidePickerControl({super.key, required this.control});

  @override
  State<SlidePickerControl> createState() => _SlidePickerControlState();
}

class _SlidePickerControlState extends State<SlidePickerControl> {
  Color _pickerColor = Colors.black;

  void _onColorChanged(Color color) {
    setState(() {
      _pickerColor = color;
    });
    final colorHex = color.toHex();
    widget.control.updateProperties({"picker_color": colorHex}, notify: true);
    widget.control.triggerEvent("color_change", colorHex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SlidePickerControl build: ${widget.control.id}");

    final controlColor =
        widget.control.getColor("picker_color", context) ?? Colors.black;
    if (controlColor.value != _pickerColor.value) {
      _pickerColor = controlColor;
    }

    final picker = SlidePicker(
      pickerColor: _pickerColor,
      onColorChanged: _onColorChanged,
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
