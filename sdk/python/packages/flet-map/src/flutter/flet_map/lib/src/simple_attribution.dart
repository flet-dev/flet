import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

class SimpleAttributionControl extends StatelessWidget {
  final Control control;

  const SimpleAttributionControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("SimpleAttributionControl build: ${control.id}");
    final text = control.getString("text");

    if (text == null) {
      return const ErrorControl("SimpleAttribution.text must be provided");
    }

    return BaseControl(
      control: control,
      child: SimpleAttributionWidget(
        source: Text(
          text,
          style: control.getTextStyle("text_style", Theme.of(context)),
        ),
        onTap: () => control.triggerEvent("click"),
        backgroundColor: control.getColor(
            "bgcolor", context, Theme.of(context).colorScheme.surface)!,
        alignment: control.getAlignment("alignment", Alignment.bottomRight)!,
      ),
    );
  }
}
