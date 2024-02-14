import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/overlay_style.dart';
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
      var centerTitle = control.attrBool("centerTitle", false)!;
      var automaticallyImplyLeading =
          control.attrBool("automaticallyImplyLeading", true)!;
      var color = HexColor.fromString(
          Theme.of(context), control.attrString("color", "")!);
      var bgcolor = HexColor.fromString(
          Theme.of(context), control.attrString("bgcolor", "")!);
      var systemOverlayStyle = parseSystemOverlayStyle(
          Theme.of(context), control, "systemOverlayStyle");

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
        systemOverlayStyle: systemOverlayStyle,
      );
    });
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}
