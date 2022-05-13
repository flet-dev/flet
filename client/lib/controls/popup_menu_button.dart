import 'package:flet_view/utils/icons.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

class PopupMenuButtonControl extends StatefulWidget {
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
  State<PopupMenuButtonControl> createState() => _PopupMenuButtonControlState();
}

class _PopupMenuButtonControlState extends State<PopupMenuButtonControl> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("PopupMenuButton build: ${widget.control.id}");

    var icon = getMaterialIcon(widget.control.attrString("icon", "")!);
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var popupButton = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store, widget.children.map((c) => c.id)),
        builder: (content, viewModel) {
          return PopupMenuButton<String>(
              enabled: !disabled,
              icon: icon != null ? Icon(icon) : null,
              shape: Theme.of(context).useMaterial3
                  ? RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10))
                  : null,
              onCanceled: () {
                ws.pageEventFromWeb(
                    eventTarget: widget.control.id,
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
                      child = createControl(cv.control, contentCtrls.first.id,
                          widget.parentDisabled);
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

    return constrainedControl(popupButton, widget.parent, widget.control);
  }
}
