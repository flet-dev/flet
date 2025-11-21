import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/error.dart';

class BannerControl extends StatelessWidget {
  final Control control;

  const BannerControl({super.key, required this.control});

  MaterialBanner _createBanner(BuildContext context) {
    return MaterialBanner(
      leading: control.buildIconOrWidget("leading"),
      leadingPadding: control.getPadding("leading_padding"),
      content: control.buildTextOrWidget("content")!,
      padding: control.getPadding("content_padding"),
      actions: control.buildWidgets("actions"),
      forceActionsBelow: control.getBool("force_actions_below", false)!,
      backgroundColor: control.getColor("bgcolor", context),
      contentTextStyle:
          control.getTextStyle("content_text_style", Theme.of(context)),
      shadowColor: control.getColor("shadow_color", context),
      dividerColor: control.getColor("divider_color", context),
      elevation: control.getDouble("elevation"),
      minActionBarHeight: control.getDouble("min_action_bar_height", 52.0)!,
      margin: control.getMargin("margin"),
      onVisible: () {
        control.triggerEvent("visible");
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final dismissed = control.getBool("_dismissed", false)!;

    debugPrint("Banner build: ${control.id}, _dismissed=$dismissed");

    if (!dismissed) {
      final lastOpen = control.getBool("_open", false)!;
      var open = control.getBool("open", false)!;

      if (open && (open != lastOpen)) {
        if (control.get("content") == null) {
          return const ErrorControl(
              "Banner.content must be provided and visible");
        } else if (control.children("actions").isEmpty) {
          return const ErrorControl(
              "Banner.actions must be provided and at least one action should be visible");
        }

        control.updateProperties({"_open": open}, python: false);

        WidgetsBinding.instance.addPostFrameCallback((_) {
          ScaffoldMessenger.of(context).removeCurrentMaterialBanner();
          ScaffoldMessenger.of(context)
              .showMaterialBanner(_createBanner(context))
              .closed
              .then((reason) {
            debugPrint("Closing Banner(${control.id}) with reason: $reason");
            if (control.get("_dismissed") != true) {
              control.updateProperties({"_dismissed": true});
              debugPrint(
                  "Dismissing Banner(${control.id}) with reason: $reason");
              //_open = false;
              control.updateProperties({"_open": false}, python: false);
              control.updateProperties({"open": false});
              control.triggerEvent("dismiss");
            }
          });
        });
      } else if (!open && lastOpen) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          ScaffoldMessenger.of(context).hideCurrentMaterialBanner();
          control.updateProperties({"_open": false}, python: false);
        });
      }
    }
    return const SizedBox.shrink();
  }
}
