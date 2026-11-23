import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentInfoBarControl extends StatelessWidget {
  final Control control;

  const FluentInfoBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentInfoBar build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        InfoBar(
          title: control.buildTextOrWidget("title", required: true)!,
          content: control.buildTextOrWidget("content"),
          action: control.buildWidget("action"),
          severity: parseEnum(
            InfoBarSeverity.values,
            control.getString("severity"),
            InfoBarSeverity.info,
          )!,
          isLong: control.getBool("long", false)!,
          isIconVisible: control.getBool("icon_visible", true)!,
          onClose: control.hasEventHandler("close")
              ? () => control.triggerEvent("close")
              : null,
        ),
      ),
    );
  }
}
