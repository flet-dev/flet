import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ListViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const ListViewControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<ListViewControl> createState() => _ListViewControlState();
}

class _ListViewControlState extends State<ListViewControl> {
  late final ScrollController _controller;

  @override
  void initState() {
    super.initState();
    _controller = ScrollController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ListViewControl build: ${widget.control.id}");

    bool disabled = widget.control.disabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.getBool("adaptive") ?? widget.parentAdaptive;

    var horizontal = widget.control.getBool("horizontal", false)!;
    var spacing = widget.control.getDouble("spacing", 0)!;
    var dividerThickness = widget.control.getDouble("dividerThickness", 0)!;
    var itemExtent = widget.control.getDouble("itemExtent");
    var cacheExtent = widget.control.getDouble("cacheExtent");
    var semanticChildCount = widget.control.getInt("semanticChildCount");
    var firstItemPrototype =
        widget.control.getBool("firstItemPrototype", false)!;
    var padding = parseEdgeInsets(widget.control, "padding");
    var reverse = widget.control.getBool("reverse", false)!;
    var clipBehavior =
        parseClip(widget.control.getString("clipBehavior"), Clip.hardEdge)!;

    List<Control> ctrls = widget.children.where((c) => c.visible).toList();
    var scrollDirection = horizontal ? Axis.horizontal : Axis.vertical;
    var buildControlsOnDemand =
        widget.control.getBool("buildControlsOnDemand", true)!;
    var prototypeItem = firstItemPrototype && widget.children.isNotEmpty
        ? createControl(widget.control, ctrls[0].id, disabled,
            parentAdaptive: adaptive)
        : null;

    Widget listView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint("ListView constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint("ListView constraints.maxHeight: ${constraints.maxHeight}");

        var shrinkWrap =
            (!horizontal && constraints.maxHeight == double.infinity) ||
                (horizontal && constraints.maxWidth == double.infinity);
        Widget child = !buildControlsOnDemand
            ? ListView(
                controller: _controller,
                cacheExtent: cacheExtent,
                reverse: reverse,
                clipBehavior: clipBehavior,
                scrollDirection: scrollDirection,
                shrinkWrap: shrinkWrap,
                padding: padding,
                semanticChildCount: semanticChildCount,
                itemExtent: itemExtent,
                prototypeItem: prototypeItem,
                children: ctrls
                    .map((c) => createControl(widget.control, c.id, disabled,
                        parentAdaptive: adaptive))
                    .toList(),
              )
            : spacing > 0
                ? ListView.separated(
                    controller: _controller,
                    cacheExtent: cacheExtent,
                    reverse: reverse,
                    clipBehavior: clipBehavior,
                    scrollDirection: scrollDirection,
                    shrinkWrap: shrinkWrap,
                    padding: padding,
                    itemCount: widget.children.length,
                    itemBuilder: (context, index) {
                      return createControl(
                          widget.control, ctrls[index].id, disabled,
                          parentAdaptive: adaptive);
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
                    clipBehavior: clipBehavior,
                    semanticChildCount: semanticChildCount,
                    reverse: reverse,
                    cacheExtent: cacheExtent,
                    scrollDirection: scrollDirection,
                    shrinkWrap: shrinkWrap,
                    padding: padding,
                    itemCount: widget.children.length,
                    itemExtent: itemExtent,
                    itemBuilder: (context, index) {
                      return createControl(
                          widget.control, ctrls[index].id, disabled,
                          parentAdaptive: adaptive);
                    },
                    prototypeItem: prototypeItem,
                  );

        child = ScrollableControl(
            control: widget.control,
            scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
            scrollController: _controller,
            backend: widget.backend,
            parentAdaptive: adaptive,
            child: child);

        if (widget.control.getBool("onScroll", false)!) {
          child = ScrollNotificationControl(
              control: widget.control, backend: widget.backend, child: child);
        }

        return child;
      },
    );

    return constrainedControl(context, listView, widget.parent, widget.control);
  }
}
