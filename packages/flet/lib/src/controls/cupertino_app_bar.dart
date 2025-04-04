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
    var large = control.attrBool("large", false)!;

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);

    // "middle" is deprecated in v0.27.0 and will be removed in v0.30.0, use "title" instead
    var titleCtrls = children
        .where((c) => (c.name == "title" || c.name == "middle") && c.isVisible);

    // if the material AppBar was used with adaptive=True, AppBar.actions[0] will be used as trailing control
    var trailingCtrls = children.where(
        (c) => (c.name == "trailing" || c.name == "action") && c.isVisible);

    var leading = leadingCtrls.isNotEmpty
        ? createControl(control, leadingCtrls.first.id, control.isDisabled,
            parentAdaptive: parentAdaptive)
        : null;

    var automaticallyImplyLeading =
        control.attrBool("automaticallyImplyLeading", true)!;
    var automaticallyImplyTitle =
        control.attrBool("automaticallyImplyTitle", control.attrBool("automaticallyImplyMiddle", true)!)!;
    var transitionBetweenRoutes =
        control.attrBool("transitionBetweenRoutes", true)!;
    var border = parseBorder(Theme.of(context), control, "border");
    var previousPageTitle = control.attrString("previousPageTitle");
    var padding = parseEdgeInsetsDirectional(control, "padding");
    var backgroundColor = control.attrColor("bgcolor", context);
    var automaticBackgroundVisibility =
        control.attrBool("automaticBackgroundVisibility", true)!;
    var enableBackgroundFilterBlur =
        control.attrBool("backgroundFilterBlur", true)!;
    var brightness = parseBrightness(control.attrString("brightness"));
    var title = titleCtrls.isNotEmpty
        ? createControl(control, titleCtrls.first.id, control.isDisabled,
            parentAdaptive: parentAdaptive)
        : null;
    var trailing = trailingCtrls.length == 1
        ? createControl(control, trailingCtrls.first.id, control.isDisabled,
            parentAdaptive: parentAdaptive)
        : trailingCtrls.length > 1
            ? Row(
                mainAxisSize: MainAxisSize.min,
                children: trailingCtrls
                    .map((c) => createControl(control, c.id, control.isDisabled,
                        parentAdaptive: parentAdaptive))
                    .toList(),
              )
            : null;

    var bar = large
        ? CupertinoNavigationBar.large(
            leading: leading,
            automaticallyImplyLeading: automaticallyImplyLeading,
            transitionBetweenRoutes: transitionBetweenRoutes,
            border: border,
            previousPageTitle: previousPageTitle,
            padding: padding,
            backgroundColor: backgroundColor,
            automaticBackgroundVisibility: automaticBackgroundVisibility,
            enableBackgroundFilterBlur: enableBackgroundFilterBlur,
            brightness: brightness,
            trailing: trailing,
            largeTitle: title,
            automaticallyImplyTitle: automaticallyImplyTitle,
          )
        : CupertinoNavigationBar(
            leading: leading,
            automaticallyImplyLeading: automaticallyImplyLeading,
            automaticallyImplyMiddle: automaticallyImplyTitle,
            transitionBetweenRoutes: transitionBetweenRoutes,
            border: border,
            previousPageTitle: previousPageTitle,
            padding: padding,
            backgroundColor: backgroundColor,
            automaticBackgroundVisibility: automaticBackgroundVisibility,
            enableBackgroundFilterBlur: enableBackgroundFilterBlur,
            brightness: brightness,
            middle: title,
            trailing: trailing,
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
