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
      bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;
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
          children.where((c) => c.name == "leading" && c.isVisible);
      var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
      var actionCtrls =
          children.where((c) => c.name == "action" && c.isVisible);
      var isSecondary = control.attrBool("isSecondary", false)!;

      var appBar = AppBar(
        leading: leadingCtrls.isNotEmpty
            ? createControl(control, leadingCtrls.first.id, control.isDisabled,
                parentAdaptive: adaptive)
            : null,
        leadingWidth: control.attrDouble("leadingWidth"),
        automaticallyImplyLeading:
            control.attrBool("automaticallyImplyLeading", true)!,
        title: titleCtrls.isNotEmpty
            ? createControl(control, titleCtrls.first.id, control.isDisabled,
                parentAdaptive: adaptive)
            : null,
        centerTitle: control.attrBool("centerTitle", false)!,
        toolbarHeight: preferredSize.height,
        foregroundColor: control.attrColor("color", context),
        backgroundColor: control.attrColor("bgcolor", context),
        elevation: control.attrDouble("elevation"),
        actions: actionCtrls
            .map((c) => createControl(control, c.id, control.isDisabled,
                parentAdaptive: adaptive))
            .toList(),
        systemOverlayStyle: Theme.of(context)
            .extension<SystemUiOverlayStyleTheme>()
            ?.systemUiOverlayStyle,
        shadowColor: control.attrColor("shadowColor", context),
        surfaceTintColor: control.attrColor("surfaceTintColor", context),
        scrolledUnderElevation: control.attrDouble("elevationOnScroll"),
        forceMaterialTransparency:
            control.attrBool("forceMaterialTransparency", false)!,
        primary: !isSecondary,
        titleSpacing: control.attrDouble("titleSpacing"),
        excludeHeaderSemantics:
            control.attrBool("excludeHeaderSemantics", false)!,
        clipBehavior: parseClip(control.attrString("clipBehavior")),
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "titleTextStyle"),
        shape: parseOutlinedBorder(control, "shape"),
        toolbarOpacity: control.attrDouble("toolbarOpacity", 1)!,
        toolbarTextStyle:
            parseTextStyle(Theme.of(context), control, "toolbarTextStyle"),
      );
      return baseControl(context, appBar, parent, control);
    });
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}
