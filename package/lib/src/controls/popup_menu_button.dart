import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'flet_stateless_control.dart';

class PopupMenuButtonControl extends FletStatelessControl {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const PopupMenuButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("PopupMenuButton build: ${control.id}");

    final server = FletAppServices.of(context).server;

    var icon = parseIcon(control.attrString("icon", "")!);
    var tooltip = control.attrString("tooltip");
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

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
          shape: Theme.of(context).useMaterial3
              ? RoundedRectangleBorder(borderRadius: BorderRadius.circular(10))
              : null,
          onCanceled: () {
            server.sendPageEvent(
                eventTarget: control.id, eventName: "cancelled", eventData: "");
          },
          onSelected: (itemId) {
            server.sendPageEvent(
                eventTarget: itemId, eventName: "click", eventData: "");
          },
          itemBuilder: (BuildContext context) =>
              viewModel.controlViews.map((cv) {
                var itemIcon = parseIcon(cv.control.attrString("icon", "")!);
                var text = cv.control.attrString("text", "")!;
                var checked = cv.control.attrBool("checked");
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
                        child: child,
                      )
                    : PopupMenuItem<String>(value: cv.control.id, child: child);

                return child != null
                    ? item
                    : const PopupMenuDivider() as PopupMenuEntry<String>;
              }).toList(),
          child: child);
    });

    return constrainedControl(context, popupButton, parent, control);
  }
}
