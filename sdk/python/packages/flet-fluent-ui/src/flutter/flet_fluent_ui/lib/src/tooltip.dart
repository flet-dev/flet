import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentTooltipControl extends StatelessWidget {
  final Control control;

  const FluentTooltipControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTooltip build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        Tooltip(
          message: control.getString("message", "")!,
          style: TooltipThemeData(
            preferBelow: control.getBool("show_below", true)!,
            waitDuration: control.getDuration("wait_duration"),
            showDuration: control.getDuration("show_duration"),
          ),
          child: control.buildWidget("content"),
        ),
      ),
    );
  }
}
