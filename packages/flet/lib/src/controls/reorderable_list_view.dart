import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ReorderableListViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const ReorderableListViewControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<ReorderableListViewControl> createState() => _ListViewControlState();
}

class _ListViewControlState extends State<ReorderableListViewControl> {
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

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var horizontal = widget.control.attrBool("horizontal", false)!;
    var buildControlsOnDemand =
        widget.control.attrBool("buildControlsOnDemand", true)!;
    var itemExtent = widget.control.attrDouble("itemExtent");
    var cacheExtent = widget.control.attrDouble("cacheExtent");
    var firstItemPrototype =
        widget.control.attrBool("firstItemPrototype", false)!;
    var padding = parseEdgeInsets(widget.control, "padding");
    var reverse = widget.control.attrBool("reverse", false)!;
    var anchor = widget.control.attrDouble("anchor", 0.0)!;
    var clipBehavior =
        parseClip(widget.control.attrString("clipBehavior"), Clip.hardEdge)!;
    List<Control> ctrls = widget.children
        .where((c) => c.name != "header" && c.name != "footer" && c.isVisible)
        .toList();
    var scrollDirection = horizontal ? Axis.horizontal : Axis.vertical;
    var headerCtrls =
        widget.children.where((c) => c.name == "header" && c.isVisible);
    var header = headerCtrls.isNotEmpty
        ? createControl(widget.control, headerCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var footerCtrls =
        widget.children.where((c) => c.name == "footer" && c.isVisible);
    var footer = footerCtrls.isNotEmpty
        ? createControl(widget.control, footerCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;
    var prototypeItem = firstItemPrototype && widget.children.isNotEmpty
        ? createControl(widget.control, ctrls[0].id, disabled,
            parentAdaptive: adaptive)
        : null;
    var autoScrollerVelocityScalar =
        widget.control.attrDouble("autoScrollerVelocityScalar", 1.0);

    void onReorder(int oldIndex, int newIndex) {
      debugPrint("onReorder: $oldIndex -> $newIndex");
      if (newIndex > oldIndex) {
        newIndex -= 1;
      }
      setState(() {
        final Control movedControl = widget.children.removeAt(oldIndex);
        widget.children.insert(newIndex, movedControl);
      });
      widget.backend.triggerControlEvent(widget.control.id, "reorder",
          jsonEncode({"old": oldIndex, "new": newIndex}));
    }

    void onReorderEnd(int newIndex) {
      widget.backend.triggerControlEvent(
          widget.control.id, "reorder_end", jsonEncode({"new": newIndex}));
    }

    void onReorderStart(int oldIndex) {
      widget.backend.triggerControlEvent(
          widget.control.id, "reorder_start", jsonEncode({"old": oldIndex}));
    }

    Widget listView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        var shrinkWrap =
            (!horizontal && constraints.maxHeight == double.infinity) ||
                (horizontal && constraints.maxWidth == double.infinity);

        Widget child = buildControlsOnDemand
            ? ReorderableListView.builder(
                scrollController: _controller,
                clipBehavior: clipBehavior,
                reverse: reverse,
                cacheExtent: cacheExtent,
                scrollDirection: scrollDirection,
                shrinkWrap: shrinkWrap,
                padding: padding,
                buildDefaultDragHandles: false,
                itemCount: ctrls.length,
                itemExtent: itemExtent,
                anchor: anchor,
                header: header,
                footer: footer,
                prototypeItem: prototypeItem,
                autoScrollerVelocityScalar: autoScrollerVelocityScalar,
                onReorder: onReorder,
                onReorderEnd: onReorderEnd,
                onReorderStart: onReorderStart,
                itemBuilder: (context, index) {
                  return createControl(
                      widget.control, ctrls[index].id, disabled,
                      parentAdaptive: adaptive);
                },
              )
            : ReorderableListView(
                scrollController: _controller,
                cacheExtent: cacheExtent,
                reverse: reverse,
                clipBehavior: clipBehavior,
                scrollDirection: scrollDirection,
                shrinkWrap: shrinkWrap,
                padding: padding,
                anchor: anchor,
                header: header,
                footer: footer,
                itemExtent: itemExtent,
                prototypeItem: prototypeItem,
                autoScrollerVelocityScalar: autoScrollerVelocityScalar,
                onReorder: onReorder,
                onReorderEnd: onReorderEnd,
                onReorderStart: onReorderStart,
                children: ctrls.map((c) {
                  return createControl(widget.control, c.id, disabled,
                      parentAdaptive: adaptive);
                }).toList(),
              );

        child = ScrollableControl(
            control: widget.control,
            scrollDirection: scrollDirection,
            scrollController: _controller,
            backend: widget.backend,
            parentAdaptive: adaptive,
            child: child);

        if (widget.control.attrBool("onScroll", false)!) {
          child = ScrollNotificationControl(
              control: widget.control, backend: widget.backend, child: child);
        }

        return child;
      },
    );

    return constrainedControl(context, listView, widget.parent, widget.control);
  }
}
