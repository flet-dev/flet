import 'error.dart';
import '../utils/gradient.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import 'create_control.dart';

class ShaderMaskControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const ShaderMaskControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("ShaderMask build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var blendMode = BlendMode.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("blendMode", "")!.toLowerCase(),
        orElse: () => BlendMode.modulate);
    bool disabled = control.isDisabled || parentDisabled;

    var gradient = parseGradient(Theme.of(context), control, "shader");
    if (gradient == null) {
      return const ErrorControl("Shader property is not set.");
    }

    return constrainedControl(
        _clipCorners(
            ShaderMask(
                shaderCallback: (bounds) {
                  debugPrint("shaderCallback: $bounds, $gradient");
                  return gradient.createShader(bounds);
                },
                blendMode: blendMode,
                child: contentCtrls.isNotEmpty
                    ? createControl(control, contentCtrls.first.id, disabled)
                    : null),
            control),
        parent,
        control);
  }

  Widget _clipCorners(Widget widget, Control control) {
    var borderRadius = parseBorderRadius(control, "borderRadius");
    return borderRadius != null
        ? ClipRRect(
            borderRadius: borderRadius,
            child: widget,
          )
        : widget;
  }
}
