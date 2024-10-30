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
    var contentCtrls = children.where((c) => c.isVisible);

    return baseControl(
        context,
        Placeholder(
            fallbackHeight: control.attrDouble("fallbackHeight", 400.0)!,
            fallbackWidth: control.attrDouble("fallbackWidth", 400.0)!,
            color:
                control.attrColor("color", context, const Color(0xFF455A64))!,
            strokeWidth: control.attrDouble("strokeWidth", 2.0)!,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id,
                    control.isDisabled || parentDisabled,
                    parentAdaptive: control.isAdaptive ?? parentAdaptive)
                : null),
        parent,
        control);
  }
}
