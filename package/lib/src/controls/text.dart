import 'dart:ui';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_control_stateless_mixin.dart';
import 'flet_store_mixin.dart';

class TextControl extends StatelessWidget
    with FletControlStatelessMixin, FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const TextControl({
    super.key,
    required this.parent,
    required this.control,
    required this.parentDisabled,
  });

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
          sendControlEvent(context, controlId, eventName, eventData);
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
          color: HexColor.fromString(
                  Theme.of(context), control.attrString("color", "")!) ??
              (spans.isNotEmpty
                  ? DefaultTextStyle.of(context).style.color
                  : null),
          backgroundColor: HexColor.fromString(
              Theme.of(context), control.attrString("bgcolor", "")!));

      TextAlign textAlign = TextAlign.values.firstWhere(
          (a) =>
              a.name.toLowerCase() ==
              control.attrString("textAlign", "")!.toLowerCase(),
          orElse: () => TextAlign.start);

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
              ? RichText(
                  text: TextSpan(text: text, style: style, children: spans),
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
