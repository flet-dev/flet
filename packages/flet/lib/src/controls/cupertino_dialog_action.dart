import 'package:flet/src/flet_backend.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

//import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/text.dart';
import 'base_controls.dart';
import 'control_widget.dart';
//import 'create_control.dart';

class CupertinoDialogActionControl extends StatelessWidget {
  //final Control? parent;
  final Control control;
  //final List<Control> children;
  //final bool parentDisabled;
  //final bool? parentAdaptive;
  //final FletControlBackend backend;

  const CupertinoDialogActionControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.children,
    //required this.parentDisabled,
    //required this.parentAdaptive,
    //required this.backend,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${control.id}");
    //bool disabled = control.disabled || parentDisabled;
    bool disabled = control.disabled || control.parent!.disabled;
    //var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    var content = control.child("content");

    Widget child;
    if (content is Control) {
      child = ControlWidget(control: content);
    } else {
      child = Text(control.getString("text", "")!);
    }

    var cupertinoDialogAction = CupertinoDialogAction(
      isDefaultAction: control.getBool("isDefaultAction", false)!,
      isDestructiveAction: control.getBool("isDestructiveAction", false)!,
      textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
      onPressed: !disabled
          ? () {
              debugPrint("CupertinoDialogAction ${control.id} clicked!");
              FletBackend.of(context).triggerControlEvent(control, "click");
            }
          : null,
      child: child,
    );

    return BaseControl(control: control, child: cupertinoDialogAction);
  }
}
