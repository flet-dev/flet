import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

class TextSourceAttributionControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const TextSourceAttributionControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "TextSourceAttributionControl build: ${control.id} (${control.hashCode})");

    Widget text = TextSourceAttribution(
      control.attrString("text", "Placeholder Text")!,
      textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
      onTap: () {
        backend.triggerControlEvent(control.id, "click");
      },
      prependCopyright: control.attrBool("prependCopyright", true)!,
    );

    return constrainedControl(context, text, parent, control);
  }
}
