import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class PopupMenuButtonControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final FletControlBackend backend;

  const PopupMenuButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("PopupMenuButton build: ${control.id}");

    var icon = parseIcon(control.getString("icon"));
    var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    bool disabled = control.disabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var popupButton = withControls(
        children
            .where((c) => c.name != "content" && c.visible)
            .map((c) => c.id), (content, viewModel) {
      return PopupMenuButton<String>(
          enabled: !disabled,
          tooltip: null,
          icon: icon != null ? Icon(icon) : null,
          iconSize: control.getDouble("iconSize"),
          splashRadius: control.getDouble("splashRadius"),
          shadowColor: control.getColor("shadowColor", context),
          surfaceTintColor: control.getColor("surfaceTintColor", context),
          iconColor: control.getColor("iconColor", context),
          elevation: control.getDouble("elevation"),
          enableFeedback: control.getBool("enableFeedback"),
          padding:
              parseEdgeInsets(control, "padding", const EdgeInsets.all(8))!,
          color: control.getColor("bgcolor", context),
          clipBehavior:
              parseClip(control.getString("clipBehavior"), Clip.none)!,
          shape: parseOutlinedBorder(control, "shape") ??
              (Theme.of(context).useMaterial3
                  ? RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10))
                  : null),
          constraints: parseBoxConstraints(control, "sizeConstraints"),
          style: parseButtonStyle(Theme.of(context), control, "style"),
          popUpAnimationStyle:
              parseAnimationStyle(control, "popupAnimationStyle"),
          menuPadding: parseEdgeInsets(control, "menuPadding"),
          onSelected: (String selection) {
            backend.triggerControlEvent(control.id, "select", selection);
          },
          onCanceled: () {
            backend.triggerControlEvent(control.id, "cancel");
          },
          onOpened: () {
            backend.triggerControlEvent(control.id, "open");
          },
          position: parsePopupMenuPosition(control.getString("menuPosition")),
          itemBuilder: (BuildContext context) =>
              viewModel.controlViews.map((cv) {
                var itemIcon = parseIcon(cv.control.getString("icon"));
                var text = cv.control.getString("text", "")!;
                var checked = cv.control.getBool("checked");
                var height = cv.control.getDouble("height", 48.0)!;
                var padding = parseEdgeInsets(cv.control, "padding");
                var disabled = cv.control.disabled || parentDisabled;
                var contentCtrls =
                    cv.children.where((c) => c.name == "content" && c.visible);

                Widget? child;
                if (contentCtrls.isNotEmpty) {
                  // custom content
                  child = createControl(
                      cv.control, contentCtrls.first.id, parentDisabled);
                } else if (itemIcon != null && text != "") {
                  // icon and text
                  child = Row(children: [
                    Icon(itemIcon),
                    const SizedBox(width: 8),
                    Text(text)
                  ]);
                } else if (text != "") {
                  child = Text(text);
                }

                var item = checked != null
                    ? CheckedPopupMenuItem<String>(
                        value: cv.control.id,
                        checked: checked,
                        height: height,
                        padding: padding,
                        enabled: !disabled || !cv.control.disabled,
                        mouseCursor: parseMouseCursor(
                            cv.control.getString("mouseCursor")),
                        onTap: () {
                          backend.triggerControlEvent(
                              cv.control.id, "click", "${!checked}");
                        },
                        child: child,
                      )
                    : PopupMenuItem<String>(
                        value: cv.control.id,
                        height: height,
                        padding: padding,
                        enabled: !disabled || !cv.control.disabled,
                        mouseCursor: parseMouseCursor(
                            cv.control.getString("mouseCursor")),
                        onTap: () {
                          backend.triggerControlEvent(cv.control.id, "click");
                        },
                        child: child);

                return child != null
                    ? item
                    : const PopupMenuDivider() as PopupMenuEntry<String>;
              }).toList(),
          child: child);
    });
    return constrainedControl(
        context,
        TooltipVisibility(
            visible: control.getString("tooltip") == null, child: popupButton),
        parent,
        control);
  }
}
