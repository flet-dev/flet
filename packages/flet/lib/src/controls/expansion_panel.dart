import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'base_controls.dart';
import 'control_widget.dart';

class ExpansionPanelListControl extends StatefulWidget {
  final Control control;

  const ExpansionPanelListControl({
    super.key,
    required this.control,
  });

  @override
  State<ExpansionPanelListControl> createState() =>
      _ExpansionPanelListControlState();
}

class _ExpansionPanelListControlState extends State<ExpansionPanelListControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionPanelList build: ${widget.control.id}");
    bool disabled = widget.control.disabled || widget.control.parent!.disabled;

    void onChange(int index, bool isExpanded) {
      FletBackend.of(context).updateControl(
          widget.control.children("panels")[index].id,
          {"expanded": isExpanded});
      FletBackend.of(context)
          .triggerControlEvent(widget.control, "change", index);
    }

    var panelList = ExpansionPanelList(
        elevation: widget.control.getDouble("elevation", 2)!,
        materialGapSize: widget.control.getDouble("spacing", 16)!,
        dividerColor: widget.control.getColor("dividerColor", context),
        expandIconColor: widget.control.getColor("expandedIconColor", context),
        expandedHeaderPadding: parseEdgeInsets(widget.control,
            "expandedHeaderPadding", const EdgeInsets.symmetric(vertical: 16))!,
        expansionCallback: !disabled
            ? (int index, bool isExpanded) {
                onChange(index, isExpanded);
              }
            : null,
        children: widget.control.children("controls").map((panelControl) {
          var headerCtrl = panelControl.child("header");
          var bodyCtrl = panelControl.child("content");

          return ExpansionPanel(
            backgroundColor: panelControl.getColor("bgColor", context),
            isExpanded: panelControl.getBool("expanded", false)!,
            canTapOnHeader: panelControl.getBool("canTapHeader", false)!,
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

    return ConstrainedControl(control: widget.control, child: panelList);
  }
}
