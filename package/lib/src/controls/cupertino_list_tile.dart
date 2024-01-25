import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'list_tile.dart';

class CupertinoListTileControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  CupertinoListTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoListTile build: ${control.id}");

    final server = FletAppServices.of(context).server;

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
    var subtitleCtrls =
        children.where((c) => c.name == "subtitle" && c.isVisible);
    var trailingCtrls =
        children.where((c) => c.name == "trailing" && c.isVisible);
    var additionalInfoCtrls =
        children.where((c) => c.name == "additionalInfo" && c.isVisible);

    bool notched = control.attrBool("notched", false)!;
    bool onclick = control.attrBool("onclick", false)!;
    bool toggleInputs = control.attrBool("toggleInputs", false)!;
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    bool disabled = control.isDisabled || parentDisabled;

    Widget? additionalInfo = additionalInfoCtrls.isNotEmpty
        ? createControl(control, additionalInfoCtrls.first.id, disabled)
        : null;
    Widget? leading = leadingCtrls.isNotEmpty
        ? createControl(control, leadingCtrls.first.id, disabled)
        : null;

    Widget? title = titleCtrls.isNotEmpty
        ? createControl(control, titleCtrls.first.id, disabled)
        : const Text("");

    Widget? subtitle = subtitleCtrls.isNotEmpty
        ? createControl(control, subtitleCtrls.first.id, disabled)
        : null;

    Widget? trailing = trailingCtrls.isNotEmpty
        ? createControl(control, trailingCtrls.first.id, disabled)
        : null;

    Color? backgroundColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);
    Color? bgcolorActivated = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolorActivated", "")!);

    var padding = parseEdgeInsets(control, "contentPadding");

    Function()? onPressed = (onclick || toggleInputs || url != "") && !disabled
        ? () {
            debugPrint("CupertinoListTile ${control.id} clicked!");
            if (toggleInputs) {
              _clickNotifier.onClick();
            }
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            if (onclick) {
              server.sendPageEvent(
                  eventTarget: control.id, eventName: "click", eventData: "");
            }
          }
        : null;

    Widget tile;
    !notched
        ? tile = CupertinoListTile(
            onTap: onPressed,
            additionalInfo: additionalInfo,
            backgroundColor: backgroundColor,
            backgroundColorActivated: bgcolorActivated,
            leading: leading,
            leadingSize: control.attrDouble("leadingSize", 28.0)!,
            leadingToTitle: control.attrDouble("leadingToTitle", 16.0)!,
            padding: padding,
            title: title,
            subtitle: subtitle,
            trailing: trailing,
          )
        : tile = CupertinoListTile.notched(
            onTap: onPressed,
            additionalInfo: additionalInfo,
            backgroundColor: backgroundColor,
            backgroundColorActivated: bgcolorActivated,
            leading: leading,
            padding: padding,
            title: title,
            subtitle: subtitle,
            trailing: trailing,
          );

    if (toggleInputs) {
      tile = ListTileClicks(notifier: _clickNotifier, child: tile);
    }

    return constrainedControl(context, tile, parent, control);
  }
}
