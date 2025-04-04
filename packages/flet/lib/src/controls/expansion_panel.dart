import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class ExpansionPanelListControl extends StatelessWidget {
  final Control control;

  const ExpansionPanelListControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionPanelList build: ${control.id}");

    void onChange(int index, bool isExpanded) {
      FletBackend.of(context).updateControl(
          control.children("controls")[index].id, {"expanded": isExpanded},
          notify: true);
      FletBackend.of(context).triggerControlEvent(control, "change", index);
    }

    var panelList = ExpansionPanelList(
        elevation: control.getDouble("elevation", 2)!,
        materialGapSize: control.getDouble("spacing", 16)!,
        dividerColor: control.getColor("divider_color", context),
        expandIconColor: control.getColor("expanded_icon_color", context),
        expandedHeaderPadding: parseEdgeInsets(
            control,
            "expanded_header_padding",
            const EdgeInsets.symmetric(vertical: 16))!,
        expansionCallback: !control.disabled
            ? (int index, bool isExpanded) {
                onChange(index, isExpanded);
              }
            : null,
        children: control.children("controls").map((panelControl) {
          panelControl.notifyParent = true;

          var headerCtrl = panelControl.child("header");
          var bodyCtrl = panelControl.child("content");

          return ExpansionPanel(
            backgroundColor: panelControl.getColor("bgColor", context),
            isExpanded: panelControl.getBool("expanded", false)!,
            canTapOnHeader: panelControl.getBool("can_tap_header", false)!,
            headerBuilder: (BuildContext context, bool isExpanded) {
              return headerCtrl != null
                  ? ControlWidget(
                      control: headerCtrl,
                    )
                  : const ListTile(title: Text("Header Placeholder"));
            },
            body: bodyCtrl != null
                ? ControlWidget(
                    control: bodyCtrl,
                  )
                : const ListTile(title: Text("Body Placeholder")),
          );
        }).toList());

    return ConstrainedControl(control: control, child: panelList);
  }
}
