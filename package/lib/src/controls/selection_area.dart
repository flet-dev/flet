import 'package:flutter/material.dart';
import '../models/control.dart';
import 'create_control.dart';

class SelectionAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SelectionAreaControl(
      {Key? key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("SelectionArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    //Widget child = contentCtrls.isNotEmpty
    //    ? createControl(control, contentCtrls.first.id, disabled)
    Widget child = createControl(control, contentCtrls.first.id, disabled);

    //var offsetDetails = parseOffset(control, "offset");

    // var bgColor = HexColor.fromString(
    //     Theme.of(context), control.attrString("bgColor", "")!);

    // var textColor = HexColor.fromString(
    //     Theme.of(context), control.attrString("textColor", "")!);

    // bool isLabelVisible = control.attrBool("isLabelVisible", true)!;
    // var largeSize = control.attrDouble("largeSize");
    // var smallSize = control.attrDouble("smallSize");

    return baseControl(
        context,
        SelectionArea(
          //label: label != null ? Text(label) : null,
          //isLabelVisible: isLabelVisible,
          // offset: offsetDetails != null
          //     ? Offset(offsetDetails.x, offsetDetails.y)
          //     : null,
          // alignment: parseAlignment(control, "alignment"),
          // backgroundColor: bgColor,
          // largeSize: largeSize,
          // padding: parseEdgeInsets(control, "padding"),
          // smallSize: smallSize,
          // textColor: textColor,
          // textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
          child: child,
        ),
        parent,
        control);
  }
}
