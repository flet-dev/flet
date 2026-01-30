import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

class HueRingPickerControl extends StatefulWidget {
  final Control control;

  const HueRingPickerControl({super.key, required this.control});

  @override
  State<HueRingPickerControl> createState() => _HueRingPickerControlState();
}

class _HueRingPickerControlState extends State<HueRingPickerControl> {
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
    debugPrint("HueRingPickerControl build: ${widget.control.id}");

    final controlColor =
        widget.control.getColor("picker_color", context) ?? Colors.black;
    if (controlColor.value != _pickerColor.value) {
      _pickerColor = controlColor;
    }

    final colorPickerHeight =
        widget.control.getDouble("color_picker_height") ?? 250.0;
    final enableAlpha = widget.control.getBool("enable_alpha", false)!;
    final hueRingStrokeWidth =
        widget.control.getDouble("hue_ring_stroke_width") ?? 20.0;
    final pickerAreaBorderRadius =
        widget.control.getBorderRadius("picker_area_border_radius") ??
            BorderRadius.zero;
    final portraitOnly = widget.control.getBool("portrait_only", false)!;

    final picker = HueRingPicker(
      pickerColor: _pickerColor,
      onColorChanged: _onColorChanged,
      colorPickerHeight: colorPickerHeight,
      enableAlpha: enableAlpha,
      hueRingStrokeWidth: hueRingStrokeWidth,
      pickerAreaBorderRadius: pickerAreaBorderRadius,
      portraitOnly: portraitOnly,
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
