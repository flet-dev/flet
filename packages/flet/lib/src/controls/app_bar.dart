import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'cupertino_app_bar.dart';
import 'flet_store_mixin.dart';

class AppBarControl extends StatelessWidget
    with FletStoreMixin
    implements PreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final double height;

  const AppBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.height});

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive = control.getBool("adaptive") ?? parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoAppBarControl(
            control: control,
            parentDisabled: parentDisabled,
            parentAdaptive: adaptive,
            children: children);
      }

      var leadingCtrls =
          children.where((c) => c.name == "leading" && c.visible);
      var titleCtrls = children.where((c) => c.name == "title" && c.visible);
      var actionCtrls = children.where((c) => c.name == "action" && c.visible);
      var isSecondary = control.getBool("isSecondary", false)!;

      var appBar = AppBar(
        leading: leadingCtrls.isNotEmpty
            ? createControl(control, leadingCtrls.first.id, control.disabled,
                parentAdaptive: adaptive)
            : null,
        leadingWidth: control.getDouble("leadingWidth"),
        automaticallyImplyLeading:
            control.getBool("automaticallyImplyLeading", true)!,
        title: titleCtrls.isNotEmpty
            ? createControl(control, titleCtrls.first.id, control.disabled,
                parentAdaptive: adaptive)
            : null,
        centerTitle: control.getBool("centerTitle", false)!,
        toolbarHeight: preferredSize.height,
        foregroundColor: control.getColor("color", context),
        backgroundColor: control.getColor("bgcolor", context),
        elevation: control.getDouble("elevation"),
        actions: actionCtrls
            .map((c) => createControl(control, c.id, control.disabled,
                parentAdaptive: adaptive))
            .toList(),
        systemOverlayStyle: Theme.of(context)
            .extension<SystemUiOverlayStyleTheme>()
            ?.systemUiOverlayStyle,
        shadowColor: control.getColor("shadowColor", context),
        surfaceTintColor: control.getColor("surfaceTintColor", context),
        scrolledUnderElevation: control.getDouble("elevationOnScroll"),
        forceMaterialTransparency:
            control.getBool("forceMaterialTransparency", false)!,
        primary: !isSecondary,
        titleSpacing: control.getDouble("titleSpacing"),
        excludeHeaderSemantics:
            control.getBool("excludeHeaderSemantics", false)!,
        clipBehavior: parseClip(control.getString("clipBehavior")),
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "titleTextStyle"),
        shape: parseOutlinedBorder(control, "shape"),
        toolbarOpacity: control.getDouble("toolbarOpacity", 1)!,
        toolbarTextStyle:
            parseTextStyle(Theme.of(context), control, "toolbarTextStyle"),
      );
      return baseControl(context, appBar, parent, control);
    });
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}
