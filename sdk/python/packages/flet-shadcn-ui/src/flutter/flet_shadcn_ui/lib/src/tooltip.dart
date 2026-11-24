import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadTooltipControl extends StatelessWidget {
  final Control control;

  const ShadTooltipControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadTooltip build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadTooltip(
          waitDuration: control.getDuration("wait_duration", Duration.zero),
          showDuration: control.getDuration("show_duration"),
          builder: (context) =>
              control.buildTextOrWidget("message", required: true)!,
          // ShadTooltip doesn't detect hover itself: it passes an
          // onHoverChange callback down through the theme, and only shadcn
          // widgets call it. ShadGestureDetector reads that callback, so any
          // Flet control can show the tooltip.
          child: ShadGestureDetector(
            child: control.buildWidget("content") ?? const SizedBox.shrink(),
          ),
        ),
      ),
    );
  }
}
