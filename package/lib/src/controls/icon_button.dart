import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'error.dart';

class IconButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const IconButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    final ws = FletAppServices.of(context).ws;

    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    IconData? selectedIcon =
        getMaterialIcon(control.attrString("selectedIcon", "")!);
    Color? iconColor = HexColor.fromString(
        Theme.of(context), control.attrString("iconColor", "")!);
    Color? selectedIconColor = HexColor.fromString(
        Theme.of(context), control.attrString("selectedIconColor", "")!);
    Color? bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    double? iconSize = control.attrDouble("iconSize");
    var tooltip = control.attrString("tooltip");
    var contentCtrls = children.where((c) => c.name == "content");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool selected = control.attrBool("selected", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("Button ${control.id} clicked!");
            ws.pageEventFromWeb(
                eventTarget: control.id, eventName: "click", eventData: "");
          };

    Widget? button;

    var theme = Theme.of(context);

    var style = parseButtonStyle(Theme.of(context), control, "style",
        defaultForegroundColor: theme.colorScheme.primary,
        defaultBackgroundColor: Colors.transparent,
        defaultOverlayColor: Colors.transparent,
        defaultShadowColor: Colors.transparent,
        defaultSurfaceTintColor: Colors.transparent,
        defaultElevation: 0,
        defaultPadding: const EdgeInsets.all(8),
        defaultBorderSide: BorderSide.none,
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    if (icon != null) {
      button = IconButton(
          autofocus: autofocus,
          icon: Icon(
            icon,
            color: iconColor,
          ),
          iconSize: iconSize,
          tooltip: tooltip,
          style: style,
          isSelected: selected,
          selectedIcon: selectedIcon != null
              ? Icon(selectedIcon, color: selectedIconColor)
              : null,
          onPressed: onPressed);
    } else if (contentCtrls.isNotEmpty) {
      button = IconButton(
          autofocus: autofocus,
          onPressed: onPressed,
          iconSize: iconSize,
          style: style,
          tooltip: tooltip,
          isSelected: selected,
          selectedIcon: selectedIcon != null
              ? Icon(selectedIcon, color: selectedIconColor)
              : null,
          icon: createControl(control, contentCtrls.first.id, disabled));
    } else {
      return const ErrorControl(
          "Icon button does not have an icon neither content specified.");
    }

    if (bgColor != null) {
      button = Container(
        decoration:
            ShapeDecoration(color: bgColor, shape: const CircleBorder()),
        child: button,
      );
    }

    return constrainedControl(button, parent, control);
  }
}
