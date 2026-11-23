import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentSliderControl extends StatelessWidget {
  final Control control;

  const FluentSliderControl({super.key, required this.control});

  void _onChanged(double value) {
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentSlider build: ${control.id}");

    final min = control.getDouble("min", 0)!;
    final max = control.getDouble("max", 100)!;
    final disabled = control.disabled;

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Slider(
          // fluent_ui asserts that the value is within [min, max].
          value: control.getDouble("value", 0)!.clamp(min, max),
          min: min,
          max: max,
          divisions: control.getInt("divisions"),
          label: control.getString("label"),
          vertical: control.getBool("vertical", false)!,
          autofocus: control.getBool("autofocus", false)!,
          onChanged: disabled ? null : _onChanged,
          onChangeStart: disabled || !control.hasEventHandler("change_start")
              ? null
              : (value) => control.triggerEvent("change_start", value),
          onChangeEnd: disabled || !control.hasEventHandler("change_end")
              ? null
              : (value) => control.triggerEvent("change_end", value),
        ),
      ),
    );
  }
}
