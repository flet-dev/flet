import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/attribution_alignment.dart';

class RichAttributionControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const RichAttributionControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<RichAttributionControl> createState() => _RichAttributionControlState();
}

class _RichAttributionControlState extends State<RichAttributionControl>
    with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "RichAttributionControl build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return withControls(widget.control.childIds, (context, attributionsView) {
      debugPrint("RichAttributionControlState build: ${widget.control.id}");

      var attributions = attributionsView.controlViews
          .map((v) => v.control)
          .where((c) => c.type == "maptextsourceattribution" && c.isVisible)
          .map((Control itemCtrl) {
        return TextSourceAttribution(
          itemCtrl.attrs["text"] ?? "Placeholder Text",
          textStyle: parseTextStyle(Theme.of(context), itemCtrl, "textStyle"),
          onTap: () {
            widget.backend.triggerControlEvent(itemCtrl.id, "click");
          },
          prependCopyright: itemCtrl.attrBool("prependCopyright", true)!,
        );
      }).toList();

      Widget rich = RichAttributionWidget(
        attributions: attributions,
        permanentHeight: widget.control.attrDouble("permanentHeight", 24)!,
        popupBackgroundColor: widget.control.attrColor("popupBgColor", context),
        showFlutterMapAttribution:
            widget.control.attrBool("showFlutterMapAttribution", true)!,
        alignment: parseAttributionAlignment(
            "alignment", widget.control, AttributionAlignment.bottomRight)!,
      );

      return constrainedControl(context, rich, widget.parent, widget.control);
    });
  }
}
