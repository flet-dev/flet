import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class TextControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const TextControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    var result = withControlTree(control, (context, viewModel) {
      debugPrint("Text build: ${control.id}");

      bool disabled = control.disabled || parentDisabled;

      String text = control.getString("value", "")!;
      var selectionCursorColor =
          control.getColor("selectionCursorColor", context);
      var selectionCursorWidth =
          control.getDouble("selectionCursorWidth", 2.0)!;
      var selectionCursorHeight = control.getDouble("selectionCursorHeight");
      var showSelectionCursor = control.getBool("showSelectionCursor", false)!;
      var enableInteractiveSelection =
          control.getBool("enableInteractiveSelection", true)!;

      List<InlineSpan>? spans = parseTextSpans(
        Theme.of(context),
        viewModel,
        disabled,
        (String controlId, String eventName, String eventData) {
          backend.triggerControlEvent(controlId, eventName, eventData);
        },
      );
      String? semanticsLabel = control.getString("semanticsLabel");
      bool noWrap = control.getBool("noWrap", false)!;
      int? maxLines = control.getInt("maxLines");

      TextStyle? style;
      var styleNameOrData = control.getString("style", null);
      if (styleNameOrData != null) {
        style = getTextStyle(context, styleNameOrData);
      }
      if (style == null && styleNameOrData != null) {
        try {
          style = parseTextStyle(Theme.of(context), control, "style");
        } on FormatException catch (_) {
          style = null;
        }
      }

      TextStyle? themeStyle;
      var styleName = control.getString("theme_style", null);
      if (styleName != null) {
        themeStyle = getTextStyle(context, styleName);
      }

      if (style == null && themeStyle != null) {
        style = themeStyle;
      } else if (style != null && themeStyle != null) {
        style = themeStyle.merge(style);
      }

      var fontWeight = control.getString("weight", "")!;

      List<FontVariation> variations = [];
      if (fontWeight.startsWith("w")) {
        variations.add(
            FontVariation('wght', parseDouble(fontWeight.substring(1), 0)!));
      }

      style = (style ?? const TextStyle()).copyWith(
        fontSize: control.getDouble("size", null),
        fontWeight: getFontWeight(fontWeight),
        fontStyle: control.getBool(
          "italic",
          false,
        )!
            ? FontStyle.italic
            : null,
        fontFamily: control.getString("fontFamily"),
        fontVariations: variations,
        color: control.getColor("color", context) ??
            (spans.isNotEmpty
                ? DefaultTextStyle.of(context).style.color
                : null),
        backgroundColor: control.getColor("bgcolor", context),
      );

      TextAlign textAlign =
          parseTextAlign(control.getString("textAlign"), TextAlign.start)!;

      TextOverflow overflow =
          parseTextOverflow(control.getString("overflow"), TextOverflow.clip)!;

      onSelectionChanged(
          TextSelection selection, SelectionChangedCause? cause) {
        debugPrint("Text ${control.id} selection changed");
        backend.triggerControlEvent(
            control.id,
            "selection_change",
            jsonEncode({
              "text": text ?? "",
              "start": selection.start,
              "end": selection.end,
              "base_offset": selection.baseOffset,
              "extent_offset": selection.extentOffset,
              "affinity": selection.affinity.name,
              "directional": selection.isDirectional,
              "collapsed": selection.isCollapsed,
              "valid": selection.isValid,
              "normalized": selection.isNormalized,
              "cause": cause?.name ?? "unknown",
            }));
      }

      onTap() {
        debugPrint("Text ${control.id} selection changed");
        backend.triggerControlEvent(
          control.id,
          "selection_change",
        );
      }

      return control.getBool("selectable", false)!
          ? (spans.isNotEmpty)
              ? SelectableText.rich(
                  TextSpan(text: text, style: style, children: spans),
                  maxLines: maxLines,
                  textAlign: textAlign,
                  cursorColor: selectionCursorColor,
                  cursorHeight: selectionCursorHeight,
                  cursorWidth: selectionCursorWidth,
                  semanticsLabel: semanticsLabel,
                  showCursor: showSelectionCursor,
                  enableInteractiveSelection: enableInteractiveSelection,
                  onSelectionChanged: onSelectionChanged,
                  onTap: onTap,
                )
              : SelectableText(
                  text,
                  semanticsLabel: semanticsLabel,
                  maxLines: maxLines,
                  style: style,
                  textAlign: textAlign,
                  cursorColor: selectionCursorColor,
                  cursorHeight: selectionCursorHeight,
                  cursorWidth: selectionCursorWidth,
                  showCursor: showSelectionCursor,
                  enableInteractiveSelection: enableInteractiveSelection,
                  onSelectionChanged: onSelectionChanged,
                  onTap: onTap,
                )
          : (spans.isNotEmpty)
              ? Text.rich(
                  TextSpan(text: text, style: style, children: spans),
                  semanticsLabel: semanticsLabel,
                  maxLines: maxLines,
                  softWrap: !noWrap,
                  textAlign: textAlign,
                  overflow: overflow,
                )
              : Text(
                  text,
                  semanticsLabel: semanticsLabel,
                  maxLines: maxLines,
                  softWrap: !noWrap,
                  style: style,
                  textAlign: textAlign,
                  overflow: overflow,
                );
    });

    return constrainedControl(context, result, parent, control);
  }
}
