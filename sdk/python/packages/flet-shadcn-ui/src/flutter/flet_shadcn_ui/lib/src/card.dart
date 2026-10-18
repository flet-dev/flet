import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadCardControl extends StatelessWidget {
  final Control control;

  const ShadCardControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadCard build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadCard(
          title: control.buildTextOrWidget("title"),
          description: control.buildTextOrWidget("description"),
          footer: control.buildWidget("footer"),
          leading: control.buildWidget("leading"),
          trailing: control.buildWidget("trailing"),
          padding: control.getPadding("padding"),
          backgroundColor: control.getColor("bgcolor", context),
          radius: control.getBorderRadius("border_radius"),
          child: control.buildWidget("content"),
        ),
      ),
    );
  }
}
