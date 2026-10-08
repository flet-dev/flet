import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadBadgeControl extends StatelessWidget {
  final Control control;

  const ShadBadgeControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadBadge build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadBadge.raw(
          variant: parseEnum(ShadBadgeVariant.values,
              control.getString("variant"), ShadBadgeVariant.primary)!,
          backgroundColor: control.getColor("bgcolor", context),
          hoverBackgroundColor: control.getColor("hover_bgcolor", context),
          foregroundColor: control.getColor("color", context),
          onPressed: control.hasEventHandler("click") && !control.disabled
              ? () => control.triggerEvent("click")
              : null,
          child: control.buildTextOrWidget("content", required: true)!,
        ),
      ),
    );
  }
}
