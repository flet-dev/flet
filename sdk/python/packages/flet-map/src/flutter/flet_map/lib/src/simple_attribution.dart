import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

class SimpleAttributionControl extends StatelessWidget {
  final Control control;

  const SimpleAttributionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("SimpleAttributionControl build: ${control.id}");
    var text = control.buildTextOrWidget("text");

    return SimpleAttributionWidget(
      source: text is Text ? text : const Text("Placeholder Text"),
      onTap: () => control.triggerEvent("click"),
      backgroundColor: control.getColor(
          "bgcolor", context, Theme.of(context).colorScheme.surface)!,
      alignment: control.getAlignment("alignment", Alignment.bottomRight)!,
    );
  }
}
