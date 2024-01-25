import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'flet_control_state.dart';

class ExpansionPanelListControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ExpansionPanelListControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<ExpansionPanelListControl> createState() =>
      _ExpansionPanelListControlState();
}

class _ExpansionPanelListControlState extends State<ExpansionPanelListControl>
    with FletControlState {
  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionPanelList build: ${widget.control.id}");

    var panels = widget.children
        .where((c) => c.name == "expansionpanel" && c.isVisible)
        .toList();

    void onChange(int index, bool isExpanded) {
      updateControlProps(
          panels[index].id, {"expanded": isExpanded.toString().toLowerCase()});
      sendControlEvent(widget.control.id, "change", "$index");
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var dividerColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("dividerColor", "")!);
    var expandedIconColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("expandedIconColor", "")!);

    var expandedHeaderPadding =
        parseEdgeInsets(widget.control, "expandedHeaderPadding");

    debugPrint(
        "ExpansionPanelListControlFletControlState build: ${widget.control.id}");

    var panelList =
        withControls(panels.map((p) => p.id), (content, panelViews) {
      return ExpansionPanelList(
          elevation: widget.control.attrDouble("elevation", 2)!,
          materialGapSize: widget.control.attrDouble("spacing", 16)!,
          dividerColor: dividerColor,
          expandIconColor: expandedIconColor,
          expandedHeaderPadding:
              expandedHeaderPadding ?? const EdgeInsets.symmetric(vertical: 16),
          expansionCallback: !disabled
              ? (int index, bool isExpanded) {
                  onChange(index, isExpanded);
                }
              : null,
          children: panelViews.controlViews.map((panelView) {
            var headerCtrls = panelView.children
                .where((c) => c.name == "header" && c.isVisible);
            var bodyCtrls = panelView.children
                .where((c) => c.name == "content" && c.isVisible);

            var isExpanded = panelView.control.attrBool("expanded", false)!;
            var canTapHeader =
                panelView.control.attrBool("canTapHeader", false)!;
            var bgColor = HexColor.fromString(Theme.of(context),
                panelView.control.attrString("bgColor", "")!);

            return ExpansionPanel(
              backgroundColor: bgColor,
              isExpanded: isExpanded,
              canTapOnHeader: canTapHeader,
              headerBuilder: (BuildContext context, bool isExpanded) {
                return headerCtrls.isNotEmpty
                    ? createControl(
                        widget.control, headerCtrls.first.id, disabled)
                    : const ListTile(title: Text("Header Placeholder"));
              },
              body: bodyCtrls.isNotEmpty
                  ? createControl(widget.control, bodyCtrls.first.id, disabled)
                  : const ListTile(title: Text("Body Placeholder")),
            );
          }).toList());
    });

    return constrainedControl(
        context, panelList, widget.parent, widget.control);
  }
}
