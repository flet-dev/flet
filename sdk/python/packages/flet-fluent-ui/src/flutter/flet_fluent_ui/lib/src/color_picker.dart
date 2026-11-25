import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentColorPickerControl extends StatelessWidget {
  final Control control;

  const FluentColorPickerControl({super.key, required this.control});

  void _onChanged(Color color) {
    final value = color.toHex();
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentColorPicker build: ${control.id}");

    final picker = ColorPicker(
      color: control.getColor("value", context) ?? const Color(0xFF0078D4),
      onChanged: _onChanged,
      orientation: control.getBool("horizontal", false)!
          ? Axis.horizontal
          : Axis.vertical,
      colorSpectrumShape: parseEnum(
        ColorSpectrumShape.values,
        control.getString("spectrum_shape"),
        ColorSpectrumShape.ring,
      )!,
      isColorPreviewVisible: control.getBool("show_preview", true)!,
      isColorSliderVisible: control.getBool("show_color_slider", true)!,
      isMoreButtonVisible: control.getBool("show_more_button", true)!,
      isColorChannelTextInputVisible: control.getBool(
        "show_channel_inputs",
        true,
      )!,
      isHexInputVisible: control.getBool("show_hex_input", true)!,
      isAlphaEnabled: control.getBool("alpha_enabled", true)!,
      isAlphaSliderVisible: control.getBool("show_alpha_slider", true)!,
      isAlphaTextInputVisible: control.getBool("show_alpha_input", true)!,
      minHue: control.getInt("min_hue", 0)!,
      maxHue: control.getInt("max_hue", 359)!,
      minSaturation: control.getInt("min_saturation", 0)!,
      maxSaturation: control.getInt("max_saturation", 100)!,
      minValue: control.getInt("min_brightness", 0)!,
      maxValue: control.getInt("max_brightness", 100)!,
    );

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        // fluent_ui's color picker has no disabled state.
        control.disabled ? IgnorePointer(child: picker) : picker,
      ),
    );
  }
}
