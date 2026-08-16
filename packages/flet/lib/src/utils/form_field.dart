import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'borders.dart';
import 'box.dart';
import 'edge_insets.dart';
import 'enums.dart';
import 'numbers.dart';
import 'text.dart';
import 'time.dart';

/// [UnderlineInputBorder]'s default corner radius, mirroring both Flutter's
/// and the Python-side default.
const BorderRadius kUnderlineInputBorderDefaultRadius = BorderRadius.only(
    topLeft: Radius.circular(4.0), topRight: Radius.circular(4.0));

InputBorder? parseInputBorder(dynamic value, ThemeData? theme,
    {BorderSide? defaultSide, InputBorder? defaultValue}) {
  if (value is! Map) return defaultValue;
  var side = parseBorderSide(value["side"], theme, defaultValue: defaultSide);
  switch (value["_type"]) {
    case "underline":
      return UnderlineInputBorder(
          borderSide: side ?? const BorderSide(),
          borderRadius: parseBorderRadius(
              value["border_radius"], kUnderlineInputBorderDefaultRadius)!);
    case "outline":
      return OutlineInputBorder(
          borderSide: side ?? const BorderSide(),
          borderRadius: parseBorderRadius(value["border_radius"],
              const BorderRadius.all(Radius.circular(4.0)))!,
          gapPadding: parseDouble(value["gap_padding"], 4.0)!);
    case "none":
      return InputBorder.none;
    default:
      return defaultValue;
  }
}

/// Per-state input borders parsed from a control's "border" property, mapped
/// onto the [InputDecoration]/[InputDecorationTheme] border slots.
class FormFieldBorders {
  InputBorder? border;
  InputBorder? enabledBorder;
  InputBorder? focusedBorder;
  InputBorder? errorBorder;
  InputBorder? focusedErrorBorder;
  InputBorder? disabledBorder;
}

/// Parses the "border" property of [control] — either a single border or a
/// map of control states ("default", "focused", "error", "disabled") to
/// borders — into [FormFieldBorders].
///
/// The default/single border defines the shape for all states. When its side
/// is unset, only [FormFieldBorders.border] is populated with it, so the
/// Material theme keeps resolving the border side per state; an explicit side
/// additionally populates [FormFieldBorders.enabledBorder]. A state entry
/// without a side falls back to the default entry's side, then to a themed
/// side for that state.
FormFieldBorders parseFormFieldBorders(Control control, ThemeData theme) {
  var borders = FormFieldBorders();
  var value = control.get("border");

  Map<dynamic, dynamic>? stateMap;
  dynamic defaultEntry = value;
  if (value is Map && !value.containsKey("_type")) {
    stateMap = value;
    defaultEntry = value["default"];
  }

  var defaultSide =
      defaultEntry is Map ? parseBorderSide(defaultEntry["side"], theme) : null;
  var defaultBorder = parseInputBorder(defaultEntry, theme,
      defaultValue: const OutlineInputBorder())!;
  borders.border = defaultBorder;
  if (defaultSide != null || defaultBorder == InputBorder.none) {
    borders.enabledBorder = defaultBorder;
  }

  if (stateMap != null) {
    InputBorder? stateBorder(String stateName, BorderSide themedSide) {
      return parseInputBorder(stateMap![stateName], theme,
          defaultSide: defaultSide ?? themedSide);
    }

    borders.focusedBorder = stateBorder(
        "focused", BorderSide(color: theme.colorScheme.primary, width: 2.0));
    borders.errorBorder = stateBorder(
        "error", BorderSide(color: theme.colorScheme.error, width: 1.0));
    // The "error" entry also covers the focused-error state, at Material's
    // focused weight when no side is configured.
    borders.focusedErrorBorder = stateBorder(
        "error", BorderSide(color: theme.colorScheme.error, width: 2.0));
    borders.disabledBorder = stateBorder(
        "disabled",
        BorderSide(
            color: theme.colorScheme.onSurface.withValues(alpha: 0.12),
            width: 1.0));
  }
  return borders;
}

/// A [BoxDecoration]'s border values, translated from an [InputBorder].
class FormFieldBoxBorder {
  final BoxBorder? border;
  final BorderRadius? borderRadius;

  const FormFieldBoxBorder({this.border, this.borderRadius});
}

