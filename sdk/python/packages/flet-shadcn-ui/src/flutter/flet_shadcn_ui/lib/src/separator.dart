import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadSeparatorControl extends StatelessWidget {
  final Control control;

  const ShadSeparatorControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadSeparator build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadSeparator.raw(
          variant: control.getBool("vertical", false)!
              ? ShadSeparatorVariant.vertical
              : ShadSeparatorVariant.horizontal,
          thickness: control.getDouble("thickness"),
          color: control.getColor("color", context),
          margin: control.getMargin("margin"),
        ),
      ),
    );
  }
}
