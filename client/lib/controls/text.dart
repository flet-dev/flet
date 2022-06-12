import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/text.dart';
import 'create_control.dart';

class TextControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const TextControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");

    String text = control.attrString("value", "")!;
    bool noWrap = control.attrBool("noWrap", false)!;
    int? maxLines = control.attrInt("maxLines");

    TextStyle? style;
    var styleName = control.attrString("style", null);
    if (styleName != null) {
      style = getTextStyle(context, styleName);
    }

    style ??= TextStyle(
        fontSize: control.attrDouble("size", null),
        fontWeight: getFontWeight(control.attrString("weight", "")!),
        fontStyle: control.attrBool("italic", false)! ? FontStyle.italic : null,
        fontFamily: control.attrString("fontFamily"),
        color: HexColor.fromString(
            Theme.of(context), control.attrString("color", "")!),
        backgroundColor: HexColor.fromString(
            Theme.of(context), control.attrString("bgcolor", "")!));

    TextAlign? textAlign = TextAlign.values.firstWhere(
        (a) =>
            a.name.toLowerCase() ==
            control.attrString("textAlign", "")!.toLowerCase(),
        orElse: () => TextAlign.start);

    TextOverflow? overflow = TextOverflow.values.firstWhere(
        (v) =>
            v.name.toLowerCase() ==
            control.attrString("overflow", "")!.toLowerCase(),
        orElse: () => TextOverflow.fade);

    return constrainedControl(
        control.attrBool("selectable", false)!
            ? SelectableText(
                text,
                maxLines: maxLines,
                style: style,
                textAlign: textAlign,
              )
            : Text(
                text,
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
