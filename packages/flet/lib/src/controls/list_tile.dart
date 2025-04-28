import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class ListTileClicks extends InheritedWidget {
  const ListTileClicks({
    super.key,
    required this.notifier,
    required super.child,
  });

  final ListTileClickNotifier notifier;

  static ListTileClicks? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ListTileClicks>();
  }

  @override
  bool updateShouldNotify(ListTileClicks oldWidget) => true;
}

class ListTileControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  ListTileControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ListTile build: ${control.id}");
    var leading = control.buildWidget("leading");
    var title = control.buildWidget("title");
    var subtitle = control.buildWidget("subtitle");
    var trailing = control.buildWidget("trailing");
    var onClick = control.getBool("on_click", false)!;
    var toggleInputs = control.getBool("toggle_inputs", false)!;
    var url = control.getString("url");
    var urlTarget = control.getString("url_target");

    Function()? onPressed =
        (onClick || toggleInputs || url != "") && !control.disabled
            ? () {
                if (toggleInputs) {
                  _clickNotifier.onClick();
                }
                if (url != null) {
                  openWebBrowser(url, webWindowName: urlTarget);
                }
                if (onClick) {
                  control.triggerEvent("click");
                }
              }
            : null;

    Function()? onLongPress =
        control.getBool("on_long_press", false)! && !control.disabled
            ? () {
                control.triggerEvent("long_press");
              }
            : null;

    Widget tile = ListTile(
      autofocus: control.getBool("autofocus", false)!,
      contentPadding: control.getPadding("content_padding"),
      isThreeLine: control.getBool("is_three_line", false)!,
      selected: control.getBool("selected", false)!,
      dense: control.getBool("dense", false)!,
      onTap: onPressed,
      onLongPress: onLongPress,
      enabled: !control.disabled,
      horizontalTitleGap: control.getDouble("horizontal_spacing"),
      enableFeedback: control.getBool("enable_feedback"),
      minLeadingWidth: control.getDouble("min_leading_width"),
      minVerticalPadding: control.getDouble("min_vertical_padding"),
      minTileHeight: control.getDouble("min_height"),
      selectedTileColor: control.getColor("selected_tile_color", context),
      selectedColor: control.getColor("selected_color", context),
      focusColor: control.getColor("focus_color", context),
      tileColor: control.getColor("bgcolor", context),
      splashColor: control.getColor("bgcolor_activated", context),
      hoverColor: control.getColor("hover_color", context),
      iconColor: control.getColor("icon_color", context),
      textColor: control.getColor("text_color", context),
      mouseCursor: control.getMouseCursor("mouse_cursor"),
      visualDensity: control.getVisualDensity("visual_density"),
      shape: control.getShape("shape", Theme.of(context)),
      titleTextStyle:
          control.getTextStyle("title_text_style", Theme.of(context)),
      leadingAndTrailingTextStyle: control.getTextStyle(
          "leading_and_trailing_text_style", Theme.of(context)),
      subtitleTextStyle:
          control.getTextStyle("subtitle_text_style", Theme.of(context)),
      titleAlignment: control.getListTileTitleAlignment("title_alignment"),
      style: control.getListTileStyle("style"),
      onFocusChange: (bool hasFocus) {
        control.triggerEvent(hasFocus ? "focus" : "blur");
      },
      leading: leading,
      title: title,
      subtitle: subtitle,
      trailing: trailing,
    );

    if (toggleInputs) {
      tile = ListTileClicks(notifier: _clickNotifier, child: tile);
    }

    tile = Material(type: MaterialType.transparency, child: tile);

    return ConstrainedControl(control: control, child: tile);
  }
}

class ListTileClickNotifier extends ChangeNotifier {
  void onClick() {
    notifyListeners();
  }
}
