import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'cupertino_list_tile.dart';

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

class ListTileControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final ListTileClickNotifier _clickNotifier = ListTileClickNotifier();

  ListTileControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("ListTile build: ${control.id}");
    bool adaptive = control.attrBool("adaptive", false)!;
    if (adaptive &&
        (defaultTargetPlatform == TargetPlatform.iOS ||
            defaultTargetPlatform == TargetPlatform.macOS)) {
      return CupertinoListTileControl(
          control: control,
          parent: parent,
          parentDisabled: parentDisabled,
          children: children);
    }

    final server = FletAppServices.of(context).server;

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
    var subtitleCtrls =
        children.where((c) => c.name == "subtitle" && c.isVisible);
    var trailingCtrls =
        children.where((c) => c.name == "trailing" && c.isVisible);

    bool selected = control.attrBool("selected", false)!;
    bool dense = control.attrBool("dense", false)!;
    bool isThreeLine = control.attrBool("isThreeLine", false)!;
    bool autofocus = control.attrBool("autofocus", false)!;
    bool onclick = control.attrBool("onclick", false)!;
    bool toggleInputs = control.attrBool("toggleInputs", false)!;
    bool onLongPressDefined = control.attrBool("onLongPress", false)!;
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = (onclick || toggleInputs || url != "") && !disabled
        ? () {
            debugPrint("ListTile ${control.id} clicked!");
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

    Function()? onLongPress = onLongPressDefined && !disabled
        ? () {
            debugPrint("Button ${control.id} clicked!");
            server.sendPageEvent(
                eventTarget: control.id,
                eventName: "long_press",
                eventData: "");
          }
        : null;

    Widget tile = ListTile(
      autofocus: autofocus,
      contentPadding: parseEdgeInsets(control, "contentPadding"),
      isThreeLine: isThreeLine,
      selected: selected,
      dense: dense,
      onTap: onPressed,
      onLongPress: onLongPress,
      enabled: !disabled,
      tileColor: HexColor.fromString(
          Theme.of(context), control.attrString("bgcolor", "")!),
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, disabled)
          : null,
      title: titleCtrls.isNotEmpty
          ? createControl(control, titleCtrls.first.id, disabled)
          : null,
      subtitle: subtitleCtrls.isNotEmpty
          ? createControl(control, subtitleCtrls.first.id, disabled)
          : null,
      trailing: trailingCtrls.isNotEmpty
          ? createControl(control, trailingCtrls.first.id, disabled)
          : null,
    );

    if (toggleInputs) {
      tile = ListTileClicks(notifier: _clickNotifier, child: tile);
    }

    return constrainedControl(context, tile, parent, control);
  }
}

class ListTileClickNotifier extends ChangeNotifier {
  void onClick() {
    notifyListeners();
  }
}
