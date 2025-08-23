import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'base_controls.dart';

class TransparentPointerControl extends StatelessWidget {
  final Control control;

  const TransparentPointerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("TransparentPointer build: ${control.id}");

    var pointer = TransparentPointer(
        transparent: true, child: control.buildWidget("content"));

    return LayoutControl(control: control, child: pointer);
  }
}

// https://stackoverflow.com/questions/65269190/pass-trough-all-gestures-between-two-widgets-in-stack
class TransparentPointer extends SingleChildRenderObjectWidget {
  const TransparentPointer({
    super.key,
    this.transparent = true,
    super.child,
  });

  final bool transparent;

  @override
  RenderTransparentPointer createRenderObject(BuildContext context) {
    return RenderTransparentPointer(
      transparent: transparent,
    );
  }

  @override
  void updateRenderObject(
      BuildContext context, RenderTransparentPointer renderObject) {
    renderObject.transparent = transparent;
  }

  @override
  void debugFillProperties(DiagnosticPropertiesBuilder properties) {
    super.debugFillProperties(properties);
    properties.add(DiagnosticsProperty<bool>('transparent', transparent));
  }
}

class RenderTransparentPointer extends RenderProxyBox {
  RenderTransparentPointer({
    RenderBox? child,
    bool transparent = true,
  })  : _transparent = transparent,
        super(child);

  bool get transparent => _transparent;
  bool _transparent;

  set transparent(bool value) {
    if (value == _transparent) return;
    _transparent = value;
  }

  @override
  bool hitTest(BoxHitTestResult result, {required Offset position}) {
    // forward hits to our child:
    final hit = super.hitTest(result, position: position);
    // but report to our parent that we are not hit when `transparent` is true:
    return !transparent && hit;
  }

  @override
  void debugFillProperties(DiagnosticPropertiesBuilder properties) {
    super.debugFillProperties(properties);
    properties.add(DiagnosticsProperty<bool>('transparent', transparent));
  }
}
