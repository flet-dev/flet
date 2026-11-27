import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentRadioGroupControl extends StatelessWidget {
  final Control control;

  const FluentRadioGroupControl({super.key, required this.control});

  void _onChanged(String? value) {
    if (value == null || value == control.getString("value")) return;
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentRadioGroup build: ${control.id}");

    final spacing = control.getDouble("spacing", 8)!;
    final items = control.buildWidgets("items");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        // RadioGroup is the Flutter widgets-layer group that fluent_ui's
        // RadioButton registers with.
        RadioGroup<String>(
          groupValue: control.getString("value"),
          onChanged: _onChanged,
          child: control.getBool("horizontal", false)!
              ? Wrap(spacing: spacing, runSpacing: spacing, children: items)
              : Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  spacing: spacing,
                  children: items,
                ),
        ),
      ),
    );
  }
}

/// A `flet_fluent_ui.RadioButton`; must be inside a `FluentRadioGroupControl`.
class FluentRadioButtonControl extends StatelessWidget {
  final Control control;

  const FluentRadioButtonControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    return RadioButton<String>(
      value: control.getString("value", "")!,
      enabled: !control.disabled,
      content: control.buildTextOrWidget("label"),
    );
  }
}
