import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../widgets/adjustable_scroll_controller.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ListViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final dynamic dispatch;

  const ListViewControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<ListViewControl> createState() => _ListViewControlState();
}

class _ListViewControlState extends State<ListViewControl> {
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
    debugPrint("ListViewControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    final horizontal = widget.control.attrBool("horizontal", false)!;
    final spacing = widget.control.attrDouble("spacing", 0)!;
    final dividerThickness = widget.control.attrDouble("dividerThickness", 0)!;
    final itemExtent = widget.control.attrDouble("itemExtent");
    final firstItemPrototype =
        widget.control.attrBool("firstItemPrototype", false)!;
    final padding = parseEdgeInsets(widget.control, "padding");

    List<Control> visibleControls =
        widget.children.where((c) => c.isVisible).toList();

    Widget listView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint("ListView constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint("ListView constraints.maxHeight: ${constraints.maxHeight}");

        var shrinkWrap =
            (!horizontal && constraints.maxHeight == double.infinity) ||
                (horizontal && constraints.maxWidth == double.infinity);

        Widget child = spacing > 0
            ? ListView.separated(
                controller: _controller,
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                shrinkWrap: shrinkWrap,
                padding: padding,
                itemCount: widget.children.length,
                itemBuilder: (context, index) {
                  return createControl(
                      widget.control, visibleControls[index].id, disabled);
                },
                separatorBuilder: (context, index) {
                  return horizontal
                      ? dividerThickness == 0
                          ? SizedBox(width: spacing)
                          : VerticalDivider(
                              width: spacing, thickness: dividerThickness)
                      : dividerThickness == 0
                          ? SizedBox(height: spacing)
                          : Divider(
                              height: spacing, thickness: dividerThickness);
                },
              )
            : ListView.builder(
                controller: _controller,
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                shrinkWrap: shrinkWrap,
                padding: padding,
                itemCount: widget.children.length,
                itemExtent: itemExtent,
                itemBuilder: (context, index) {
                  return createControl(
                      widget.control, visibleControls[index].id, disabled);
                },
                prototypeItem: firstItemPrototype && widget.children.isNotEmpty
                    ? createControl(
                        widget.control, visibleControls[0].id, disabled)
                    : null,
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

    return constrainedControl(context, listView, widget.parent, widget.control);
  }
}
