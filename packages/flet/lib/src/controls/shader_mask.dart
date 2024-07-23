import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import 'create_control.dart';
import 'error.dart';

class ShaderMaskControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const ShaderMaskControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShaderMask build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var blendMode =
        parseBlendMode(control.attrString("blendMode"), BlendMode.modulate)!;
    bool disabled = control.isDisabled || parentDisabled;

    var gradient = parseGradient(Theme.of(context), control, "shader");
    if (gradient == null) {
      return const ErrorControl("ShaderMask.shader must be provided");
    }

    return constrainedControl(
        context,
        _clipCorners(
            ShaderMask(
                shaderCallback: (bounds) {
                  debugPrint("shaderCallback: $bounds, $gradient");
                  return gradient.createShader(bounds);
                },
                blendMode: blendMode,
                child: contentCtrls.isNotEmpty
                    ? createControl(control, contentCtrls.first.id, disabled,
                        parentAdaptive: parentAdaptive)
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
