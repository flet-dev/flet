import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/field.dart';

class ShadCheckboxControl extends StatelessWidget {
  final Control control;

  const ShadCheckboxControl({super.key, required this.control});

  void _onChanged(bool value) {
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadCheckbox build: ${control.id}");

    return LayoutControl(
      control: control,
      child: buildShadField(
        context,
        control,
        decorated: false,
        (decoration) => ShadCheckbox(
          decoration: decoration,
          value: control.getBool("value", false)!,
          enabled: !control.disabled,
          onChanged: _onChanged,
          label: control.buildTextOrWidget("label"),
          sublabel: control.buildTextOrWidget("sublabel"),
          color: control.getColor("color", context),
          uncheckedColor: control.getColor("unchecked_color", context),
          size: control.getDouble("size"),
        ),
      ),
    );
  }
}
