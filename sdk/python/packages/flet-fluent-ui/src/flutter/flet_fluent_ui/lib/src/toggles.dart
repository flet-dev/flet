import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

void _setValue(Control control, String property, dynamic value) {
  control.updateProperties({property: value}, notify: true);
  control.triggerEvent("change", value);
}

class FluentToggleButtonControl extends StatelessWidget {
  final Control control;

  const FluentToggleButtonControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentToggleButton build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        ToggleButton(
          checked: control.getBool("checked", false)!,
          onChanged: control.disabled
              ? null
              : (value) => _setValue(control, "checked", value),
          autofocus: control.getBool("autofocus", false)!,
          child: control.buildTextOrWidget("content"),
        ),
      ),
    );
  }
}

class FluentCheckboxControl extends StatelessWidget {
  final Control control;

  const FluentCheckboxControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentCheckbox build: ${control.id}");

    final tristate = control.getBool("tristate", false)!;
    // `None` means "indeterminate" with tristate enabled, unchecked otherwise.
    final bool? value = control.getBool("value") ?? (tristate ? null : false);

    // fluent_ui's Checkbox reports null for a tap on the indeterminate state,
    // so the next value is worked out here: unchecked -> checked ->
    // indeterminate (tristate only) -> unchecked.
    final bool? next = switch (value) {
      false => true,
      true => tristate ? null : false,
      null => false,
    };

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Checkbox(
          checked: value,
          onChanged: control.disabled
              ? null
              : (_) => _setValue(control, "value", next),
          autofocus: control.getBool("autofocus", false)!,
          content: control.buildTextOrWidget("label"),
        ),
      ),
    );
  }
}

class FluentToggleSwitchControl extends StatelessWidget {
  final Control control;

  const FluentToggleSwitchControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentToggleSwitch build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        ToggleSwitch(
          checked: control.getBool("value", false)!,
          onChanged: control.disabled
              ? null
              : (value) => _setValue(control, "value", value),
          autofocus: control.getBool("autofocus", false)!,
          content: control.buildTextOrWidget("label"),
          leadingContent: control.getBool("label_first", false)!,
        ),
      ),
    );
  }
}
