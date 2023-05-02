import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/desktop.dart';
import '../utils/edge_insets.dart';
import '../widgets/adjustable_scroll_controller.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';

class ListViewControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  ListViewControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  final ScrollController _controller =
      isWindowsDesktop() ? AdjustableScrollController() : ScrollController();

  void _scrollDown() {
    _controller.animateTo(
      _controller.position.maxScrollExtent,
      duration: const Duration(seconds: 1),
      curve: Curves.fastOutSlowIn,
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ListViewControl build: ${control.id}");

    bool disabled = control.isDisabled || parentDisabled;

    final horizontal = control.attrBool("horizontal", false)!;
    final autoScroll = control.attrBool("autoScroll", false)!;
    final spacing = control.attrDouble("spacing", 0)!;
    final dividerThickness = control.attrDouble("dividerThickness", 0)!;
    final itemExtent = control.attrDouble("itemExtent");
    final firstItemPrototype = control.attrBool("firstItemPrototype", false)!;
    final padding = parseEdgeInsets(control, "padding");

    List<Control> visibleControls = children.where((c) => c.isVisible).toList();

    if (autoScroll) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollDown();
      });
    }

    Widget listView = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint("ListView constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint("ListView constraints.maxHeight: ${constraints.maxHeight}");

        var shrinkWrap =
            (!horizontal && constraints.maxHeight == double.infinity) ||
                (horizontal && constraints.maxWidth == double.infinity);

        return spacing > 0
            ? ListView.separated(
                controller: _controller,
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                shrinkWrap: shrinkWrap,
                padding: padding,
                itemCount: children.length,
                itemBuilder: (context, index) {
                  return createControl(
                      control, visibleControls[index].id, disabled);
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
                itemCount: children.length,
                itemExtent: itemExtent,
                itemBuilder: (context, index) {
                  return createControl(
                      control, visibleControls[index].id, disabled);
                },
                prototypeItem: firstItemPrototype && children.isNotEmpty
                    ? createControl(control, visibleControls[0].id, disabled)
                    : null,
              );
      },
    );

    if (control.attrBool("onScroll", false)!) {
      listView = ScrollNotificationControl(control: control, child: listView);
    }

    return constrainedControl(context, listView, parent, control);
  }
}
