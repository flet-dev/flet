import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class AppBarControl extends StatelessWidget implements PreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final double height;

  const AppBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.height})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
    var actionCtrls = children.where((c) => c.name == "action" && c.isVisible);

    var leadingWidth = control.attrDouble("leadingWidth");
    var centerTitle = control.attrBool("centerTitle", false)!;
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    var bgcolor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);

    return AppBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.isDisabled)
          : null,
      leadingWidth: leadingWidth,
      title: titleCtrls.isNotEmpty
          ? createControl(control, titleCtrls.first.id, control.isDisabled)
          : null,
      centerTitle: centerTitle,
      toolbarHeight: preferredSize.height,
      foregroundColor: color,
      backgroundColor: bgcolor,
      actions: actionCtrls
          .map((c) => createControl(control, c.id, control.isDisabled))
          .toList(),
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}
