import 'package:flutter/material.dart';

import '../models/control.dart';
import 'cupertino_colors.dart';
import 'material_state.dart';
import 'numbers.dart';

Color? _getThemeColor(ThemeData theme, String colorName) {
  var scheme = theme.colorScheme;
  switch (colorName.toLowerCase()) {
    // Primary colors
    case "primary":
      return scheme.primary;
    case "onprimary":
      return scheme.onPrimary;
    case "primarycontainer":
      return scheme.primaryContainer;
    case "onprimarycontainer":
      return scheme.onPrimaryContainer;
    case "primaryfixed":
      return scheme.primaryFixed;
    case "primaryfixeddim":
      return scheme.primaryFixedDim;
    case "onprimaryfixed":
      return scheme.onPrimaryFixed;
    case "onprimaryfixedvariant":
      return scheme.onPrimaryFixedVariant;

    // Secondary colors
    case "secondary":
      return scheme.secondary;
    case "onsecondary":
      return scheme.onSecondary;
    case "secondarycontainer":
      return scheme.secondaryContainer;
    case "onsecondarycontainer":
      return scheme.onSecondaryContainer;
    case "secondaryfixed":
      return scheme.secondaryFixed;
    case "secondaryfixeddim":
      return scheme.secondaryFixedDim;
    case "onsecondaryfixed":
      return scheme.onSecondaryFixed;
    case "onsecondaryfixedvariant":
      return scheme.onSecondaryFixedVariant;

    // Tertiary colors
    case "tertiary":
      return scheme.tertiary;
    case "ontertiary":
      return scheme.onTertiary;
    case "tertiarycontainer":
      return scheme.tertiaryContainer;
    case "ontertiarycontainer":
      return scheme.onTertiaryContainer;
    case "tertiaryfixed":
      return scheme.tertiaryFixed;
    case "tertiaryfixeddim":
      return scheme.tertiaryFixedDim;
    case "ontertiaryfixed":
      return scheme.onTertiaryFixed;
    case "ontertiaryfixedvariant":
      return scheme.onTertiaryFixedVariant;

    // Error colors
    case "error":
      return scheme.error;
    case "onerror":
      return scheme.onError;
    case "errorcontainer":
      return scheme.errorContainer;
    case "onerrorcontainer":
      return scheme.onErrorContainer;

    // Surface colors
    case "surface":
      return scheme.surface;
    case "onsurface":
      return scheme.onSurface;
    case "surfacebright":
      return scheme.surfaceBright;
    case "surfacedim":
      return scheme.surfaceDim;
    case "surfacecontainer":
      return scheme.surfaceContainer;
    case "surfacecontainerhigh":
      return scheme.surfaceContainerHigh;
    case "surfacecontainerlow":
      return scheme.surfaceContainerLow;
    case "surfacecontainerlowest":
      return scheme.surfaceContainerLowest;
    case "surfacecontainerhighest":
      return scheme.surfaceContainerHighest;

    // Utility colors
    case "outline":
      return scheme.outline;
    case "outlinevariant":
      return scheme.outlineVariant;
    case "shadow":
      return scheme.shadow;
    case "scrim":
      return scheme.scrim;
    case "onsurfacevariant":
      return scheme.onSurfaceVariant;
    case "surfacetint":
      return scheme.surfaceTint;

    // Inverse colors
    case "inversesurface":
      return scheme.inverseSurface;
    case "oninversesurface":
      return scheme.onInverseSurface;
    case "inverseprimary":
      return scheme.inversePrimary;
  }
  return null;
}

Map<String, Color> _plainColors = {
  "white10": Colors.white10,
  "white12": Colors.white12,
  "white24": Colors.white24,
  "white30": Colors.white30,
  "white38": Colors.white38,
  "white54": Colors.white54,
  "white60": Colors.white60,
  "white70": Colors.white70,
  "white": Colors.white,
  "black12": Colors.black12,
  "black26": Colors.black26,
  "black38": Colors.black38,
  "black45": Colors.black45,
  "black54": Colors.black54,
  "black87": Colors.black87,
  "black": Colors.black,
  "transparent": Colors.transparent
};

Map<String, MaterialColor> _materialColors = {
  "red": Colors.red,
  "pink": Colors.pink,
  "purple": Colors.purple,
  "deeppurple": Colors.deepPurple,
  "indigo": Colors.indigo,
  "blue": Colors.blue,
  "lightblue": Colors.lightBlue,
  "cyan": Colors.cyan,
  "teal": Colors.teal,
  "green": Colors.green,
  "lightgreen": Colors.lightGreen,
  "lime": Colors.lime,
  "yellow": Colors.yellow,
  "amber": Colors.amber,
  "orange": Colors.orange,
  "deeporange": Colors.deepOrange,
  "brown": Colors.brown,
  "bluegrey": Colors.blueGrey,
  "grey": Colors.grey
};

Map<String, MaterialAccentColor> _materialAccentColors = {
  "redaccent": Colors.redAccent,
  "pinkaccent": Colors.pinkAccent,
  "purpleaccent": Colors.purpleAccent,
  "deeppurpleaccent": Colors.deepPurpleAccent,
  "indigoaccent": Colors.indigoAccent,
  "blueaccent": Colors.blueAccent,
  "lightblueaccent": Colors.lightBlueAccent,
  "cyanaccent": Colors.cyanAccent,
  "tealaccent": Colors.tealAccent,
  "greenaccent": Colors.greenAccent,
  "lightgreenaccent": Colors.lightGreenAccent,
  "limeaccent": Colors.limeAccent,
  "yellowaccent": Colors.yellowAccent,
  "amberaccent": Colors.amberAccent,
  "orangeaccent": Colors.orangeAccent,
  "deeporangeaccent": Colors.deepOrangeAccent,
};

