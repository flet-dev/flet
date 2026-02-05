import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:flet/src/utils/enums.dart';
import 'utils/color_picker.dart';

class ColorPickerControl extends StatefulWidget {
  final Control control;

  const ColorPickerControl({super.key, required this.control});

  @override
  State<ColorPickerControl> createState() => _ColorPickerControlState();
}

class _ColorPickerControlState extends State<ColorPickerControl> {
  Color _pickerColor = Colors.black;

  void _onColorChanged(Color color) {
    setState(() {
      _pickerColor = color;
    });
    final colorHex = color.toHex();
    widget.control.updateProperties({"picker_color": colorHex}, notify: true);
    widget.control.triggerEvent("color_change", colorHex);
  }

  void _onHsvColorChanged(HSVColor color) {
    final hsvData = {
      "alpha": color.alpha,
      "hue": color.hue,
      "saturation": color.saturation,
      "value": color.value,
    };
    widget.control
        .updateProperties({"picker_hsv_color": hsvData}, notify: true);
    widget.control.triggerEvent("hsv_color_change", hsvData);
  }

  void _onHistoryChanged(List<Color> colors) {
    final colorsHex = colors.map((color) => color.toHex()).toList();
    widget.control.updateProperties({"color_history": colorsHex}, notify: true);
    widget.control.triggerEvent("history_change", colorsHex);
  }

  ColorLabelType? _parseLabelType(String? value,
      [ColorLabelType? defaultValue]) {
    return parseEnum(ColorLabelType.values, value, defaultValue);
  }

  PaletteType? _parsePaletteType(String? value, [PaletteType? defaultValue]) {
    return parseEnum(PaletteType.values, value, defaultValue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ColorPickerControl build: ${widget.control.id}");

    final pickerHsvColor =
        parseHsvColor(widget.control.get("picker_hsv_color"));
    final controlColor =
        widget.control.getColor("picker_color", context) ?? Colors.black;
    if (pickerHsvColor != null) {
      final hsvColor = pickerHsvColor.toColor();
      if (hsvColor.value != _pickerColor.value) {
        _pickerColor = hsvColor;
      }
    } else if (controlColor.value != _pickerColor.value) {
      _pickerColor = controlColor;
    }

    final colorPickerWidth = widget.control.getDouble("color_picker_width");
    final displayThumbColor =
        widget.control.getBool("display_thumb_color", true)!;
    final enableAlpha = widget.control.getBool("enable_alpha", true)!;
    final hexInputBar = widget.control.getBool("hex_input_bar", true)!;
    final labelTextStyle =
        widget.control.getTextStyle("label_text_style", Theme.of(context));
    final rawLabelTypes = widget.control.get("label_types");
    final labelTypes = <ColorLabelType>[];
    if (rawLabelTypes is List) {
      for (final raw in rawLabelTypes) {
        final parsed = _parseLabelType(raw?.toString());
        if (parsed != null) {
          labelTypes.add(parsed);
        }
      }
    }
    final paletteType =
        _parsePaletteType(widget.control.get("palette_type")?.toString());
    final pickerAreaBorderRadius =
        widget.control.getBorderRadius("picker_area_border_radius");
    final pickerAreaHeightPercent =
        widget.control.getDouble("picker_area_height_percent") ?? 1.0;
    final labelTypesArg = rawLabelTypes is List
        ? labelTypes
        : const [ColorLabelType.rgb, ColorLabelType.hsv, ColorLabelType.hsl];

    final rawHistory = widget.control.get("color_history");
    final theme = Theme.of(context);
    final colorHistory = <Color>[];
    if (rawHistory is List) {
      for (final raw in rawHistory) {
        final parsed = parseColor(raw?.toString(), theme);
        if (parsed != null) {
          colorHistory.add(parsed);
        }
      }
    }

    final picker = ColorPicker(
      pickerColor: _pickerColor,
      onColorChanged: _onColorChanged,
      colorPickerWidth: colorPickerWidth ?? 300.0,
      colorHistory: colorHistory.isNotEmpty ? colorHistory : null,
      onHistoryChanged: _onHistoryChanged,
      displayThumbColor: displayThumbColor,
      enableAlpha: enableAlpha,
      hexInputBar: hexInputBar,
      labelTextStyle: labelTextStyle,
      labelTypes: labelTypesArg,
      paletteType: paletteType ?? PaletteType.hsvWithHue,
      pickerAreaBorderRadius: pickerAreaBorderRadius ?? BorderRadius.zero,
      pickerAreaHeightPercent: pickerAreaHeightPercent,
      pickerHsvColor: pickerHsvColor,
      onHsvColorChanged: _onHsvColorChanged,
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
