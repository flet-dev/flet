import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../widgets/adjustable_scroll_controller.dart';
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
    final maxExtent = control.attrDouble("maxExtent");
    final spacing = control.attrDouble("spacing", 10)!;
    final runSpacing = control.attrDouble("runSpacing", 10)!;
    final padding = parseEdgeInsets(control, "padding");
    final childAspectRatio = control.attrDouble("childAspectRatio", 1)!;

    List<Control> visibleControls = children.where((c) => c.isVisible).toList();

    var gridView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint("GridView constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint("GridView constraints.maxHeight: ${constraints.maxHeight}");

        var shrinkWrap =
            (!horizontal && constraints.maxHeight == double.infinity) ||
                (horizontal && constraints.maxWidth == double.infinity);

        var gridDelegate = maxExtent == null
            ? SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: runsCount,
                mainAxisSpacing: spacing,
                crossAxisSpacing: runSpacing,
                childAspectRatio: childAspectRatio)
            : SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: maxExtent,
                mainAxisSpacing: spacing,
                crossAxisSpacing: runSpacing,
                childAspectRatio: childAspectRatio);

        return GridView.builder(
          scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
          controller: isWindowsDesktop() ? AdjustableScrollController() : null,
          shrinkWrap: shrinkWrap,
          padding: padding,
          gridDelegate: gridDelegate,
          itemCount: visibleControls.length,
          itemBuilder: (context, index) {
            return createControl(control, visibleControls[index].id, disabled);
          },
        );
      },
    );

    return constrainedControl(context, gridView, parent, control);
  }
}
