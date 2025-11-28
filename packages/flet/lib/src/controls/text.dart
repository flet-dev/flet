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

    final theme = Theme.of(context);
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
      control.children("spans"),
      theme,
      (Control control, String eventName, [dynamic eventData]) {
        control.triggerEvent(eventName, eventData);
      },
    );
    var semanticsLabel = control.getString("semantics_label");
    var noWrap = control.getBool("no_wrap", false)!;
    var maxLines = control.getInt("max_lines");

    var style = control.getTextStyle("style", theme);
    var themeStyle =
        parseTextThemeStyle(control.getString("theme_style"), context);
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
      overflow: control.getTextOverflow("overflow"),
      fontSize: control.getDouble("size", null),
      fontWeight: parseFontWeight(fontWeight),
      fontStyle: control.getBool("italic", false)! ? FontStyle.italic : null,
      fontFamily: control.getString("font_family"),
      fontVariations: variations,
      color: control.getColor("color", context) ??
          (spans.isNotEmpty ? DefaultTextStyle.of(context).style.color : null),
      backgroundColor: control.getColor("bgcolor", context),
    );

    var textAlign =
        parseTextAlign(control.getString("text_align"), TextAlign.start)!;

    onSelectionChanged(TextSelection selection, SelectionChangedCause? cause) {
      control.triggerEvent("selection_change", {
        "selected_text": text,
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
              )
            : Text(
                text,
                semanticsLabel: semanticsLabel,
                maxLines: maxLines,
                softWrap: !noWrap,
                style: style,
                textAlign: textAlign,
              );

    return LayoutControl(control: control, child: textWidget);
  }
}
