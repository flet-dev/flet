import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class SliverGridViewControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SliverGridViewControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<SliverGridViewControl> createState() => _SliverGridViewControlState();
}

class _SliverGridViewControlState extends State<SliverGridViewControl> {
  late final ScrollController _controller = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliverGridViewControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    final spacing = widget.control.attrDouble("spacing", 0)!;
    List<Control> ctrls = widget.children.where((c) => c.isVisible).toList();
    final maxExtent = widget.control.attrDouble("maxExtent");
    final runSpacing = widget.control.attrDouble("runSpacing", 10)!;
    final runsCount = widget.control.attrInt("runsCount", 1)!;
    final childAspectRatio = widget.control.attrDouble("childAspectRatio", 1)!;
    var buildControlsOnDemand =
        widget.control.attrBool("buildControlsOnDemand", true)!;

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

    Widget child = buildControlsOnDemand
        ? SliverGrid.builder(
            itemCount: widget.children.length,
            gridDelegate: gridDelegate,
            itemBuilder: (context, index) {
              return createControl(widget.control, ctrls[index].id, disabled,
                  parentAdaptive: adaptive);
            },
          )
        : SliverGrid(
            gridDelegate: gridDelegate,
            delegate: SliverChildBuilderDelegate(
              (context, index) => createControl(
                  widget.control, ctrls[index].id, disabled,
                  parentAdaptive: adaptive),
              childCount: ctrls.length,
            ),
          );
    child = ScrollableControl(
        control: widget.control,
        scrollDirection: Axis.vertical,
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
