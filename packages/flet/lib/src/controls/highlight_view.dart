import 'package:flutter/material.dart';
import 'package:highlight/highlight.dart' show highlight, Node;

/// Highlight Flutter Widget
class HighlightView extends StatelessWidget {
  /// The original code to be highlighted
  final String source;

  /// Highlight language
  ///
  /// It is recommended to give it a value for performance
  ///
  /// [All available languages](https://github.com/pd4d10/highlight/tree/master/highlight/lib/languages)
  final String? language;

  /// Highlight theme
  ///
  /// [All available themes](https://github.com/pd4d10/highlight/blob/master/flutter_highlight/lib/themes)
  final Map<String, TextStyle> theme;

  /// Padding
  final EdgeInsetsGeometry? padding;

  final Decoration? decoration;

  /// Text styles
  ///
  /// Specify text styles such as font family and font size
  final TextStyle? textStyle;

  final bool selectable;

  HighlightView(String input,
      {super.key,
      this.language,
      this.theme = const {},
      this.padding,
      this.decoration,
      this.textStyle,
      int tabSize = 8, // TODO: https://github.com/flutter/flutter/issues/50087
      this.selectable = false})
      : source = input.replaceAll('\t', ' ' * tabSize);

  List<TextSpan> _convert(List<Node> nodes) {
    List<TextSpan> spans = [];
    var currentSpans = spans;
    List<List<TextSpan>> stack = [];

    traverse(Node node) {
      if (node.value != null) {
        currentSpans.add(node.className == null
            ? TextSpan(text: node.value)
            : TextSpan(text: node.value, style: theme[node.className!]));
      } else if (node.children != null) {
        List<TextSpan> tmp = [];
        currentSpans
            .add(TextSpan(children: tmp, style: theme[node.className!]));
        stack.add(currentSpans);
        currentSpans = tmp;

        for (var n in node.children!) {
          traverse(n);
          if (n == node.children!.last) {
            currentSpans = stack.isEmpty ? spans : stack.removeLast();
          }
        }
      }
    }

    for (var node in nodes) {
      traverse(node);
    }

    return spans;
  }

  static const _rootKey = 'root';

  // TODO: dart:io is not available at web platform currently
  // See: https://github.com/flutter/flutter/issues/39998
  // So we just use monospace here for now
  static const _defaultFontFamily = 'monospace';

  @override
  Widget build(BuildContext context) {
    var style = TextStyle(
      fontFamily: _defaultFontFamily,
      color: theme[_rootKey]?.color ??
          Theme.of(context).colorScheme.onSurfaceVariant,
    );
    if (textStyle != null) {
      style = style.merge(textStyle);
    }

    var d = BoxDecoration(
        color: theme[_rootKey]?.backgroundColor ??
            Theme.of(context).colorScheme.surfaceVariant);

    if (decoration != null) {
      d = d.copyWith(borderRadius: (decoration as BoxDecoration).borderRadius);
    }

    return Container(
      padding: padding,
      decoration: d,
      child: selectable
          ? SelectableText.rich(TextSpan(
              style: style,
              children:
                  _convert(highlight.parse(source, language: language).nodes!),
            ))
          : Text.rich(
              TextSpan(
                style: style,
                children: _convert(
                    highlight.parse(source, language: language).nodes!),
              ),
            ),
    );
  }
}
