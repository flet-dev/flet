import 'dart:ui';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'create_control.dart';

class TextControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const TextControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");

    String text = control.attrString("value", "")!;
    List<TextSpan>? spans = parseTextSpans(Theme.of(context), control, "spans");
    String? semanticsLabel = control.attrString("semanticsLabel");
    bool noWrap = control.attrBool("noWrap", false)!;
    int? maxLines = control.attrInt("maxLines");

    TextStyle? style;
    var styleName = control.attrString("style", null);
    if (styleName != null) {
      style = getTextStyle(context, styleName);
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
        fontStyle: control.attrBool("italic", false)! ? FontStyle.italic : null,
        fontFamily: control.attrString("fontFamily"),
        fontVariations: variations,
        color: HexColor.fromString(
                Theme.of(context), control.attrString("color", "")!) ??
            Theme.of(context).textTheme.bodyMedium!.color,
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

    return constrainedControl(
        context,
        control.attrBool("selectable", false)!
            ? SelectableText(
                text,
                semanticsLabel: semanticsLabel,
                maxLines: maxLines,
                style: style,
                textAlign: textAlign,
              )
            : (spans != null && spans.isNotEmpty)
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
                  ),
        parent,
        control);
  }
}
