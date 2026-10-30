import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadProgressControl extends StatelessWidget {
  final Control control;

  const ShadProgressControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadProgress build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadProgress(
          value: control.getDouble("value"),
          color: control.getColor("color", context),
          backgroundColor: control.getColor("bgcolor", context),
          minHeight: control.getDouble("bar_height"),
        ),
      ),
    );
  }
}
