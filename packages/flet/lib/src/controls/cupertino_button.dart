import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoButtonControl> createState() => _CupertinoButtonControlState();
}

class _CupertinoButtonControlState extends State<CupertinoButtonControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoButton build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var contentCtrls = widget.children.where((c) => c.name == "content");

    String? text = widget.control.attrString("text");
    IconData? icon = parseIcon(widget.control.attrString("icon", "")!);
    Color? iconColor = widget.control.attrColor("iconColor", context);

    // IconButton props below
    double? iconSize = widget.control.attrDouble("iconSize");
    bool selected = widget.control.attrBool("selected", false)!;
    IconData? selectedIcon =
        parseIcon(widget.control.attrString("selectedIcon", "")!);
    Color? selectedIconColor =
        widget.control.attrColor("selectedIconColor", context);

    Widget? content;
    List<Widget> children = [];
    if (icon != null) {
      children.add(Icon(
        selected ? selectedIcon : icon,
        color: selected ? selectedIconColor : iconColor,
        size: iconSize,
      ));
    }
    if (text != null) {
      children.add(Text(text));
    }

    if (children.isNotEmpty) {
      if (children.length == 2) {
        children.insert(1, const SizedBox(width: 8));
        content = Row(
          mainAxisSize: MainAxisSize.min,
          children: children,
        );
      } else {
        content = children.first;
      }
    } else if (contentCtrls.isNotEmpty) {
      content = createControl(widget.control, contentCtrls.first.id, disabled,
          parentAdaptive: widget.parentAdaptive);
    }

    if (content == null) {
      return const ErrorControl(
          "CupertinoButton has no content control. Please specify one.");
    }

    double pressedOpacity = widget.control.attrDouble("opacityOnClick", 0.4)!;
    double minSize = widget.control.attrDouble("minSize", 44.0)!;
    String url = widget.control.attrString("url", "")!;
    Color disabledColor = widget.control.attrColor("disabledColor", context) ??
        CupertinoColors.quaternarySystemFill;
    Color? bgColor = widget.control.attrColor("bgColor", context);
    Color? color = widget.control.attrColor("color", context);
    AlignmentGeometry alignment =
        parseAlignment(widget.control, "alignment") ?? Alignment.center;
    BorderRadius borderRadius =
        parseBorderRadius(widget.control, "borderRadius") ??
            const BorderRadius.all(Radius.circular(8.0));

    EdgeInsets? padding = parseEdgeInsets(widget.control, "padding");

    var theme = Theme.of(context);
    var style = parseButtonStyle(Theme.of(context), widget.control, "style",
        defaultForegroundColor: theme.colorScheme.primary,
        defaultBackgroundColor: Colors.transparent,
        defaultOverlayColor: Colors.transparent,
        defaultShadowColor: Colors.transparent,
        defaultSurfaceTintColor: Colors.transparent,
        defaultElevation: 0,
        defaultPadding: const EdgeInsets.all(8),
        defaultBorderSide: BorderSide.none,
        defaultShape: theme.useMaterial3
            ? const StadiumBorder()
            : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    if (padding == null && style != null) {
      padding = style.padding?.resolve({}) as EdgeInsets?;
    }

    if (bgColor == null && style != null) {
      bgColor = style.backgroundColor
          ?.resolve(selected ? {MaterialState.selected} : {});
    }

    if (color == null && style != null) {
      color = style.foregroundColor
          ?.resolve(selected ? {MaterialState.selected} : {});
    }

    if (color != null) {
      content = DefaultTextStyle(
          style: CupertinoTheme.of(context)
              .textTheme
              .textStyle
              .copyWith(color: color),
          child: content);
    }

    Function()? onPressed = !disabled
        ? () {
            debugPrint("CupertinoButton ${widget.control.id} clicked!");
            if (url != "") {
              openWebBrowser(url,
                  webWindowName: widget.control.attrString("urlTarget"));
            }
            widget.backend.triggerControlEvent(widget.control.id, "click");
          }
        : null;

    CupertinoButton? button = CupertinoButton(
      onPressed: onPressed,
      disabledColor: disabledColor,
      color: bgColor,
      padding: padding,
      borderRadius: borderRadius,
      pressedOpacity: pressedOpacity,
      alignment: alignment,
      minSize: minSize,
      child: content,
    );

    return constrainedControl(context, button, widget.parent, widget.control);
  }
}
