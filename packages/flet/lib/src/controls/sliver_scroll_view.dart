import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/others.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class SliverScrollViewControl extends StatefulWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final FletControlBackend backend;

  const SliverScrollViewControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<SliverScrollViewControl> createState() =>
      _SliverScrollViewControlState();
}

class _SliverScrollViewControlState extends State<SliverScrollViewControl> {
  late final ScrollController _controller = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliverScrollView build: ${widget.control.id}");

    bool? adaptive = widget.control.isAdaptive ?? widget.parentAdaptive;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var ctrls = createControls(
            widget.control, widget.children.where((c) => c.isVisible), disabled,
            parentAdaptive: adaptive) ??
        const [];
    var scrollDirection = widget.control.attrBool("horizontal", false)!
        ? Axis.horizontal
        : Axis.vertical;

    Widget child = CustomScrollView(
      clipBehavior:
          parseClip(widget.control.attrString("clipBehavior"), Clip.hardEdge)!,
      reverse: widget.control.attrBool("reverse", false)!,
      scrollDirection: scrollDirection,
      shrinkWrap: widget.control.attrBool("shrinkWrap", false)!,
      semanticChildCount:
          widget.control.attrInt("semanticChildCount", ctrls.length),
      anchor: widget.control.attrDouble("anchor", 0.0)!,
      primary: widget.control.attrBool("primary"),
      cacheExtent: widget.control.attrDouble("cacheExtent"),
      slivers: ctrls,
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

    return baseControl(context, child, widget.parent, widget.control);
  }
}
