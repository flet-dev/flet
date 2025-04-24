import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class TextControl extends StatelessWidget {
  final Control control;

  const TextControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");

    String text = control.getString("value", "")!;
    var selectionCursorColor =
        control.getColor("selection_cursor_color", context);
    var selectionCursorWidth =
        control.getDouble("selection_cursor_width", 2.0)!;
    var selectionCursorHeight = control.getDouble("selection_cursor_height");
    var showSelectionCursor = control.getBool("show_selection_cursor", false)!;
    var enableInteractiveSelection =
        control.getBool("enable_interactive_selection", true)!;

    List<TextSpan>? spans = parseTextSpans(
      Theme.of(context),
      control.children("spans"),
      control.disabled,
      (Control control, String eventName, String eventData) {
        control.triggerEvent(eventName, data: eventData);
      },
    );
    String? semanticsLabel = control.getString("semantics_label");
    bool noWrap = control.getBool("no_wrap", false)!;
    int? maxLines = control.getInt("max_lines");

    TextStyle? style;
    var styleNameOrData = control.getString("style", null);
    if (styleNameOrData != null) {
      style = getTextStyle(context, styleNameOrData);
    }
    if (style == null && styleNameOrData != null) {
      try {
        style = control.getTextStyle("style", Theme.of(context));
      } on FormatException catch (_) {
        style = null;
      }
    }

    TextStyle? themeStyle;
    var styleName = control.getString("theme_style");
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
      variations
          .add(FontVariation('wght', parseDouble(fontWeight.substring(1), 0)!));
    }

    style = (style ?? const TextStyle()).copyWith(
      fontSize: control.getDouble("size", null),
      fontWeight: getFontWeight(fontWeight),
      fontStyle: control.getBool("italic", false)! ? FontStyle.italic : null,
      fontFamily: control.getString("font_family"),
      fontVariations: variations,
      color: control.getColor("color", context) ??
          (spans.isNotEmpty ? DefaultTextStyle.of(context).style.color : null),
      backgroundColor: control.getColor("bgcolor", context),
    );

    TextAlign textAlign =
        parseTextAlign(control.getString("text_align"), TextAlign.start)!;

    TextOverflow overflow =
        parseTextOverflow(control.getString("overflow"), TextOverflow.clip)!;

    onSelectionChanged(TextSelection selection, SelectionChangedCause? cause) {
      control.triggerEvent("selection_change", fields: {
        "text": text,
        "cause": cause?.name ?? "unknown",
        "selection": selection.toMap(),
      });
    }

    onTap() {
      control.triggerEvent("tap");
    }

    var textWidget = control.getBool("selectable", false)!
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

    return ConstrainedControl(control: control, child: textWidget);
  }
}
