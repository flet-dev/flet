import 'package:flutter/widgets.dart';

import '../controls/control_widget.dart';
import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/layout.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class GridViewControl extends StatefulWidget {
  final Control control;

  GridViewControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<GridViewControl> createState() => _GridViewControlState();
}

class _GridViewControlState extends State<GridViewControl> {
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
    debugPrint("GridViewControl build: ${widget.control.id}");

    final horizontal = widget.control.getBool("horizontal", false)!;
    final runsCount = widget.control.getInt("runs_count", 1)!;
    final maxExtent = widget.control.getDouble("max_extent");
    final spacing = widget.control.getDouble("spacing", 10)!;
    final semanticChildCount = widget.control.getInt("semantic_child_count");
    final runSpacing = widget.control.getDouble("run_spacing", 10)!;
    final padding = widget.control.getPadding("padding");
    final childAspectRatio = widget.control.getDouble("child_aspect_ratio", 1)!;
    final reverse = widget.control.getBool("reverse", false)!;
    final cacheExtent = widget.control.getDouble("cache_extent");

    var clipBehavior =
        widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!;

    var gridView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        // debugPrint("GridView constraints.maxWidth: ${constraints.maxWidth}");
        // debugPrint("GridView constraints.maxHeight: ${constraints.maxHeight}");

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

        var buildControlsOnDemand =
            widget.control.getBool("build_controls_on_demand", true)!;
        Widget child = !buildControlsOnDemand
            ? GridView(
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                controller: _controller,
                clipBehavior: clipBehavior,
                reverse: reverse,
                cacheExtent: cacheExtent,
                semanticChildCount: semanticChildCount,
                shrinkWrap: shrinkWrap,
                padding: padding,
                gridDelegate: gridDelegate,
                children: widget.control.buildWidgets("controls"),
              )
            : GridView.builder(
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                controller: _controller,
                clipBehavior: clipBehavior,
                reverse: reverse,
                cacheExtent: cacheExtent,
                semanticChildCount: semanticChildCount,
                shrinkWrap: shrinkWrap,
                padding: padding,
                gridDelegate: gridDelegate,
                itemCount: widget.control.children("controls").length,
                itemBuilder: (context, index) {
                  return ControlWidget(
                      control: widget.control.children("controls")[index]);
                },
              );

        if (horizontal &&
            constraints.maxHeight == double.infinity &&
            widget.control.getDouble("height") == null &&
            widget.control.getExpand("expand", 0)! <= 0) {
          return const ErrorControl(
              "Error displaying GridViewControl: height is unbounded.",
              description:
                  "Set a fixed height, a non-zero expand, or place inside "
                  "a control with bounded height.");
        }

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

    return LayoutControl(control: widget.control, child: gridView);
  }
}
