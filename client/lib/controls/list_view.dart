import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

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

  final ScrollController _controller = ScrollController();

// This is what you're looking for!
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
    final padding = parseEdgeInsets(control, "padding");

    List<Control> visibleControls = children.where((c) => c.isVisible).toList();

    if (autoScroll) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollDown();
      });
    }

    return constrainedControl(
        spacing > 0
            ? ListView.separated(
                controller: _controller,
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                padding: padding,
                itemCount: children.length,
                itemBuilder: (context, index) {
                  return createControl(
                      control, visibleControls[index].id, disabled);
                },
                separatorBuilder: (context, index) {
                  return Divider(height: spacing);
                },
              )
            : ListView.builder(
                controller: _controller,
                scrollDirection: horizontal ? Axis.horizontal : Axis.vertical,
                padding: padding,
                itemCount: children.length,
                itemBuilder: (context, index) {
                  return createControl(
                      control, visibleControls[index].id, disabled);
                },
                prototypeItem: children.isNotEmpty
                    ? createControl(control, visibleControls[0].id, disabled)
                    : null,
              ),
        parent,
        control);
  }
}
