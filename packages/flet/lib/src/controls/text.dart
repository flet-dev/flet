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

      bool disabled = control.isDisabled || parentDisabled;

      String text = control.attrString("value", "")!;

      List<InlineSpan>? spans = parseTextSpans(
        Theme.of(context),
        viewModel,
        disabled,
        (String controlId, String eventName, String eventData) {
          backend.triggerControlEvent(controlId, eventName, eventData);
        },
      );
      String? semanticsLabel = control.attrString("semanticsLabel");
      bool noWrap = control.attrBool("noWrap", false)!;
      int? maxLines = control.attrInt("maxLines");

      TextStyle? style;
      var styleNameOrData = control.attrString("style", null);
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
      var styleName = control.attrString("theme_style", null);
      if (styleName != null) {
        themeStyle = getTextStyle(context, styleName);
      }

      if (style == null && themeStyle != null) {
        style = themeStyle;
      } else if (style != null && themeStyle != null) {
        style = themeStyle.merge(style);
      }

      var fontWeight = control.attrString("weight", "")!;

      List<FontVariation> variations = [];
      if (fontWeight.startsWith("w")) {
        variations
            .add(FontVariation('wght', parseDouble(fontWeight.substring(1))));
      }

      style = (style ?? const TextStyle()).copyWith(
        fontSize: control.attrDouble("size", null),
        fontWeight: getFontWeight(fontWeight),
        fontStyle: control.attrBool(
          "italic",
          false,
        )!
            ? FontStyle.italic
            : null,
        fontFamily: control.attrString("fontFamily"),
        fontVariations: variations,
        color: control.attrColor("color", context) ??
            (spans.isNotEmpty
                ? DefaultTextStyle.of(context).style.color
                : null),
        backgroundColor: control.attrColor("bgcolor", context),
      );

      TextAlign textAlign = parseTextAlign(
          control.attrString("textAlign", "")!, TextAlign.start)!;

      TextOverflow overflow = TextOverflow.values.firstWhere(
          (v) =>
              v.name.toLowerCase() ==
              control.attrString("overflow", "")!.toLowerCase(),
          orElse: () => TextOverflow.clip);

      return control.attrBool("selectable", false)!
          ? (spans.isNotEmpty)
              ? SelectableText.rich(
                  TextSpan(text: text, style: style, children: spans),
                  maxLines: maxLines,
                  textAlign: textAlign,
                )
              : SelectableText(
                  text,
                  semanticsLabel: semanticsLabel,
                  maxLines: maxLines,
                  style: style,
                  textAlign: textAlign,
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
