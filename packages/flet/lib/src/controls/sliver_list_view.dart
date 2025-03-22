import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
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
  late final ScrollController _controller = ScrollController();

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

    final spacing = widget.control.attrDouble("spacing", 0)!;
    final dividerThickness = widget.control.attrDouble("dividerThickness", 0)!;
    List<Control> ctrls = widget.children.where((c) => c.isVisible).toList();
    var itemCount = ctrls.length;

    Widget child = spacing > 0
        ? SliverList.separated(
            itemCount: itemCount,
            itemBuilder: (context, index) {
              return createControl(widget.control, ctrls[index].id, disabled,
                  parentAdaptive: adaptive);
            },
            separatorBuilder: (context, index) {
              return dividerThickness == 0
                  ? SizedBox(height: spacing)
                  : Divider(height: spacing, thickness: dividerThickness);
            },
          )
        : SliverList.builder(
            itemCount: itemCount,
            itemBuilder: (context, index) {
              return createControl(widget.control, ctrls[index].id, disabled,
                  parentAdaptive: adaptive);
            },
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
