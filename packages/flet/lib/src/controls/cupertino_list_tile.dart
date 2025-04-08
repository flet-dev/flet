import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'list_tile.dart';

class CupertinoListTileControl extends StatelessWidget {
  final Control control;
  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  CupertinoListTileControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoListTile build: ${control.id}");

    var title = control.buildWidget("title");
    if (title == null) {
      return const ErrorControl(
          "CupertinoListTile.title must be provided and visible");
    }
    var leading = control.buildWidget("leading");
    var additionalInfo = control.buildWidget("additional_info");
    var subtitle = control.buildWidget("subtitle");
    var trailing = control.buildWidget("trailing");
    var backgroundColor = control.getColor("bgcolor", context);
    var bgcolorActivated = control.getColor("bgcolor_activated", context);
    var padding = control.getPadding("content_padding");
    var leadingSize = control.getDouble("leading_size");
    var leadingToTitle = control.getDouble("leading_to_title");
    var notched = control.getBool("notched", false)!;
    var onclick = control.getBool("on_click", false)!;
    var toggleInputs = control.getBool("toggle_inputs", false)!;
    var url = control.getString("url", "")!;
    var urlTarget = control.getString("url_target");

    Function()? onPressed =
        (onclick || toggleInputs || url != "") && !control.disabled
            ? () {
                if (toggleInputs) {
                  _clickNotifier.onClick();
                }
                if (url != "") {
                  openWebBrowser(url, webWindowName: urlTarget);
                }
                if (onclick) {
                  control.triggerEvent("click");
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
            leadingSize: leadingSize ?? 28.0,
            leadingToTitle: leadingToTitle ?? 16.0,
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
            leadingSize: leadingSize ?? 30.0,
            leadingToTitle: leadingToTitle ?? 12.0,
            padding: padding,
            title: title,
            subtitle: subtitle,
            trailing: trailing,
          );

    if (toggleInputs) {
      tile = ListTileClicks(notifier: _clickNotifier, child: tile);
    }

    return ConstrainedControl(control: control, child: tile);
  }
}
