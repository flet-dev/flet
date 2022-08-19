import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../utils/icons.dart';
import 'create_control.dart';

class PopupMenuButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const PopupMenuButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("PopupMenuButton build: ${control.id}");

    final ws = FletAppServices.of(context).ws;

    var icon = getMaterialIcon(control.attrString("icon", "")!);
    var tooltip = control.attrString("tooltip");
    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled)
        : null;

    var popupButton = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store, children.where((c) => c.name != "content").map((c) => c.id)),
        builder: (content, viewModel) {
          return PopupMenuButton<String>(
              enabled: !disabled,
              icon: icon != null ? Icon(icon) : null,
              tooltip: tooltip,
              child: child,
              shape: Theme.of(context).useMaterial3
                  ? RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10))
                  : null,
              onCanceled: () {
                ws.pageEventFromWeb(
                    eventTarget: control.id,
                    eventName: "cancelled",
                    eventData: "");
              },
              onSelected: (itemId) {
                ws.pageEventFromWeb(
                    eventTarget: itemId, eventName: "click", eventData: "");
              },
              itemBuilder: (BuildContext context) =>
                  viewModel.controlViews.map((cv) {
                    var itemIcon =
                        getMaterialIcon(cv.control.attrString("icon", "")!);
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
                        : PopupMenuItem<String>(
                            value: cv.control.id, child: child);

                    return child != null
                        ? item
                        : const PopupMenuDivider() as PopupMenuEntry<String>;
                  }).toList());
        });

    return constrainedControl(popupButton, parent, control);
  }
}
