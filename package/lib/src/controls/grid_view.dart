import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../widgets/adjustable_scroll_controller.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class GridViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final dynamic dispatch;

  const GridViewControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<GridViewControl> createState() => _GridViewControlState();
}

class _GridViewControlState extends State<GridViewControl> {
  late final ScrollController _controller;

  @override
  void initState() {
    super.initState();
    _controller =
        isWindowsDesktop() ? AdjustableScrollController() : ScrollController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("GridViewControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    final horizontal = widget.control.attrBool("horizontal", false)!;
    final runsCount = widget.control.attrInt("runsCount", 1)!;
    final maxExtent = widget.control.attrDouble("maxExtent");
    final spacing = widget.control.attrDouble("spacing", 10)!;
    final runSpacing = widget.control.attrDouble("runSpacing", 10)!;
    final padding = parseEdgeInsets(widget.control, "padding");
    final childAspectRatio = widget.control.attrDouble("childAspectRatio", 1)!;
    final reverse = widget.control.attrBool("reverse", false)!;

    List<Control> visibleControls =
        widget.children.where((c) => c.isVisible).toList();

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

        Widget child = GridView.builder(
          scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
          controller: _controller,
          reverse: reverse,
          shrinkWrap: shrinkWrap,
          padding: padding,
          gridDelegate: gridDelegate,
          itemCount: visibleControls.length,
          itemBuilder: (context, index) {
            return createControl(
                widget.control, visibleControls[index].id, disabled);
          },
        );

        child = ScrollableControl(
          control: widget.control,
          scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
          dispatch: widget.dispatch,
          scrollController: _controller,
          child: child,
        );

        if (widget.control.attrBool("onScroll", false)!) {
          child =
              ScrollNotificationControl(control: widget.control, child: child);
        }

        return child;
      },
    );

    return constrainedControl(context, gridView, widget.parent, widget.control);
  }
}
