import 'package:flet/src/utils/edge_insets.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import 'base_controls.dart';

class AppBarControl extends StatelessWidget implements PreferredSizeWidget {
  final Control control;

  const AppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    var appBar = AppBar(
      leading: control.buildWidget("leading"),
      leadingWidth: control.getDouble("leading_width"),
      automaticallyImplyLeading:
          control.getBool("automatically_imply_leading", true)!,
      title: control.buildTextOrWidget("title"),
      centerTitle: control.getBool("center_title"),
      toolbarHeight: preferredSize.height,
      foregroundColor: control.getColor("color", context),
      backgroundColor: control.getColor("bgcolor", context),
      elevation: control.getDouble("elevation"),
      actions: control.buildWidgets("actions"),
      systemOverlayStyle: Theme.of(context)
          .extension<SystemUiOverlayStyleTheme>()
          ?.systemUiOverlayStyle,
      shadowColor: control.getColor("shadow_color", context),
      scrolledUnderElevation: control.getDouble("elevation_on_scroll"),
      forceMaterialTransparency:
          control.getBool("force_material_transparency", false)!,
      primary: !control.getBool("secondary", false)!,
      titleSpacing: control.getDouble("title_spacing"),
      excludeHeaderSemantics:
          control.getBool("exclude_header_semantics", false)!,
      clipBehavior: control.getClipBehavior("clip_behavior"),
      titleTextStyle:
          control.getTextStyle("title_text_style", Theme.of(context)),
      shape: control.getShape("shape", Theme.of(context)),
      toolbarOpacity: control.getDouble("toolbar_opacity", 1)!,
      toolbarTextStyle:
          control.getTextStyle("toolbar_text_style", Theme.of(context)),
      actionsPadding: control.getPadding("actions_padding"),
    );

    return BaseControl(control: control, child: appBar);
  }

  @override
  Size get preferredSize =>
      Size.fromHeight(control.getDouble("toolbar_height", kToolbarHeight)!);
}
