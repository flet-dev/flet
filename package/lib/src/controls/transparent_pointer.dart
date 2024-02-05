import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

import '../models/control.dart';
import 'create_control.dart';

class TransparentPointerControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const TransparentPointerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("TransparentPointer build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        context,
        TransparentPointer(
            transparent: true,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled,
                    parentAdaptive: parentAdaptive)
                : null),
        parent,
        control);
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
