import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import 'edge_insets.dart';
import 'mouse.dart';
import 'numbers.dart';
import 'text.dart';

/// Builds a list of [PopupMenuEntry] widgets from a collection of Flet controls.
///
/// Only controls with type `PopupMenuItem` are converted. Controls without any
/// visible content are treated as menu dividers.
List<PopupMenuEntry<String>> buildPopupMenuEntries(
    Iterable<Control> items, BuildContext context) {
  return items.where((item) => item.type == "PopupMenuItem").map((item) {
    var checked = item.getBool("checked");
    var height = item.getDouble("height", 48.0)!;
    var padding = item.getPadding("padding");
    var itemContent = item.buildTextOrWidget("content");
    var itemIcon = item.buildIconOrWidget("icon");
    var mouseCursor = item.getMouseCursor("mouse_cursor");
    var labelTextStyle =
        item.getWidgetStateTextStyle("label_text_style", Theme.of(context));

    Widget? child;
    if (itemContent != null && itemIcon == null) {
      child = itemContent;
    } else if (itemContent == null && itemIcon != null) {
      child = itemIcon;
    } else if (itemContent != null && itemIcon != null) {
      child = Row(children: [
        itemIcon,
        const SizedBox(width: 8),
        itemContent,
      ]);
    }

    var entry = checked != null
        ? CheckedPopupMenuItem<String>(
            value: item.id.toString(),
            checked: checked,
            height: height,
            padding: padding,
            enabled: !item.disabled,
            mouseCursor: mouseCursor,
            labelTextStyle: labelTextStyle,
            onTap: () => item.triggerEvent("click", !checked),
            child: child,
          )
        : PopupMenuItem<String>(
            value: item.id.toString(),
            height: height,
            padding: padding,
            labelTextStyle: labelTextStyle,
            enabled: !item.disabled,
            mouseCursor: mouseCursor,
            onTap: () => item.triggerEvent("click"),
            child: child,
          );

    return child != null
        ? entry
        : const PopupMenuDivider() as PopupMenuEntry<String>;
  }).toList();
}
