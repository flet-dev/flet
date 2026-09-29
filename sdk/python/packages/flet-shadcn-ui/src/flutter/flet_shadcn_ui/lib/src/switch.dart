import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadSwitchControl extends StatelessWidget {
  final Control control;

  const ShadSwitchControl({super.key, required this.control});

  void _onChanged(bool value) {
    control.updateProperties({"value": value}, notify: true);
    control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadSwitch build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadSwitch(
          value: control.getBool("value", false)!,
          enabled: !control.disabled,
          onChanged: _onChanged,
          label: control.buildTextOrWidget("label"),
          sublabel: control.buildTextOrWidget("sublabel"),
          thumbColor: control.getColor("thumb_color", context),
          checkedTrackColor: control.getColor("track_color", context),
          uncheckedTrackColor:
              control.getColor("inactive_track_color", context),
        ),
      ),
    );
  }
}
