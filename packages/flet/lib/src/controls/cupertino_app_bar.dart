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

    // "title" if coming from material AppBar
    var middle = control.buildTextOrWidget("middle") ??
        control.buildTextOrWidget("title");

    // "actions" if coming from material AppBar
    var trailing =
        control.buildWidget("trailing") ?? control.buildWidgets("actions");

    var bar = CupertinoNavigationBar(
        leading: control.buildWidget("leading"),
        automaticallyImplyLeading:
            control.getBool("automatically_imply_leading", true)!,
        automaticallyImplyMiddle:
            control.getBool("automatically_imply_middle", true)!,
        transitionBetweenRoutes:
            control.getBool("transition_between_routes", true)!,
        border: control.getBorder("border", Theme.of(context)),
        previousPageTitle: control.getString("previous_page_title"),
        padding: control.getEdgeInsetsDirectional("padding"),
        backgroundColor: control.getColor("bgcolor", context),
        automaticBackgroundVisibility:
            control.getBool("automatic_background_visibility", true)!,
        enableBackgroundFilterBlur:
            control.getBool("background_filter_blur", true)!,
        brightness: control.getBrightness("brightness"),
        middle: middle,
        trailing: trailing is Widget
            ? trailing
            : trailing is List<Widget>
                ? Row(
                    mainAxisSize: MainAxisSize.min,
                    children: trailing,
                  )
                : null);
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
