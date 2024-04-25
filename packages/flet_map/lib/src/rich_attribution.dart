import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
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

class _RichAttributionControlState extends State<RichAttributionControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "RichAttribution build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var ctrls = widget.children
        .where((c) => c.isVisible && c.type == "textsourceattribution");
    List attributions = ctrls
        .map((c) => createControl(widget.control, c.id, disabled))
        .toList();

    debugPrint("RichAttribution build: ${attributions} children");

    Widget rich = RichAttributionWidget(
      attributions: [],
      //attributions,
      permanentHeight: widget.control.attrDouble("permanentHeight", 24)!,
      popupBackgroundColor: widget.control.attrColor("popupBgColor", context),
      showFlutterMapAttribution:
          widget.control.attrBool("showFlutterMapAttribution", true)!,
      alignment: parseAttributionAlignment(
          "alignment", widget.control, AttributionAlignment.bottomRight)!,
    );

    return constrainedControl(context, rich, widget.parent, widget.control);
  }
}
