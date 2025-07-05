import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/theme.dart';
import 'base_controls.dart';

class CupertinoAppBarControl extends StatelessWidget
    implements ObstructingPreferredSizeWidget {
  final Control control;

  const CupertinoAppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoAppBar build: ${control.id}");

    var title = control.buildTextOrWidget("title");

    var leading = control.buildWidget("leading");
    var automaticallyImplyLeading =
        control.getBool("automatically_imply_leading", true)!;
    var automaticallyImplyTitle =
        control.getBool("automatically_imply_title", true)!;
    var transitionBetweenRoutes =
        control.getBool("transition_between_routes", true)!;
    var border = control.getBorder("border", Theme.of(context));
    var previousPageTitle = control.getString("previous_page_title");
    var padding = control.getEdgeInsetsDirectional("padding");
    var backgroundColor = control.getColor("bgcolor", context);
    var automaticBackgroundVisibility =
        control.getBool("automatic_background_visibility", true)!;
    var enableBackgroundFilterBlur =
        control.getBool("background_filter_blur", true)!;
    var brightness = control.getBrightness("brightness");

    // "actions" if coming from material AppBar
    var trailing =
        control.buildWidget("trailing") ?? control.buildWidgets("actions");
    var trailingWidget = trailing is Widget
        ? trailing
        : trailing is List<Widget>
            ? Row(mainAxisSize: MainAxisSize.min, children: trailing)
            : null;

    var bar = control.getBool("large", false)!
        ? CupertinoNavigationBar.large(
            leading: leading,
            automaticallyImplyLeading: automaticallyImplyLeading,
            automaticallyImplyTitle: automaticallyImplyTitle,
            transitionBetweenRoutes: transitionBetweenRoutes,
            border: border,
            previousPageTitle: previousPageTitle,
            padding: padding,
            backgroundColor: backgroundColor,
            automaticBackgroundVisibility: automaticBackgroundVisibility,
            enableBackgroundFilterBlur: enableBackgroundFilterBlur,
            brightness: brightness,
            largeTitle: title,
            trailing: trailingWidget)
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
            trailing: trailingWidget);

    return BaseControl(control: control, child: bar);
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
