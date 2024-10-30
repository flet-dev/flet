import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/others.dart';
import 'create_control.dart';
import '../flet_control_backend.dart';
import 'flet_store_mixin.dart';







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
    required this.backend
  
  });
  @override
  State<LayoutBuilderControl> createState() => _LayoutBuilderControlState();
}

class _LayoutBuilderControlState extends State<LayoutBuilderControl>
    with FletStoreMixin {


  void updateAttributes(double width,double height) {
    widget.backend.updateControlState(widget.control.id, {"widthLayout": width.toString()});
    widget.backend.updateControlState(widget.control.id, {"heightLayout": height.toString()});
  }


  @override
  Widget build(BuildContext context) {
    debugPrint("Stack with layout builder build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    bool? adaptive = widget.control.attrBool("adaptive") ?? widget.parentAdaptive;

    
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
          double containerWidth = constraints.maxWidth;
          double containerHeight = constraints.maxHeight;

          updateAttributes(containerWidth, containerHeight);

          debugPrint("LayoutBuilder dimensions: Width: $containerWidth, Height: $containerHeight");
         
          return Container(
            clipBehavior: Clip.none,
            alignment: parseAlignment(widget.control, "alignment") ?? AlignmentDirectional.topStart,
            child: child,
          );
        },
      ),
      widget.parent,
      widget.control,
    );
  }
}
