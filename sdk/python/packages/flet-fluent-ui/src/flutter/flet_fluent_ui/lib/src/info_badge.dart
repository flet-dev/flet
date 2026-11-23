import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentInfoBadgeControl extends StatelessWidget {
  final Control control;

  const FluentInfoBadgeControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentInfoBadge build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        InfoBadge(
          source: control.buildTextOrWidget("content"),
          severity: parseEnum(
            InfoBarSeverity.values,
            control.getString("severity"),
            InfoBarSeverity.info,
          )!,
          color: control.getColor("bgcolor", context),
          foregroundColor: control.getColor("color", context),
        ),
      ),
    );
  }
}