/// Translates the "border" property of [control] into [BoxDecoration] values,
/// for controls decorated with a [BoxDecoration] rather than an
/// [InputDecoration].
///
/// A [BoxDecoration] holds one static border, so the entry matching the
/// control's current state is resolved here instead of by the framework;
/// "error" has no counterpart on this side and is ignored. A null
/// [FormFieldBoxBorder.border] means "keep the widget's own default border",
/// since [BoxDecoration.copyWith] leaves null arguments unchanged.
FormFieldBoxBorder parseFormFieldBoxBorder(Control control, ThemeData theme,
    {bool focused = false}) {
  var value = control.get("border");

  dynamic defaultEntry = value;
  dynamic entry = value;
  if (value is Map && !value.containsKey("_type")) {
    defaultEntry = value["default"];
    entry = (control.disabled ? value["disabled"] : null) ??
        (focused ? value["focused"] : null) ??
        defaultEntry;
  }

  // A state entry without a side inherits the default entry's side, as on the
  // Material side.
  var explicitSide = (entry is Map ? entry["side"] : null) ??
      (defaultEntry is Map ? defaultEntry["side"] : null);
  var borderSide =
      parseBorderSide(explicitSide, theme, defaultValue: const BorderSide())!;

  switch (entry is Map ? entry["_type"] : "outline") {
    case "underline":
      // The underline's default top-corner radius is treated as unconfigured,
      // and a non-zero radius cannot be painted with a hairline solid side.
      var radius = parseBorderRadius(entry["border_radius"]);
      return FormFieldBoxBorder(
          border: Border(bottom: borderSide),
          borderRadius: radius == null ||
                  radius == kUnderlineInputBorderDefaultRadius ||
                  (borderSide.width == 0.0 &&
                      borderSide.style == BorderStyle.solid)
              ? BorderRadius.zero
              : radius);
    case "none":
      // A nothing-painting border: copyWith cannot clear an existing border,
      // so it must be replaced instead.
      return const FormFieldBoxBorder(
          border: Border.fromBorderSide(BorderSide.none));
    default:
      // Outline: without an explicit side, keep the widget's native border.
      return FormFieldBoxBorder(
          border:
              explicitSide != null ? Border.fromBorderSide(borderSide) : null,
          borderRadius:
              entry is Map ? parseBorderRadius(entry["border_radius"]) : null);
  }
}

TextInputType? parseTextInputType(String? value,
    [TextInputType? defaultValue]) {
  const typeMap = {
    "datetime": TextInputType.datetime,
    "email": TextInputType.emailAddress,
    "multiline": TextInputType.multiline,
    "name": TextInputType.name,
    "none": TextInputType.none,
    "number": TextInputType.number,
    "phone": TextInputType.phone,
    "streetaddress": TextInputType.streetAddress,
    "text": TextInputType.text,
    "url": TextInputType.url,
    "visiblepassword": TextInputType.visiblePassword,
    "websearch": TextInputType.webSearch,
    "twitter": TextInputType.twitter,
  };
  return typeMap[value?.toLowerCase()] ?? defaultValue;
}

