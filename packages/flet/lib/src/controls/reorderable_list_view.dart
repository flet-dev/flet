import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/keys.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../widgets/reorderable_item_scope.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ReorderableListViewControl extends StatefulWidget {
  final Control control;

  ReorderableListViewControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<ReorderableListViewControl> createState() => _ListViewControlState();
}

class _ListViewControlState extends State<ReorderableListViewControl> {
  late final ScrollController _controller;
  List<Control> _controls = [];

  Widget _buildItem(int index) {
    final control = _controls[index];
    final keyValue = control.getKey("key")?.value ?? control.id;
    return ReorderableItemScope(
      key: ValueKey(keyValue),
      index: index,
      child: ControlWidget(
        key: ValueKey(keyValue),
        control: control,
      ),
    );
  }

  Widget _buildPrototypeItem() {
    final control = _controls[0];
    return ReorderableItemScope(
      index: 0,
      child: ControlWidget(
        key: ValueKey(control.id),
        control: control,
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    _controller = ScrollController();
    _controls = [...widget.control.children("controls")];
  }

  @override
  void didUpdateWidget(covariant ReorderableListViewControl oldWidget) {
    _controls = [...widget.control.children("controls")];
    super.didUpdateWidget(oldWidget);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ReorderableListViewControl build: ${widget.control.id}");

    var horizontal = widget.control.getBool("horizontal", false)!;
    var buildControlsOnDemand =
        widget.control.getBool("build_controls_on_demand", true)!;
    var itemExtent = widget.control.getDouble("item_extent");
    var cacheExtent = widget.control.getDouble("cache_extent");
    var firstItemPrototype =
        widget.control.getBool("first_item_prototype", false)!;
    var padding = widget.control.getPadding("padding");
    var reverse = widget.control.getBool("reverse", false)!;
    var showDefaultDragHandles =
        widget.control.getBool("show_default_drag_handles", true)!;
    var anchor = widget.control.getDouble("anchor", 0.0)!;
    var clipBehavior =
        widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!;
    var scrollDirection = horizontal ? Axis.horizontal : Axis.vertical;
    var header = widget.control.buildWidget("header");
    var footer = widget.control.buildWidget("footer");
    var prototypeItem = firstItemPrototype && _controls.isNotEmpty
        ? _buildPrototypeItem()
        : null;
    var autoScrollerVelocityScalar =
        widget.control.getDouble("auto_scroller_velocity_scalar");
    var mouseCursor = widget.control.getMouseCursor("mouse_cursor");

    void onReorder(int oldIndex, int newIndex) {
      setState(() {
        if (oldIndex < newIndex) {
          newIndex -= 1;
        }
        final item = _controls.removeAt(oldIndex);
        _controls.insert(newIndex, item);
      });
      widget.control.triggerEvent(
          "reorder", {"old_index": oldIndex, "new_index": newIndex});
    }

    void onReorderEnd(int newIndex) {
      widget.control.triggerEvent("reorder_end", {"new_index": newIndex});
    }

    void onReorderStart(int oldIndex) {
      widget.control.triggerEvent("reorder_start", {"old_index": oldIndex});
    }

    Widget result = LayoutBuilder(
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
                buildDefaultDragHandles: showDefaultDragHandles,
                scrollDirection: scrollDirection,
                shrinkWrap: shrinkWrap,
                padding: padding,
                itemCount: _controls.length,
                itemExtent: itemExtent,
                mouseCursor: mouseCursor,
                anchor: anchor,
                header: header,
                footer: footer,
                prototypeItem: prototypeItem,
                autoScrollerVelocityScalar: autoScrollerVelocityScalar,
                onReorder: onReorder,
                onReorderEnd: onReorderEnd,
                onReorderStart: onReorderStart,
                itemBuilder: (context, index) {
                  return _buildItem(index);
                },
              )
            : ReorderableListView(
                scrollController: _controller,
                cacheExtent: cacheExtent,
                reverse: reverse,
                clipBehavior: clipBehavior,
                buildDefaultDragHandles: showDefaultDragHandles,
                scrollDirection: scrollDirection,
                shrinkWrap: shrinkWrap,
                padding: padding,
                anchor: anchor,
                header: header,
                footer: footer,
                itemExtent: itemExtent,
                mouseCursor: mouseCursor,
                prototypeItem: prototypeItem,
                autoScrollerVelocityScalar: autoScrollerVelocityScalar,
                onReorder: onReorder,
                onReorderEnd: onReorderEnd,
                onReorderStart: onReorderStart,
                children: List.generate(_controls.length, _buildItem),
              );

        child = ScrollableControl(
            control: widget.control,
            scrollDirection: scrollDirection,
            scrollController: _controller,
            child: child);

        if (widget.control.getBool("on_scroll", false)!) {
          child =
              ScrollNotificationControl(control: widget.control, child: child);
        }

        return child;
      },
    );

    return LayoutControl(control: widget.control, child: result);
  }
}
