import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class CupertinoAppBarControl extends StatelessWidget
    implements ObstructingPreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;

  const CupertinoAppBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAppBar build: ${control.id}");

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);

    // if the material AppBar was used with adaptive=True, AppBar.title will be used as middle control
    var middleCtrls = children
        .where((c) => (c.name == "middle" || c.name == "title") && c.isVisible);

    // if the material AppBar was used with adaptive=True, AppBar.actions[0] will be used as trailing control
    var trailingCtrls = children.where(
        (c) => (c.name == "trailing" || c.name == "action") && c.isVisible);

    var automaticallyImplyLeading =
        control.attrBool("automaticallyImplyLeading", true)!;
    var automaticallyImplyMiddle =
        control.attrBool("automaticallyImplyMiddle", true)!;
    var transitionBetweenRoutes =
        control.attrBool("transitionBetweenRoutes", true)!;
    var bgcolor = control.attrColor("bgcolor", context);

    return CupertinoNavigationBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
          : null,
      automaticallyImplyLeading: automaticallyImplyLeading,
      automaticallyImplyMiddle: automaticallyImplyMiddle,
      transitionBetweenRoutes: transitionBetweenRoutes,
      border: parseBorder(Theme.of(context), control, "border"),
      previousPageTitle: control.attrString("previousPageTitle"),
      padding: parseEdgeInsetsDirectional(control, "padding"),
      middle: middleCtrls.isNotEmpty
          ? createControl(control, middleCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
          : null,
      trailing: trailingCtrls.isNotEmpty
          ? createControl(control, trailingCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
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
    final Color backgroundColor = CupertinoDynamicColor.maybeResolve(
            control.attrColor("bgcolor", context), context) ??
        CupertinoTheme.of(context).barBackgroundColor;
    return backgroundColor.alpha == 0xFF;
  }
}
