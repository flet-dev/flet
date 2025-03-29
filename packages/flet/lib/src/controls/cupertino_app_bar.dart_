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

    var leadingCtrls = children.where((c) => c.name == "leading" && c.visible);

    // if the material AppBar was used with adaptive=True, AppBar.title will be used as middle control
    var middleCtrls = children
        .where((c) => (c.name == "middle" || c.name == "title") && c.visible);

    // if the material AppBar was used with adaptive=True, AppBar.actions[0] will be used as trailing control
    var trailingCtrls = children.where(
        (c) => (c.name == "trailing" || c.name == "action") && c.visible);

    var bar = CupertinoNavigationBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.disabled,
              parentAdaptive: parentAdaptive)
          : null,
      automaticallyImplyLeading:
          control.getBool("automaticallyImplyLeading", true)!,
      automaticallyImplyMiddle:
          control.getBool("automaticallyImplyMiddle", true)!,
      transitionBetweenRoutes:
          control.getBool("transitionBetweenRoutes", true)!,
      border: parseBorder(Theme.of(context), control, "border"),
      previousPageTitle: control.getString("previousPageTitle"),
      padding: parseEdgeInsetsDirectional(control, "padding"),
      backgroundColor: control.getColor("bgcolor", context),
      automaticBackgroundVisibility:
          control.getBool("automaticBackgroundVisibility", true)!,
      enableBackgroundFilterBlur:
          control.getBool("backgroundFilterBlur", true)!,
      brightness: parseBrightness(control.getString("brightness")),
      middle: middleCtrls.isNotEmpty
          ? createControl(control, middleCtrls.first.id, control.disabled,
              parentAdaptive: parentAdaptive)
          : null,
      trailing: trailingCtrls.length == 1
          ? createControl(control, trailingCtrls.first.id, control.disabled,
              parentAdaptive: parentAdaptive)
          : trailingCtrls.length > 1
              ? Row(
                  mainAxisSize: MainAxisSize.min,
                  children: trailingCtrls
                      .map((c) => createControl(control, c.id, control.disabled,
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
            control.getColor("bgcolor", context), context) ??
        CupertinoTheme.of(context).barBackgroundColor;
    return backgroundColor.alpha == 0xFF;
  }
}
