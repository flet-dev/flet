import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ShaderMaskControl extends StatelessWidget {
  final Control control;

  const ShaderMaskControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShaderMask build: ${control.id}");
    var gradient = control.getGradient("shader", Theme.of(context));
    if (gradient == null) {
      return const ErrorControl("ShaderMask.shader must be provided");
    }
    final shaderMask = ShaderMask(
        shaderCallback: (bounds) => gradient.createShader(bounds),
        blendMode: control.getBlendMode("blend_mode", BlendMode.modulate)!,
        child: control.buildWidget("content"));
    return LayoutControl(
        control: control,
        child: _clipCorners(shaderMask,
            borderRadius: control.getBorderRadius("border_radius")));
  }

  Widget _clipCorners(Widget widget, {BorderRadius? borderRadius}) {
    return borderRadius != null
        ? ClipRRect(borderRadius: borderRadius, child: widget)
        : widget;
  }
}
