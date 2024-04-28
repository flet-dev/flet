import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

class SimpleAttributionControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const SimpleAttributionControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<SimpleAttributionControl> createState() =>
      _SimpleAttributionControlState();
}

class _SimpleAttributionControlState extends State<SimpleAttributionControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "SimpleAttributionControl build: ${widget.control.id} (${widget.control.hashCode})");

    Widget a = SimpleAttributionWidget(
      source: Text(widget.control.attrString("text", "Placeholder Text")!),
      onTap: () {
        widget.backend.triggerControlEvent(widget.control.id, "click");
      },
      backgroundColor: widget.control.attrColor("backgroundColor", context),
      alignment:
          parseAlignment(widget.control, "alignment", Alignment.bottomRight)!,
    );

    return constrainedControl(context, a, widget.parent, widget.control);
  }
}
