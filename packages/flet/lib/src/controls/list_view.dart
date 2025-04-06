import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/misc.dart';
import 'base_controls.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ListViewControl extends StatefulWidget {
  final Control control;

  const ListViewControl({
    super.key,
    required this.control,
  });

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
    var horizontal = widget.control.getBool("horizontal", false)!;
    var spacing = widget.control.getDouble("spacing", 0)!;
    var dividerThickness = widget.control.getDouble("divider_thickness", 0)!;
    var itemExtent = widget.control.getDouble("item_extent");
    var cacheExtent = widget.control.getDouble("cache_extent");
    var semanticChildCount = widget.control.getInt("semantic_child_count");
    var padding = widget.control.getEdgeInsets("padding");
    var reverse = widget.control.getBool("reverse", false)!;
    var clipBehavior =
        parseClip(widget.control.getString("clip_behavior"), Clip.hardEdge)!;
    var scrollDirection = horizontal ? Axis.horizontal : Axis.vertical;
    var buildControlsOnDemand =
        widget.control.getBool("build_controls_on_demand", true)!;
    var firstItemPrototype =
        widget.control.getBool("first_item_prototype", false)!;
    var prototypeItem = firstItemPrototype
        ? widget.control.buildWidget("prototype_item")
        : null;
    List<Widget> controls = widget.control.buildWidgets("controls");

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
                children: controls,
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
                    itemCount: controls.length,
                    itemBuilder: (context, index) {
                      return controls[index];
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
                    itemCount: controls.length,
                    itemExtent: itemExtent,
                    itemBuilder: (context, index) {
                      return controls[index];
                    },
                    prototypeItem: prototypeItem,
                  );

        child = ScrollableControl(
            control: widget.control,
            scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
            scrollController: _controller,
            child: child);

        if (widget.control.getBool("on_scroll", false)!) {
          child =
              ScrollNotificationControl(control: widget.control, child: child);
        }

        return child;
      },
    );

    return ConstrainedControl(control: widget.control, child: listView);
  }
}
