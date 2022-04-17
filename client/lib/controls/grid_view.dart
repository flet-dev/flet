import 'package:flutter/widgets.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class GridViewControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const GridViewControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("GridViewControl build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;

    final horizontal = control.attrBool("horizontal", false)!;
    final runsCount = control.attrInt("runsCount", 1)!;
    final spacing = control.attrDouble("spacing", 10)!;
    final runSpacing = control.attrDouble("runSpacing", 10)!;
    final padding = parseEdgeInsets(control, "padding");

    List<Widget> controls =
        children.map((c) => createControl(control, c.id, disabled)).toList();

    return constrainedControl(
        GridView.count(
          scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
          crossAxisCount: runsCount,
          mainAxisSpacing: spacing,
          crossAxisSpacing: runSpacing,
          padding: padding,
          children: controls,
        ),
        parent,
        control);
  }
}
