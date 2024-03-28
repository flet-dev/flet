import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
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

      var leadingWidth = control.attrDouble("leadingWidth");
      var elevation = control.attrDouble("elevation");
      var toolbarOpacity = control.attrDouble("toolbarOpacity", 1)!;
      var centerTitle = control.attrBool("centerTitle", false)!;
      var automaticallyImplyLeading =
          control.attrBool("automaticallyImplyLeading", true)!;
      var color = control.attrColor("color", context);
      var bgcolor = control.attrColor("bgcolor", context);
      var shadowColor = control.attrColor("shadowColor", context);
      var surfaceTintColor = control.attrColor("surfaceTintColor", context);
      var elevationOnScroll = control.attrDouble("elevationOnScroll");
      var forceMaterialTransparency =
          control.attrBool("forceMaterialTransparency", false)!;
      var isSecondary = control.attrBool("isSecondary", false)!;
      var excludeHeaderSemantics =
          control.attrBool("excludeHeaderSemantics", false)!;
      var titleSpacing = control.attrDouble("titleSpacing");

      var clipBehavior = Clip.values.firstWhereOrNull(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("clipBehavior", "")!.toLowerCase(),
      );

      return AppBar(
        leading: leadingCtrls.isNotEmpty
            ? createControl(control, leadingCtrls.first.id, control.isDisabled,
                parentAdaptive: adaptive)
            : null,
        leadingWidth: leadingWidth,
        automaticallyImplyLeading: automaticallyImplyLeading,
        title: titleCtrls.isNotEmpty
            ? createControl(control, titleCtrls.first.id, control.isDisabled,
                parentAdaptive: adaptive)
            : null,
        centerTitle: centerTitle,
        toolbarHeight: preferredSize.height,
        foregroundColor: color,
        backgroundColor: bgcolor,
        elevation: elevation,
        actions: actionCtrls
            .map((c) => createControl(control, c.id, control.isDisabled,
                parentAdaptive: adaptive))
            .toList(),
        systemOverlayStyle: Theme.of(context)
            .extension<SystemUiOverlayStyleTheme>()
            ?.systemUiOverlayStyle,
        shadowColor: shadowColor,
        surfaceTintColor: surfaceTintColor,
        scrolledUnderElevation: elevationOnScroll,
        forceMaterialTransparency: forceMaterialTransparency,
        primary: !isSecondary,
        titleSpacing: titleSpacing,
        excludeHeaderSemantics: excludeHeaderSemantics,
        clipBehavior: clipBehavior,
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "titleTextStyle"),
        shape: parseOutlinedBorder(control, "shape"),
        toolbarOpacity: toolbarOpacity,
        toolbarTextStyle:
            parseTextStyle(Theme.of(context), control, "toolbarTextStyle"),
      );
    });
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}
