import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class AlignControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const AlignControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint('Align build : ${control.id}');

    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool('adaptive') ?? parentAdaptive;
    var contentCtrls =
        children.where((c) => c.name == 'content' && c.isVisible);
    var alignment = parseAlignment(control, 'alignment') ?? Alignment.center;
    Widget? child = contentCtrls.isNotEmpty
        ? createControl(control, contentCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;

    Widget result() {
      debugPrint('Alignmenttt ${parseAlignment(control, 'alignment')}');
      return Align(
        alignment: alignment,
        heightFactor: control.attrDouble('height_factor', null),
        widthFactor: control.attrDouble('width_factor', null),
        child: child,
      );
    }

    return constrainedControl(context, result(), parent, control);
  }
}
