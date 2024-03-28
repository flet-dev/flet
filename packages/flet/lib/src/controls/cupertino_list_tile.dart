import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'list_tile.dart';

class CupertinoListTileControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;
  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  CupertinoListTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoListTile build: ${control.id}");

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
        ? createControl(control, additionalInfoCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;
    Widget? leading = leadingCtrls.isNotEmpty
        ? createControl(control, leadingCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    Widget? title = titleCtrls.isNotEmpty
        ? createControl(control, titleCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : const Text("");

    Widget? subtitle = subtitleCtrls.isNotEmpty
        ? createControl(control, subtitleCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    Widget? trailing = trailingCtrls.isNotEmpty
        ? createControl(control, trailingCtrls.first.id, disabled,
            parentAdaptive: parentAdaptive)
        : null;

    Color? backgroundColor = control.attrColor("bgcolor", context);
    Color? bgcolorActivated = control.attrColor("bgcolorActivated", context);

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
              backend.triggerControlEvent(control.id, "click");
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
            leadingSize: control.attrDouble("leadingSize", 30.0)!,
            leadingToTitle: control.attrDouble("leadingToTitle", 12.0)!,
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
