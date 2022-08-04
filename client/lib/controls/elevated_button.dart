import 'package:flet_view/utils/buttons.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

class ElevatedButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ElevatedButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    String text = control.attrString("text", "")!;
    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    Color? iconColor = HexColor.fromString(
        Theme.of(context), control.attrString("iconColor", "")!);
    Color? color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    Color? bgcolor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);
    var elevation = control.attrDouble("elevation");
    var contentCtrls = children.where((c) => c.name == "content");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("Button ${control.id} clicked!");
            ws.pageEventFromWeb(
                eventTarget: control.id,
                eventName: "click",
                eventData: control.attrs["data"] ?? "");
          };

    Function()? onLongPress = disabled
        ? null
        : () {
            debugPrint("Button ${control.id} long pressed!");
            ws.pageEventFromWeb(
                eventTarget: control.id,
                eventName: "long_press",
                eventData: control.attrs["data"] ?? "");
          };

    ElevatedButton? button;

    var theme = Theme.of(context);

    var style = parseButtonStyle(Theme.of(context), control, "style",
        defaultForegroundColor: theme.colorScheme.primary,
        defaultBackgroundColor: theme.colorScheme.surface,
        defaultOverlayColor: theme.colorScheme.primary.withOpacity(0.08),
        defaultShadowColor: theme.colorScheme.shadow,
        defaultSurfaceTintColor: theme.colorScheme.surfaceTint,
        defaultElevation: 1,
        defaultPadding: const EdgeInsets.symmetric(horizontal: 8),
        defaultBorderSide: BorderSide.none,
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    if (icon != null) {
      button = ElevatedButton.icon(
          style: style,
          autofocus: autofocus,
          onPressed: onPressed,
          onLongPress: onLongPress,
          icon: Icon(
            icon,
            color: iconColor,
          ),
          label: Text(text));
    } else if (contentCtrls.isNotEmpty) {
      button = ElevatedButton(
          style: style,
          autofocus: autofocus,
          onPressed: onPressed,
          onLongPress: onLongPress,
          child: createControl(control, contentCtrls.first.id, disabled));
    } else {
      button = ElevatedButton(
          style: style,
          onPressed: onPressed,
          onLongPress: onLongPress,
          child: Text(text));
    }

    return constrainedControl(button, parent, control);
  }
}
