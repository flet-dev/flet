import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'base_controls.dart';

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
      control
          .children("controls")[index]
          .updateProperties({"expanded": isExpanded}, notify: true);
      control.triggerEvent("change", index);
    }

    var panelList = ExpansionPanelList(
        elevation: control.getDouble("elevation", 2)!,
        materialGapSize: control.getDouble("spacing", 16)!,
        dividerColor: control.getColor("divider_color", context),
        expandIconColor: control.getColor("expanded_icon_color", context),
        expandedHeaderPadding: control.getEdgeInsets("expanded_header_padding",
            const EdgeInsets.symmetric(vertical: 16))!,
        expansionCallback: !control.disabled
            ? (int index, bool isExpanded) {
                onChange(index, isExpanded);
              }
            : null,
        children: control.children("controls").map((panelControl) {
          panelControl.notifyParent = true;
          return ExpansionPanel(
            backgroundColor: panelControl.getColor("bgcolor", context),
            isExpanded: panelControl.getBool("expanded", false)!,
            highlightColor: panelControl.getColor("highlight_color", context),
            splashColor: panelControl.getColor("splash_color", context),
            canTapOnHeader: panelControl.getBool("can_tap_header", false)!,
            headerBuilder: (BuildContext context, bool isExpanded) {
              return panelControl.buildWidget("header") ??
                  const ListTile(title: Text("Header Placeholder"));
            },
            body: panelControl.buildWidget("content") ??
                const ListTile(title: Text("Body Placeholder")),
          );
        }).toList());

    return ConstrainedControl(control: control, child: panelList);
  }
}
