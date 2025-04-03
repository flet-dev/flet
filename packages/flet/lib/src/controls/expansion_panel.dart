import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'control_widget.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class ExpansionPanelListControl extends StatefulWidget {
  //final Control? parent;
  final Control control;
  //final List<Control> children;
  //final bool parentDisabled;
  //final bool? parentAdaptive;
  //final FletControlBackend backend;

  const ExpansionPanelListControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.children,
    //required this.parentDisabled,
    //required this.parentAdaptive,
    //required this.backend,
  });

  @override
  State<ExpansionPanelListControl> createState() =>
      _ExpansionPanelListControlState();
}

class _ExpansionPanelListControlState extends State<ExpansionPanelListControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("ExpansionPanelList build: ${widget.control.id}");
    //bool disabled = widget.control.disabled || widget.parentDisabled;
    bool disabled = widget.control.disabled || widget.control.parent!.disabled;
    // bool? adaptive =
    //     widget.control.getBool("adaptive") ?? widget.parentAdaptive;
    bool? adaptive = widget.control.adaptive ?? widget.control.parent?.adaptive;
    // var panels = widget.children
    //     .where((c) => c.name == "expansionpanel" && c.visible)
    //     .toList();

    var panels = widget.control
        .children("controls")
        .map((child) => ControlWidget(control: child, key: ValueKey(child.id)))
        .toList();

    void onChange(int index, bool isExpanded) {
      widget.backend.updateControlState(
          panels[index].id, {"expanded": isExpanded.toString().toLowerCase()});
      widget.backend.triggerControlEvent(widget.control.id, "change", "$index");
    }

    var panelList =
        withControls(panels.map((p) => p.id), (content, panelViews) {
      return ExpansionPanelList(
          elevation: widget.control.getDouble("elevation", 2)!,
          materialGapSize: widget.control.getDouble("spacing", 16)!,
          dividerColor: widget.control.getColor("dividerColor", context),
          expandIconColor:
              widget.control.getColor("expandedIconColor", context),
          expandedHeaderPadding: parseEdgeInsets(
              widget.control,
              "expandedHeaderPadding",
              const EdgeInsets.symmetric(vertical: 16))!,
          expansionCallback: !disabled
              ? (int index, bool isExpanded) {
                  onChange(index, isExpanded);
                }
              : null,
          children: panelViews.controlViews.map((panelView) {
            var headerCtrls = panelView.children
                .where((c) => c.name == "header" && c.visible);
            var bodyCtrls = panelView.children
                .where((c) => c.name == "content" && c.visible);

            return ExpansionPanel(
              backgroundColor: panelView.control.getColor("bgColor", context),
              isExpanded: panelView.control.getBool("expanded", false)!,
              canTapOnHeader: panelView.control.getBool("canTapHeader", false)!,
              headerBuilder: (BuildContext context, bool isExpanded) {
                return headerCtrls.isNotEmpty
                    ? createControl(
                        widget.control, headerCtrls.first.id, disabled,
                        parentAdaptive: adaptive)
                    : const ListTile(title: Text("Header Placeholder"));
              },
              body: bodyCtrls.isNotEmpty
                  ? createControl(widget.control, bodyCtrls.first.id, disabled,
                      parentAdaptive: adaptive)
                  : const ListTile(title: Text("Body Placeholder")),
            );
          }).toList());
    });

    return constrainedControl(
        context, panelList, widget.parent, widget.control);
  }
}
