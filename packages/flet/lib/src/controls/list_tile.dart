import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';

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
    return withPagePlatform((context, platform) {
      var leadingCtrl = control.child("leading");
      var titleCtrl = control.child("title");
      var subtitleCtrl = control.child("subtitle");
      var trailingCtrl = control.child("trailing");

      bool onclick = control.getBool("onclick", false)!;
      bool toggleInputs = control.getBool("toggle_inputs", false)!;
      bool onLongPressDefined = control.getBool("on_long_press", false)!;
      String url = control.getString("url", "")!;
      String? urlTarget = control.getString("url_target");

      Function()? onPressed = (onclick || toggleInputs || url != "") &&
              !control.disabled
          ? () {
              if (toggleInputs) {
                _clickNotifier.onClick();
              }
              if (url != "") {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              if (onclick) {
                FletBackend.of(context).triggerControlEvent(control, "click");
              }
            }
          : null;

      Function()? onLongPress = onLongPressDefined && !control.disabled
          ? () {
              FletBackend.of(context)
                  .triggerControlEvent(control, "long_press");
            }
          : null;

      Widget tile = ListTile(
        autofocus: control.getBool("autofocus", false)!,
        contentPadding: parseEdgeInsets(control, "content_padding"),
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
        mouseCursor: parseMouseCursor(control.getString("mouse_cursor")),
        visualDensity: parseVisualDensity(control.getString("visual_density")),
        shape: parseOutlinedBorder(control, "shape"),
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "title_text_style"),
        leadingAndTrailingTextStyle: parseTextStyle(
            Theme.of(context), control, "leading_and_trailing_text_style"),
        subtitleTextStyle:
            parseTextStyle(Theme.of(context), control, "subtitle_text_style"),
        titleAlignment:
            parseListTileTitleAlignment(control.getString("title_alignment")),
        style: parseListTileStyle(control.getString("style")),
        onFocusChange: (bool hasFocus) {
          FletBackend.of(context)
              .triggerControlEvent(control, hasFocus ? "focus" : "blur");
        },
        leading:
            leadingCtrl != null ? ControlWidget(control: leadingCtrl) : null,
        title: titleCtrl != null ? ControlWidget(control: titleCtrl) : null,
        subtitle:
            subtitleCtrl != null ? ControlWidget(control: subtitleCtrl) : null,
        trailing:
            trailingCtrl != null ? ControlWidget(control: trailingCtrl) : null,
      );

      if (toggleInputs) {
        tile = ListTileClicks(notifier: _clickNotifier, child: tile);
      }

      tile = Material(color: Colors.transparent, child: tile);

      return ConstrainedControl(control: control, child: tile);
    });
  }
}

class ListTileClickNotifier extends ChangeNotifier {
  void onClick() {
    notifyListeners();
  }
}
