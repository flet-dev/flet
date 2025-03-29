import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class PlaceholderControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const PlaceholderControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Placeholder build: ${control.id}");
    var contentCtrls = children.where((c) => c.visible);

    return baseControl(
        context,
        Placeholder(
            fallbackHeight: control.getDouble("fallbackHeight", 400.0)!,
            fallbackWidth: control.getDouble("fallbackWidth", 400.0)!,
            color: control.getColor("color", context, const Color(0xFF455A64))!,
            strokeWidth: control.getDouble("strokeWidth", 2.0)!,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id,
                    control.disabled || parentDisabled,
                    parentAdaptive: control.adaptive ?? parentAdaptive)
                : null),
        parent,
        control);
  }
}
