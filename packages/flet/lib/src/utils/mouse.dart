import 'package:flutter/material.dart';

import '../models/control.dart';
import 'material_state.dart';

MouseCursor? parseMouseCursor(String? cursor, [MouseCursor? defaultValue]) {
  const cursorMap = {
    "alias": SystemMouseCursors.alias,
    "allscroll": SystemMouseCursors.allScroll,
    "basic": SystemMouseCursors.basic,
    "cell": SystemMouseCursors.cell,
    "click": SystemMouseCursors.click,
    "contextmenu": SystemMouseCursors.contextMenu,
    "copy": SystemMouseCursors.copy,
    "disappearing": SystemMouseCursors.disappearing,
    "forbidden": SystemMouseCursors.forbidden,
    "grab": SystemMouseCursors.grab,
    "grabbing": SystemMouseCursors.grabbing,
    "help": SystemMouseCursors.help,
    "move": SystemMouseCursors.move,
    "nodrop": SystemMouseCursors.noDrop,
    "none": SystemMouseCursors.none,
    "precise": SystemMouseCursors.precise,
    "progress": SystemMouseCursors.progress,
    "resizecolumn": SystemMouseCursors.resizeColumn,
    "resizedown": SystemMouseCursors.resizeDown,
    "resizedownleft": SystemMouseCursors.resizeDownLeft,
    "resizedownright": SystemMouseCursors.resizeDownRight,
    "resizeleft": SystemMouseCursors.resizeLeft,
    "resizeleftright": SystemMouseCursors.resizeLeftRight,
    "resizeright": SystemMouseCursors.resizeRight,
    "resizerow": SystemMouseCursors.resizeRow,
    "resizeup": SystemMouseCursors.resizeUp,
    "resizeupdown": SystemMouseCursors.resizeUpDown,
    "resizeupleft": SystemMouseCursors.resizeUpLeft,
    "resizeupleftdownright": SystemMouseCursors.resizeUpLeftDownRight,
    "resizeupright": SystemMouseCursors.resizeUpRight,
    "resizeuprightdownleft": SystemMouseCursors.resizeUpRightDownLeft,
    "text": SystemMouseCursors.text,
    "verticaltext": SystemMouseCursors.verticalText,
    "wait": SystemMouseCursors.wait,
    "zoomin": SystemMouseCursors.zoomIn,
    "zoomout": SystemMouseCursors.zoomOut,
  };

  return cursorMap[cursor?.toLowerCase() ?? ""] ?? defaultValue;
}

WidgetStateProperty<MouseCursor?>? parseWidgetStateMouseCursor(dynamic value,
    {MouseCursor? defaultMouseCursor,
    WidgetStateProperty<MouseCursor?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<MouseCursor?>(
      value, (jv) => parseMouseCursor(jv as String), defaultMouseCursor);
}

extension MouseParsers on Control {
  MouseCursor? getMouseCursor(String propertyName,
      [MouseCursor? defaultValue]) {
    return parseMouseCursor(get(propertyName), defaultValue);
  }

  WidgetStateProperty<MouseCursor?>? getWidgetStateMouseCursor(
      String propertyName,
      {MouseCursor? defaultMouseCursor,
      WidgetStateProperty<MouseCursor?>? defaultValue}) {
    return parseWidgetStateMouseCursor(get(propertyName),
        defaultMouseCursor: defaultMouseCursor, defaultValue: defaultValue);
  }
}
