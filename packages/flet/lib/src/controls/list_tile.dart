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
      bool? adaptive = control.isAdaptive ?? parentAdaptive;
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
          children.where((c) => c.name == "leading" && c.isVisible);
      var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
      var subtitleCtrls =
          children.where((c) => c.name == "subtitle" && c.isVisible);
      var trailingCtrls =
          children.where((c) => c.name == "trailing" && c.isVisible);

      bool onclick = control.attrBool("onclick", false)!;
      bool toggleInputs = control.attrBool("toggleInputs", false)!;
      bool onLongPressDefined = control.attrBool("onLongPress", false)!;
      String url = control.attrString("url", "")!;
      String? urlTarget = control.attrString("urlTarget");
      bool disabled = control.isDisabled || parentDisabled;

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
        autofocus: control.attrBool("autofocus", false)!,
        contentPadding: parseEdgeInsets(control, "contentPadding"),
        isThreeLine: control.attrBool("isThreeLine", false)!,
        selected: control.attrBool("selected", false)!,
        dense: control.attrBool("dense", false)!,
        onTap: onPressed,
        onLongPress: onLongPress,
        enabled: !disabled,
        horizontalTitleGap: control.attrDouble("horizontalSpacing"),
        enableFeedback: control.attrBool("enableFeedback"),
        minLeadingWidth: control.attrDouble("minLeadingWidth"),
        minVerticalPadding: control.attrDouble("minVerticalPadding"),
        minTileHeight: control.attrDouble("minHeight"),
        selectedTileColor: control.attrColor("selectedTileColor", context),
        selectedColor: control.attrColor("selectedColor", context),
        focusColor: control.attrColor("focusColor", context),
        tileColor: control.attrColor("bgcolor", context),
        splashColor: control.attrColor("bgcolorActivated", context),
        hoverColor: control.attrColor("hoverColor", context),
        iconColor: control.attrColor("iconColor", context),
        textColor: control.attrColor("textColor", context),
        mouseCursor: parseMouseCursor(control.attrString("mouseCursor")),
        visualDensity: parseVisualDensity(control.attrString("visualDensity")),
        shape: parseOutlinedBorder(control, "shape"),
        titleTextStyle:
            parseTextStyle(Theme.of(context), control, "titleTextStyle"),
        leadingAndTrailingTextStyle: parseTextStyle(
            Theme.of(context), control, "leadingAndTrailingTextStyle"),
        subtitleTextStyle:
            parseTextStyle(Theme.of(context), control, "subtitleTextStyle"),
        titleAlignment:
            parseListTileTitleAlignment(control.attrString("titleAlignment")),
        style: parseListTileStyle(control.attrString("style")),
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
