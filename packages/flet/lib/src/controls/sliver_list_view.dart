import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/others.dart';
import '../widgets/adjustable_scroll_controller.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class SliverListViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SliverListViewControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<SliverListViewControl> createState() => _SliverListViewControlState();
}

class _SliverListViewControlState extends State<SliverListViewControl> {
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
    debugPrint("SliverListViewControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    final horizontal = widget.control.attrBool("horizontal", false)!;
    final spacing = widget.control.attrDouble("spacing", 0)!;
    final dividerThickness = widget.control.attrDouble("dividerThickness", 0)!;
    final cacheExtent = widget.control.attrDouble("cacheExtent");
    var clipBehavior =
        parseClip(widget.control.attrString("clipBehavior"), Clip.hardEdge)!;

    List<Control> visibleControls =
        widget.children.where((c) => c.isVisible).toList();
    var scrollDirection = horizontal ? Axis.horizontal : Axis.vertical;

    Widget child = spacing > 0
        ? SliverList.separated(
            itemCount: widget.children.length,
            itemBuilder: (context, index) {
              return createControl(
                  widget.control, visibleControls[index].id, disabled,
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
                      : Divider(height: spacing, thickness: dividerThickness);
            },
          )
        : SliverList.builder(
            itemCount: widget.children.length,
            itemBuilder: (context, index) {
              return createControl(
                  widget.control, visibleControls[index].id, disabled,
                  parentAdaptive: adaptive);
            },
          );
    child = CustomScrollView(
      slivers: [child],
      cacheExtent: cacheExtent,
      clipBehavior: clipBehavior,
      scrollDirection: scrollDirection,
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

    return constrainedControl(context, child, widget.parent, widget.control);
  }
}
