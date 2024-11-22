import 'package:flutter/widgets.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import 'create_control.dart';
import '../flet_control_backend.dart';
import 'flet_store_mixin.dart';
import 'dart:convert';

class LayoutBuilderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final FletControlBackend backend;

  const LayoutBuilderControl({
    super.key,
    this.parent,
    required this.control,
    required this.children,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
  });

  @override
  State<LayoutBuilderControl> createState() => _LayoutBuilderControlState();
}

class _LayoutBuilderControlState extends State<LayoutBuilderControl>
    with FletStoreMixin {
  final GlobalKey _widgetKey = GlobalKey();
  Size? _lastSize;
  bool _hasInitialized = false;
  bool _updateOnBuild = false;
  double xPosition = 0.0;
  double yPosition = 0.0;

  @override
  void initState() {
    super.initState();
    _updateOnBuild = widget.control.attrBool("update_on_build") ?? false;
    debugPrint("UPDATEEEEE ON BUUUUIIILLDD: $_updateOnBuild");
  }

  void onChange(double width, double height) {
    widget.backend.triggerControlEvent(
      widget.control.id,
      "layout_change",
      jsonEncode({
        "height": height,
        "width": width,
        "x_position": xPosition,
        "y_position": yPosition,
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Stack with layout builder build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive =
        widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    Widget? child = contentCtrls.isNotEmpty
        ? createControl(widget.control, contentCtrls.first.id, disabled,
            parentAdaptive: adaptive)
        : null;

    return constrainedControl(
      context,
      LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (_widgetKey.currentContext != null) {
              final RenderBox box =
                  _widgetKey.currentContext!.findRenderObject() as RenderBox;
              final Offset position = box.localToGlobal(Offset.zero);
              xPosition = position.dx;
              yPosition = position.dy;

              debugPrint("Widget position: x: $xPosition, y: $yPosition");
            }

            final Size currentSize =
                Size(constraints.maxWidth, constraints.maxHeight);
            if (_hasInitialized == false && _updateOnBuild == true) {
              onChange(constraints.maxWidth, constraints.maxHeight);
              debugPrint("ON CHANGE FIRST UPDATE!!!!!!!!!");
            }
            if (_hasInitialized == true && _lastSize != currentSize) {
              onChange(constraints.maxWidth, constraints.maxHeight);
              debugPrint("ON CHANGE SECONDDDDDDDDDD UPDATE!!!!!!!!!");
            }
            _hasInitialized = true;

            _lastSize = currentSize;
            debugPrint(
                "LayoutBuilder dimensions: Width: ${constraints.maxWidth}, Height: ${constraints.maxHeight}");
          });

          return Container(
            key: _widgetKey,
            clipBehavior: Clip.none,
            alignment: parseAlignment(widget.control, "alignment") ??
                AlignmentDirectional.topStart,
            child: child,
          );
        },
      ),
      widget.parent,
      widget.control,
    );
  }
}
