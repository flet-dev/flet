import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadAlertControl extends StatelessWidget {
  final Control control;

  const ShadAlertControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadAlert build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadAlert.raw(
          variant: parseEnum(ShadAlertVariant.values,
              control.getString("variant"), ShadAlertVariant.primary)!,
          icon: control.buildIconOrWidget("icon"),
          iconColor: control.getColor("icon_color", context),
          title: control.buildTextOrWidget("title"),
          description: control.buildTextOrWidget("description"),
        ),
      ),
    );
  }
}
