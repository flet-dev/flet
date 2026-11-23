import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/fields.dart';
import 'utils/theme.dart';

class FluentNumberBoxControl extends StatelessWidget {
  final Control control;

  const FluentNumberBoxControl({super.key, required this.control});

  void _onChanged(num? value) {
    // Whole numbers are reported as ints when no decimals are shown.
    final reported = value != null &&
            control.getInt("precision") == 0 &&
            value == value.roundToDouble()
        ? value.toInt()
        : value;
    control.updateProperties({"value": reported});
    control.triggerEvent("change", reported);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentNumberBox build: ${control.id}");

    final precision = control.getInt("precision");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        NumberBox<num>(
          value: control.getDouble("value"),
          onChanged: control.disabled ? null : _onChanged,
          min: control.getDouble("min"),
          max: control.getDouble("max"),
          smallChange: control.getDouble("small_change", 1)!,
          largeChange: control.getDouble("large_change", 10)!,
          // fluent_ui formats `precision` decimals with the pattern "#." plus
          // one "#" per decimal, which leaves a trailing "." for 0 decimals.
          precision: precision == 0 ? null : precision,
          pattern: precision == 0 ? "#" : null,
          allowExpressions: control.getBool("allow_expressions", false)!,
          // The compact mode's pop-up builds in the page's overlay, above the
          // fallback FluentTheme, so only inline buttons or none are offered.
          mode: control.getBool("spin_buttons", true)!
              ? SpinButtonPlacementMode.inline
              : SpinButtonPlacementMode.none,
          clearButton: control.getBool("clear_button", true)!,
          placeholder: control.getString("placeholder"),
          leadingIcon: buildFieldPrefix(control),
          autofocus: control.getBool("autofocus", false)!,
        ),
      ),
    );
  }
}
