import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class FlexibleSpaceBarControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;

  const FlexibleSpaceBarControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("FlexibleSpaceBar build: ${control.id}");

    bool? adaptive = control.isAdaptive ?? parentAdaptive;
    bool disabled = control.isDisabled || parentDisabled;

    var backgroundCtrl = children
        .where((c) => c.name == "background" && c.isVisible)
        .firstOrNull;
    var titleCtrl =
        children.where((c) => c.name == "title" && c.isVisible).firstOrNull;

    var bar = FlexibleSpaceBar(
      title: titleCtrl != null
          ? createControl(control, titleCtrl.id, disabled,
              parentAdaptive: adaptive)
          : null,
      background: backgroundCtrl != null
          ? createControl(control, backgroundCtrl.id, disabled,
              parentAdaptive: adaptive)
          : null,
      centerTitle: control.attrBool("centerTitle", false)!,
      expandedTitleScale: control.attrDouble("expandedTitleScale", 1.5)!,
      titlePadding: parseEdgeInsets(control, "titlePadding"),
      collapseMode: parseCollapseMode(
          control.attrString("collapseMode"), CollapseMode.parallax)!,
      //stretchModes: ,
    );
    return constrainedControl(context, bar, parent, control);
  }
}