// https://stackoverflow.com/questions/50081213/how-do-i-use-hexadecimal-color-strings-in-flutter
extension HexColor on Color {
  static Color? fromString(ThemeData? theme, String? colorString,
      [Color? defaultColor]) {
    if (colorString == null || colorString.isEmpty) {
      return defaultColor;
    }
    var colorParts = colorString.split(",");

    var colorValue = colorParts[0];
    var colorOpacity = colorParts.length > 1 ? colorParts[1] : null;

    Color? color;
    if (colorValue.startsWith("#")) {
      color = HexColor._fromHex(colorValue.substring(1));
    } else if (colorValue.startsWith("0x")) {
      color = HexColor._fromHex(colorValue.substring(2));
    } else {
      color = HexColor._fromNamedColor(theme, colorValue);
    }

    if (color != null && colorOpacity != null) {
      color = color.withValues(alpha: parseDouble(colorOpacity, 1.0)!);
    }

    return color ?? defaultColor;
  }

  static Color? _fromNamedColor(ThemeData? theme, String colorName) {
    RegExp namedColor = RegExp(r'^([a-zA-Z]+)([0-9]*)$');
    var matches = namedColor.allMatches(colorName);
    if (matches.isEmpty) {
      return null;
    }
    var name = matches.first.group(1) ?? "";
    var shade = int.tryParse(matches.first.group(2)!) ?? 0;

    // scheme color
    if (theme != null) {
      Color? color = _getThemeColor(theme, name);
      if (color != null) {
        return color;
      }
    }

    // plain color
    Color? color = _plainColors[colorName.toLowerCase()];
    if (color != null) {
      return color;
    }

    // find material color
    MaterialColor? primaryColor = _materialColors[name.toLowerCase()];
    if (primaryColor != null) {
      var shadedColor = primaryColor[shade];
      return shadedColor ?? primaryColor;
    }

    // find cupertino color
    Color? cupertinoColor = cupertinoColors[name.toLowerCase()];
    if (cupertinoColor != null) {
      return cupertinoColor;
    }

    // accent color
    MaterialAccentColor? accentColor =
        _materialAccentColors[name.toLowerCase()];
    if (accentColor != null) {
      var shadedColor = accentColor[shade];
      return shadedColor ?? accentColor;
    }

    return null;
  }

  /// String is in the format "aabbcc" or "ffaabbcc" with an optional leading "#".
  static Color _fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6) buffer.write('ff');
    buffer.write(hexString);
    return Color(int.parse(buffer.toString(), radix: 16));
  }

  /// Prefixes a hash sign if [leadingHashSign] is set to `true` (default is `true`).
  String toHex({bool leadingHashSign = true}) {
    int to8bit(double component) =>
        (component * 255.0).round().clamp(0, 255);

    final alpha8 = to8bit(a);
    final red8 = to8bit(r);
    final green8 = to8bit(g);
    final blue8 = to8bit(b);

    return '${leadingHashSign ? '#' : ''}'
        '${alpha8.toRadixString(16).padLeft(2, '0')}'
        '${red8.toRadixString(16).padLeft(2, '0')}'
        '${green8.toRadixString(16).padLeft(2, '0')}'
        '${blue8.toRadixString(16).padLeft(2, '0')}';
  }
}

extension ColorExtension on Color {
  /// Convert the color to a darken color based on the [percent]
  Color darken([int percent = 40]) {
    assert(1 <= percent && percent <= 100);
    final value = 1 - percent / 100;
    int to8bit(double component) =>
        (component * 255.0).round().clamp(0, 255);

    return Color.fromARGB(
      to8bit(a),
      (to8bit(r) * value).round().clamp(0, 255),
      (to8bit(g) * value).round().clamp(0, 255),
      (to8bit(b) * value).round().clamp(0, 255),
    );
  }
}

WidgetStateProperty<Color?>? parseWidgetStateColor(
    dynamic value, ThemeData theme,
    {Color? defaultColor, WidgetStateProperty<Color?>? defaultValue}) {
  if (value == null) return defaultValue;

  return getWidgetStateProperty<Color?>(
      value, (jv) => HexColor.fromString(theme, jv as String), defaultColor);
}

Color? parseColor(String? value, ThemeData? theme, [Color? defaultColor]) =>
    HexColor.fromString(theme, value, defaultColor);

extension ColorParsers on Control {
  Color? getColor(String propertyName, BuildContext? context,
      [Color? defaultValue]) {
    return parseColor(getString(propertyName),
        context != null ? Theme.of(context) : null, defaultValue);
  }

  WidgetStateProperty<Color?>? getWidgetStateColor(
      String propertyName, ThemeData theme,
      {Color? defaultColor, WidgetStateProperty<Color?>? defaultValue}) {
    return parseWidgetStateColor(get(propertyName), theme,
        defaultColor: defaultColor, defaultValue: defaultValue);
  }
}
