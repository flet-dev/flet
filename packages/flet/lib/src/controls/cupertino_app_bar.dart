import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/overlay_style.dart';
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

    var bar = CupertinoNavigationBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
          : null,
      automaticallyImplyLeading:
          control.attrBool("automaticallyImplyLeading", true)!,
      automaticallyImplyMiddle:
          control.attrBool("automaticallyImplyMiddle", true)!,
      transitionBetweenRoutes:
          control.attrBool("transitionBetweenRoutes", true)!,
      border: parseBorder(Theme.of(context), control, "border"),
      previousPageTitle: control.attrString("previousPageTitle"),
      padding: parseEdgeInsetsDirectional(control, "padding"),
      backgroundColor: control.attrColor("bgcolor", context),
      automaticBackgroundVisibility:
          control.attrBool("automaticBackgroundVisibility", true)!,
      enableBackgroundFilterBlur:
          control.attrBool("backgroundFilterBlur", true)!,
      brightness: parseBrightness(control.attrString("brightness")),
      middle: middleCtrls.isNotEmpty
          ? createControl(control, middleCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
          : null,
      trailing: trailingCtrls.length == 1
          ? createControl(control, trailingCtrls.first.id, control.isDisabled,
              parentAdaptive: parentAdaptive)
          : trailingCtrls.length > 1
              ? Row(
                  mainAxisSize: MainAxisSize.min,
                  children: trailingCtrls
                      .map((c) => createControl(
                          control, c.id, control.isDisabled,
                          parentAdaptive: parentAdaptive))
                      .toList(),
                )
              : null,
    );
    return baseControl(context, bar, parent, control);
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
