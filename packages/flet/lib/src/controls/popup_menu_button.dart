import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class PopupMenuButtonControl extends StatelessWidget {
  final Control control;

  const PopupMenuButtonControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("PopupMenuButton build: ${control.id}");

    var content = control.buildWidget("content");

    var popupMenuButton = PopupMenuButton<String>(
        enabled: !control.disabled,
        tooltip: null,
        icon: control.buildIconOrWidget("icon"),
        iconSize: control.getDouble("icon_size"),
        splashRadius: control.getDouble("splash_radius"),
        shadowColor: control.getColor("shadow_color", context),
        surfaceTintColor: control.getColor("surface_tint_color", context),
        iconColor: control.getColor("icon_color", context),
        elevation: control.getDouble("elevation"),
        enableFeedback: control.getBool("enable_feedback"),
        padding: control.getPadding("padding", const EdgeInsets.all(8))!,
        color: control.getColor("bgcolor", context),
        clipBehavior: control.getClipBehavior("clip_behavior", Clip.none)!,
        shape: control.getShape("shape", Theme.of(context),
            defaultValue: (Theme.of(context).useMaterial3
                ? RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10))
                : null))!,
        constraints: control.getBoxConstraints("size_constraints"),
        style: control.getButtonStyle("style", Theme.of(context)),
        popUpAnimationStyle: control.getAnimationStyle("popup_animation_style"),
        menuPadding: control.getPadding("menu_padding"),
        position: control.getPopupMenuPosition("menu_position"),
        onSelected: (String selection) =>
            control.triggerEvent("select", selection),
        onCanceled: () => control.triggerEvent("cancel"),
        onOpened: () => control.triggerEvent("open"),
        itemBuilder: (BuildContext context) => control
                .children("items")
                .where((i) => i.type == "PopupMenuItem")
                .map((item) {
              var itemIcon = item.getIcon("icon");
              var text = item.getString("text", "")!;
              var checked = item.getBool("checked");
              var height = item.getDouble("height", 48.0)!;
              var padding = item.getPadding("padding");
              var content = item.buildWidget("content");
              var mouseCursor = item.getMouseCursor("mouse_cursor");

              Widget? child;
              if (content != null) {
                // custom content
                child = content;
              } else if (itemIcon != null && text != "") {
                // icon and text
                child = Row(children: [
                  Icon(itemIcon),
                  const SizedBox(width: 8),
                  Text(text)
                ]);
              } else if (text != "") {
                child = Text(text);
              }

              var result = checked != null
                  ? CheckedPopupMenuItem<String>(
                      value: item.id.toString(),
                      checked: checked,
                      height: height,
                      padding: padding,
                      enabled: !item.disabled,
                      mouseCursor: mouseCursor,
                      onTap: () => item.triggerEvent("click", !checked),
                      child: child,
                    )
                  : PopupMenuItem<String>(
                      value: item.id.toString(),
                      height: height,
                      padding: padding,
                      enabled: !item.disabled,
                      mouseCursor: mouseCursor,
                      onTap: () {
                        item.triggerEvent("click");
                      },
                      child: child);

              return child != null
                  ? result
                  : const PopupMenuDivider() as PopupMenuEntry<String>;
            }).toList(),
        child: content);

    return ConstrainedControl(
        control: control,
        child: TooltipVisibility(
            visible: control.getString("tooltip") == null,
            child: popupMenuButton));
  }
}
