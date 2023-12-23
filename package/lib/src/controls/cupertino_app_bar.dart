import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class CupertinoAppBarControl extends StatelessWidget
    implements ObstructingPreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final Color? bgcolor;

  const CupertinoAppBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.bgcolor});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAppBar build: ${control.id}");

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var middleCtrls = children.where((c) => c.name == "middle" && c.isVisible);
    var trailingCtrls =
        children.where((c) => c.name == "trailing" && c.isVisible);

    var automaticallyImplyLeading =
        control.attrBool("automaticallyImplyLeading", true)!;
    var automaticallyImplyMiddle =
        control.attrBool("automaticallyImplyMiddle", true)!;
    var transitionBetweenRoutes =
        control.attrBool("transitionBetweenRoutes", true)!;
    var bgcolor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);

    return CupertinoNavigationBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.isDisabled)
          : null,
      automaticallyImplyLeading: automaticallyImplyLeading,
      automaticallyImplyMiddle: automaticallyImplyMiddle,
      transitionBetweenRoutes: transitionBetweenRoutes,
      border: parseBorder(Theme.of(context), control, "border"),
      previousPageTitle: control.attrString("previousPageTitle"),
      // padding: parseEdgeInsets(control, "padding"),
      middle: middleCtrls.isNotEmpty
          ? createControl(control, middleCtrls.first.id, control.isDisabled)
          : null,
      trailing: trailingCtrls.isNotEmpty
          ? createControl(control, trailingCtrls.first.id, control.isDisabled)
          : null,
      backgroundColor: bgcolor,
    );
  }

  @override
  Size get preferredSize {
    return const Size.fromHeight(44);
  }

  @override
  bool shouldFullyObstruct(BuildContext context) {
    final Color backgroundColor =
        CupertinoDynamicColor.maybeResolve(bgcolor, context) ??
            CupertinoTheme.of(context).barBackgroundColor;
    return backgroundColor.alpha == 0xFF;
  }
}
