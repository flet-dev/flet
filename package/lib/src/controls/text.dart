import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_tree_view_model.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'create_control.dart';

class TextControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const TextControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    var result = StoreConnector<AppState, ControlTreeViewModel>(
        distinct: true,
        converter: (store) => ControlTreeViewModel.fromStore(store, control),
        builder: (context, viewModel) {
          debugPrint("Text build: ${control.id}");

          bool disabled = control.isDisabled || parentDisabled;

          String text = control.attrString("value", "")!;
          List<InlineSpan>? spans = parseTextSpans(Theme.of(context), viewModel,
              disabled, FletAppServices.of(context).server);
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
            variations.add(
                FontVariation('wght', parseDouble(fontWeight.substring(1))));
          }

          style = (style ?? const TextStyle()).copyWith(
              fontSize: control.attrDouble("size", null),
              fontWeight: getFontWeight(fontWeight),
              fontStyle:
                  control.attrBool("italic", false)! ? FontStyle.italic : null,
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