InputDecoration buildInputDecoration(
  BuildContext context,
  Control control, {
  Widget? customSuffix,
  int? valueLength,
  int? maxLength,
  bool focused = false,
}) {
  var borders = parseFormFieldBorders(control, Theme.of(context));
  var bgcolor = control.getColor("bgcolor", context);
  var focusedBgcolor = control.getColor("focused_bgcolor", context);
  var fillColor = control.getColor("fill_color", context);
  var hoverColor = control.getColor("hover_color", context);

  //counter
  String? counterText;
  Widget? counterWidget;
  var counter = control.get("counter");
  if (counter is Control) {
    counterWidget = control.buildWidget("counter");
  } else {
    counterText = control
        .getString("counter")
        ?.replaceAll("{value_length}", valueLength.toString())
        .replaceAll("{max_length}", maxLength?.toString() ?? "None")
        .replaceAll("{symbols_left}",
            "${maxLength == null ? 'None' : (maxLength - (valueLength ?? 0))}");
  }

  // error
  String? errorText;
  Widget? errorWidget;
  var error = control.get("error");
  if (error is Control) {
    errorWidget = control.buildWidget("error");
  } else {
    errorText = control.getString("error");
  }
  // helper
  String? helperText;
  Widget? helperWidget;
  var helper = control.get("helper");
  if (helper is Control) {
    helperWidget = control.buildWidget("helper");
  } else {
    helperText = control.getString("helper");
  }

  // prefix
  String? prefixText;
  Widget? prefixWidget;
  var prefix = control.get("prefix");
  if (prefix is Control) {
    prefixWidget = control.buildWidget("prefix");
  } else {
    prefixText = control.getString("prefix");
  }

  // suffix
  String? suffixText;
  Widget? suffixWidget;
  var suffix = control.get("suffix");
  if (suffix is Control) {
    suffixWidget = control.buildWidget("suffix");
  } else {
    suffixText = control.getString("suffix");
  }

  return InputDecoration(
      enabled: !control.disabled,
      contentPadding: control.getEdgeInsets("content_padding"),
      isDense: control.getBool("dense"),
      label: control.buildTextOrWidget("label"),
      labelStyle: control.getTextStyle("label_style", Theme.of(context)),
      border: borders.border,
      enabledBorder: borders.enabledBorder,
      focusedBorder: borders.focusedBorder,
      errorBorder: borders.errorBorder,
      focusedErrorBorder: borders.focusedErrorBorder,
      disabledBorder: borders.disabledBorder,
      hoverColor: hoverColor,
      icon: control.buildIconOrWidget("icon"),
      filled: control.getBool("filled", false)!,
      fillColor: fillColor ?? (focused ? (focusedBgcolor ?? bgcolor) : bgcolor),
      //hint
      hintText: control.getString("hint_text"),
      hintStyle: control.getTextStyle("hint_style", Theme.of(context)),
      hintFadeDuration: control.getDuration("hint_fade_duration"),
      hintMaxLines: control.getInt("hint_max_lines"),
      //helper
      helper: helperWidget,
      helperText: helperText,
      helperStyle: control.getTextStyle("helper_style", Theme.of(context)),
      helperMaxLines: control.getInt("helper_max_lines"),
      //counter
      counter: counterWidget,
      counterText: counterText,
      counterStyle: control.getTextStyle("counter_style", Theme.of(context)),
      //error
      error: errorWidget,
      errorText: errorText,
      errorStyle: control.getTextStyle("error_style", Theme.of(context)),
      errorMaxLines: control.getInt("error_max_lines"),
      constraints: control.getBoxConstraints("size_constraints"),
      isCollapsed: control.getBool("collapsed"),
      prefixIconConstraints:
          control.getBoxConstraints("prefix_icon_constraints"),
      suffixIconConstraints:
          control.getBoxConstraints("suffix_icon_constraints"),
      focusColor: control.getColor("focus_color", context),
      alignLabelWithHint: control.getBool("align_label_with_hint"),
      prefixIcon: control.buildIconOrWidget("prefix_icon"),
      //prefix
      prefix: prefixWidget,
      prefixText: prefixText,
      prefixStyle: control.getTextStyle("prefix_style", Theme.of(context)),
      suffixIcon: control.buildIconOrWidget("suffix_icon") ?? customSuffix,
      //suffix
      suffix: suffixWidget,
      suffixText: suffixText,
      suffixStyle: control.getTextStyle("suffix_style", Theme.of(context)));
}

OverlayVisibilityMode? parseOverlayVisibilityMode(String? value,
    [OverlayVisibilityMode? defaultValue]) {
  return parseEnum(OverlayVisibilityMode.values, value, defaultValue);
}

StrutStyle? parseStrutStyle(dynamic value, [StrutStyle? defaultValue]) {
  if (value == null) return defaultValue;

  return StrutStyle(
    fontSize: parseDouble(value["size"]),
    fontWeight: parseFontWeight(value["weight"]),
    fontStyle: parseBool(value["italic"], false)! ? FontStyle.italic : null,
    fontFamily: value["font_family"],
    height: parseDouble(value["height"]),
    leading: parseDouble(value["leading"]),
    forceStrutHeight: parseBool(value["force_strut_height"]),
  );
}

extension FormFieldParsers on Control {
  TextInputType? getTextInputType(String propertyName,
      [TextInputType? defaultValue]) {
    return parseTextInputType(get(propertyName), defaultValue);
  }

  OverlayVisibilityMode? getOverlayVisibilityMode(String propertyName,
      [OverlayVisibilityMode? defaultValue]) {
    return parseOverlayVisibilityMode(get(propertyName), defaultValue);
  }

  StrutStyle? getStrutStyle(String propertyName, [StrutStyle? defaultValue]) {
    return parseStrutStyle(get(propertyName), defaultValue);
  }
}
