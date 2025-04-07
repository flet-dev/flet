import 'package:flet/src/utils/borders.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/misc.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'cupertino_app_bar.dart';

class AppBarControl extends StatelessWidget
    with FletStoreMixin
    implements PreferredSizeWidget {
  final Control control;

  const AppBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive = control.adaptive ?? control.parent?.adaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoAppBarControl(control: control);
      }

      var appBar = AppBar(
        leading: control.buildWidget("leading"),
        leadingWidth: control.getDouble("leading_width"),
        automaticallyImplyLeading:
            control.getBool("automatically_imply_leading", true)!,
        title: control.buildWidget("title"),
        centerTitle: control.getBool("center_title", false)!,
        toolbarHeight: preferredSize.height,
        foregroundColor: control.getColor("color", context),
        backgroundColor: control.getColor("bgcolor", context),
        elevation: control.getDouble("elevation"),
        actions: control.buildWidgets("actions"),
        systemOverlayStyle: Theme.of(context)
            .extension<SystemUiOverlayStyleTheme>()
            ?.systemUiOverlayStyle,
        shadowColor: control.getColor("shadow_color", context),
        surfaceTintColor: control.getColor("surface_tint_color", context),
        scrolledUnderElevation: control.getDouble("elevation_on_scroll"),
        forceMaterialTransparency:
            control.getBool("force_material_transparency", false)!,
        primary: !control.getBool("isSecondary", false)!,
        titleSpacing: control.getDouble("title_spacing"),
        excludeHeaderSemantics:
            control.getBool("exclude_header_semantics", false)!,
        clipBehavior: control.getClipBehavior("clip_behavior"),
        titleTextStyle:
            control.getTextStyle("title_text_style", Theme.of(context)),
        shape: control.getShape("shape"),
        toolbarOpacity: control.getDouble("toolbar_opacity", 1)!,
        toolbarTextStyle: parseTextStyle(
            control.get("toolbar_text_style"), Theme.of(context)),
      );

      return BaseControl(control: control, child: appBar);
    });
  }

  @override
  Size get preferredSize => const Size.fromHeight(56);
}
