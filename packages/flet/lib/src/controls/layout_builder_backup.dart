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
  Size? _lastSize;
  bool _hasInitialized = false;
  bool _updateOnBuild = false;

  @override
  void initState() {
    super.initState();
    _updateOnBuild = widget.control.attrBool("update_on_build") ?? false;
  }

  void onChange(double width, double height) {
  widget.backend.updateControlState(widget.control.id, {"layoutWidth": width.toString()});
  widget.backend.updateControlState(widget.control.id, {"layoutHeight": height.toString()});

  widget.backend.triggerControlEvent(
    widget.control.id,
    "layout_change",
    jsonEncode({
      "height": height,
      "width": width,
    }),
  );

  setState(() {});
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
    
    var layoyt_ = LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            final Size currentSize =
                Size(constraints.maxWidth, constraints.maxHeight);
            if (_hasInitialized == false && _updateOnBuild == true) {
              onChange(constraints.maxWidth, constraints.maxHeight);
            }
            if (_hasInitialized == true && _lastSize != currentSize) {
              onChange(constraints.maxWidth, constraints.maxHeight);
            }
            _hasInitialized = true;

            _lastSize = currentSize;
            debugPrint(
                "LayoutBuilder dimensions: Width: ${constraints.maxWidth}, Height: ${constraints.maxHeight}");
          });

         return Container(
            clipBehavior: Clip.none,
            alignment: parseAlignment(widget.control, "alignment") ?? AlignmentDirectional.topStart,
            child: child
            );

        },
      );

    return constrainedControl(
      context,
      layoyt_,
      widget.parent,
      widget.control,
    );
  }
}
