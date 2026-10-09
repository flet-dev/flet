import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadThemeControl extends StatelessWidget {
  final Control control;

  const ShadThemeControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadTheme build: ${control.id}");

    return LayoutControl(
      control: control,
      child: ShadTheme(
        data: parseShadThemeData(control, context),
        child: control.buildWidget("content") ?? const SizedBox.shrink(),
      ),
    );
  }
}
