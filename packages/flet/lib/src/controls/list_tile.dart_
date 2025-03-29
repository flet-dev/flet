import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import 'create_control.dart';
import 'cupertino_list_tile.dart';
import 'flet_store_mixin.dart';

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
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;
  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  ListTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("ListTile build: ${control.id}");
    return withPagePlatform((context, platform) {
      bool? adaptive = control.adaptive ?? parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoListTileControl(
            control: control,
            parent: parent,
            parentDisabled: parentDisabled,
            parentAdaptive: adaptive,
            children: children,
            backend: backend);
      }

      var leadingCtrls =
          children.where((c) => c.name == "leading" && c.visible);
      var titleCtrls = children.where((c) => c.name == "title" && c.visible);
      var subtitleCtrls =
          children.where((c) => c.name == "subtitle" && c.visible);
      var trailingCtrls =
          children.where((c) => c.name == "trailing" && c.visible);

      bool onclick = control.getBool("onclick", false)!;
      bool toggleInputs = control.getBool("toggleInputs", false)!;
      bool onLongPressDefined = control.getBool("onLongPress", false)!;
      String url = control.getString("url", "")!;
      String? urlTarget = control.getString("urlTarget");
      bool disabled = control.disabled || parentDisabled;

      Function()? onPressed =
          (onclick || toggleInputs || url != "") && !disabled
              ? () {
                  debugPrint("ListTile ${control.id} clicked!");
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

      Function()? onLongPress = onLongPressDefined && !disabled
          ? () {
              debugPrint("Button ${control.id} clicked!");
              backend.triggerControlEvent(control.id, "long_press");
            }
          : null;

      Widget tile = ListTile(
        autofocus: control.getBool("autofocus", false)!,
        contentPadding: parseEdgeInsets(control, "contentPadding"),
        isThreeLine: control.getBool("isThreeLine", false)!,
        selected: control.getBool("selected", false)!,
        dense: control.getBool("dense", false)!,
        onTap: onPressed,
        onLongPress: onLongPress,
        enabled: !disabled,
        horizontalTitleGap: control.getDouble("horizontalSpacing"),
        enableFeedback: control.getBool("enableFeedback"),
        minLeadingWidth: control.getDouble("minLeadingWidth"),
        minVerticalPadding: control.getDouble("minVerticalPadding"),
        minTileHeight: control.getDouble("minHeight"),
        selectedTileColor: control.getColor("selectedTileColor", context),
        selectedColor: control.getColor("selectedColor", context),
        focusColor: control.getColor("focusColor", context),
        tileColor: control.getColor("bgcolor", context),
        splashColor: control.getColor("bgcolorActivated", context),
        hoverColor: control.getColor("hoverColor", context),
        iconColor: control.getColor("iconColor", context),
        textColor: control.getColor("textColor", context),
        mouseCursor: parseMouseCursor(control.getString("mouseCursor")),
        visualDensity: parseVisualDensity(control.getString("visualDensity")),
        shape: parseOutlinedBorder(control, "shape"),
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "titleTextStyle"),
        leadingAndTrailingTextStyle: parseTextStyle(
            Theme.of(context), control, "leadingAndTrailingTextStyle"),
        subtitleTextStyle:
            parseTextStyle(Theme.of(context), control, "subtitleTextStyle"),
        titleAlignment:
            parseListTileTitleAlignment(control.getString("titleAlignment")),
        style: parseListTileStyle(control.getString("style")),
        onFocusChange: (bool hasFocus) {
          backend.triggerControlEvent(control.id, hasFocus ? "focus" : "blur");
        },
        leading: leadingCtrls.isNotEmpty
            ? createControl(control, leadingCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : null,
        title: titleCtrls.isNotEmpty
            ? createControl(control, titleCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : null,
        subtitle: subtitleCtrls.isNotEmpty
            ? createControl(control, subtitleCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : null,
        trailing: trailingCtrls.isNotEmpty
            ? createControl(control, trailingCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : null,
      );

      if (toggleInputs) {
        tile = ListTileClicks(notifier: _clickNotifier, child: tile);
      }

      tile = Material(color: Colors.transparent, child: tile);

      return constrainedControl(context, tile, parent, control);
    });
  }
}

class ListTileClickNotifier extends ChangeNotifier {
  void onClick() {
    notifyListeners();
  }
}
