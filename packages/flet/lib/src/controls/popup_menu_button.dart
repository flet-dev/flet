import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/mouse.dart';
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

    var icon = parseIcon(control.attrString("icon", "")!);
    var tooltip = control.attrString("tooltip", "")!;
    var iconSize = control.attrDouble("iconSize");
    var splashRadius = control.attrDouble("splashRadius");
    var elevation = control.attrDouble("elevation");
    var enableFeedback = control.attrBool("enableFeedback");
    var shape = parseOutlinedBorder(control, "shape") ??
        (Theme.of(context).useMaterial3
            ? RoundedRectangleBorder(borderRadius: BorderRadius.circular(10))
            : null);
    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);
    var bgcolor = control.attrColor("bgcolor", context);
    var iconColor = control.attrColor("iconColor", context);
    var shadowColor = control.attrColor("shadowColor", context);
    var surfaceTintColor = control.attrColor("surfaceTintColor", context);
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    PopupMenuPosition? menuPosition = PopupMenuPosition.values.firstWhereOrNull(
        (p) =>
            p.name.toLowerCase() ==
            control.attrString("menuPosition", "")!.toLowerCase());

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var popupButton = withControls(
        children.where((c) => c.name != "content").map((c) => c.id),
        (content, viewModel) {
      return PopupMenuButton<String>(
          enabled: !disabled,
          icon: icon != null ? Icon(icon) : null,
          tooltip: tooltip,
          iconSize: iconSize,
          splashRadius: splashRadius,
          shadowColor: shadowColor,
          surfaceTintColor: surfaceTintColor,
          iconColor: iconColor,
          elevation: elevation,
          enableFeedback: enableFeedback,
          padding:
              parseEdgeInsets(control, "padding") ?? const EdgeInsets.all(8),
          color: bgcolor,
          clipBehavior: clipBehavior,
          shape: shape,
          onCanceled: () {
            backend.triggerControlEvent(control.id, "cancel");
            backend.triggerControlEvent(control.id, "cancelled"); // DEPRECATED
          },
          onOpened: () {
            backend.triggerControlEvent(control.id, "open");
          },
          onSelected: (itemId) {
            backend.triggerControlEvent(itemId, "click");
          },
          position: menuPosition,
          itemBuilder: (BuildContext context) =>
              viewModel.controlViews.map((cv) {
                var itemIcon = parseIcon(cv.control.attrString("icon", "")!);
                var text = cv.control.attrString("text", "")!;
                var checked = cv.control.attrBool("checked");
                var height = cv.control.attrDouble("height", 48.0)!;
                var padding = parseEdgeInsets(cv.control, "padding");
                var disabled = cv.control.isDisabled || parentDisabled;
                var contentCtrls =
                    cv.children.where((c) => c.name == "content");

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
                        enabled: !disabled || !cv.control.isDisabled,
                        mouseCursor: parseMouseCursor(
                            cv.control.attrString("mouseCursor")),
                        onTap: () {
                          backend.updateControlState(
                              cv.control.id, {"checked": "${!checked}"});
                          backend.triggerControlEvent(
                              cv.control.id, "click", "${!checked}");
                        },
                        child: child,
                      )
                    : PopupMenuItem<String>(
                        value: cv.control.id,
                        height: height,
                        padding: padding,
                        enabled: !disabled || !cv.control.isDisabled,
                        mouseCursor: parseMouseCursor(
                            cv.control.attrString("mouseCursor")),
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
        TooltipVisibility(visible: tooltip != "", child: popupButton),
        parent,
        control);
  }
}
