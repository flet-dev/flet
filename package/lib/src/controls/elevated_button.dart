import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'error.dart';

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

    final server = FletAppServices.of(context).server;

    String text = control.attrString("text", "")!;
    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    Color? iconColor = HexColor.fromString(
        Theme.of(context), control.attrString("iconColor", "")!);
    var contentCtrls = children.where((c) => c.name == "content");
    bool onHover = control.attrBool("onHover", false)!;
    bool onLongPress = control.attrBool("onLongPress", false)!;
    bool autofocus = control.attrBool("autofocus", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("Button ${control.id} clicked!");
            server.sendPageEvent(
                eventTarget: control.id, eventName: "click", eventData: "");
          }
        : null;

    Function()? onLongPressHandler = onLongPress && !disabled
        ? () {
            debugPrint("Button ${control.id} long pressed!");
            server.sendPageEvent(
                eventTarget: control.id,
                eventName: "long_press",
                eventData: "");
          }
        : null;

    Function(bool)? onHoverHandler = onHover && !disabled
        ? (state) {
            debugPrint("Button ${control.id} hovered!");
            server.sendPageEvent(
                eventTarget: control.id,
                eventName: "hover",
                eventData: state.toString());
          }
        : null;

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
      if (text == "") {
        return const ErrorControl("Error displaying ElevatedButton",
            description: "\"icon\" must be specified together with \"text\".");
      }
      button = ElevatedButton.icon(
          style: style,
          autofocus: autofocus,
          onPressed: onPressed,
          onLongPress: onLongPressHandler,
          onHover: onHoverHandler,
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
          onLongPress: onLongPressHandler,
          onHover: onHoverHandler,
          child: createControl(control, contentCtrls.first.id, disabled));
    } else {
      button = ElevatedButton(
          style: style,
          onPressed: onPressed,
          onLongPress: onLongPressHandler,
          onHover: onHoverHandler,
          child: Text(text));
    }

    return constrainedControl(context, button, parent, control);
  }
}
