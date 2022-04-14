import 'package:flet_view/controls/create_control.dart';
import 'package:flet_view/utils/colors.dart';
import 'package:flet_view/utils/text.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';

class TextControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const TextControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Text build: ${control.id}");

    String text = control.attrString("value", "")!;

    TextStyle? style;
    var styleName = control.attrString("style", null);
    if (styleName != null) {
      style = getTextStyle(context, styleName);
    }

    style ??= TextStyle(
        fontSize: control.attrDouble("size", null),
        fontWeight: getFontWeight(control.attrString("weight", "")!),
        fontStyle: control.attrBool("italic", false)! ? FontStyle.italic : null,
        color: HexColor.fromNamedColor(control.attrString("color", "")!),
        backgroundColor:
            HexColor.fromNamedColor(control.attrString("bgcolor", "")!));

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

    return commonControl(
        control.attrBool("selectable", false)!
            ? SelectableText(
                text,
                style: style,
                textAlign: textAlign,
              )
            : Text(
                text,
                style: style,
                textAlign: textAlign,
                overflow: overflow,
              ),
        parent,
        control);
  }
}
