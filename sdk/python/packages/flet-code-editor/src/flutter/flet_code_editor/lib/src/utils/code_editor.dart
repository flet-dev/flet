import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_code_editor/flutter_code_editor.dart' as fce;
import 'package:flutter_highlight/theme_map.dart';

fce.CodeThemeData? parseCodeThemeData(Control control, BuildContext context) {
  final codeTheme = control.get("code_theme");
  if (codeTheme is! Map) {
    if (codeTheme is String) {
      final named = themeMap[codeTheme.toLowerCase()];
      return named == null ? null : fce.CodeThemeData(styles: named);
    }
    return null;
  }

  final themeName = codeTheme["name"];
  if (themeName is String) {
    final named = themeMap[themeName.toLowerCase()];
    if (named != null) {
      return fce.CodeThemeData(styles: named);
    }
  }

  final styles = codeTheme["styles"];
  final Map<dynamic, dynamic> stylesSource;
  if (styles is Map) {
    stylesSource = styles.cast<dynamic, dynamic>();
  } else {
    // CustomCodeTheme is serialized as a flat map of token -> TextStyle.
    final flattened = Map.of(codeTheme);
    flattened.remove("name");
    stylesSource = flattened;
  }

  final parsedStyles = <String, TextStyle>{};
  stylesSource.forEach((key, value) {
    final style = parseTextStyle(value, Theme.of(context));
    if (style != null) {
      parsedStyles[key.toString()] = style;
    }
  });

  if (parsedStyles.isEmpty) {
    return null;
  }

  return fce.CodeThemeData(styles: parsedStyles);
}

fce.GutterStyle? parseGutterStyle(Control control, BuildContext context) {
  final gutterStyle = control.get("gutter_style");
  if (gutterStyle is! Map) {
    return null;
  }

  final textStyle = parseTextStyle(gutterStyle["text_style"], Theme.of(context));
  final background =
      parseColor(gutterStyle["background_color"], Theme.of(context));
  final width = parseDouble(gutterStyle["width"]);
  final margin = _parseGutterMargin(gutterStyle["margin"]);

  final showErrors = gutterStyle["show_errors"];
  final showFoldingHandles = gutterStyle["show_folding_handles"];
  final showLineNumbers = gutterStyle["show_line_numbers"];

  return fce.GutterStyle(
    textStyle: textStyle,
    background: background,
    width: width ?? 80.0,
    margin: margin ?? 10.0,
    showErrors: showErrors is bool ? showErrors : true,
    showFoldingHandles: showFoldingHandles is bool ? showFoldingHandles : true,
    showLineNumbers: showLineNumbers is bool ? showLineNumbers : true,
  );
}

double? _parseGutterMargin(dynamic value) {
  final margin = parseDouble(value);
  if (margin != null) {
    return margin;
  }
  final edgeInsets = parseEdgeInsets(value);
  if (edgeInsets == null) {
    return null;
  }
  return (edgeInsets.left + edgeInsets.right) / 2;
}
