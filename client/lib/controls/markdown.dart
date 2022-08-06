import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class MarkdownControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const MarkdownControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Markdown build: ${control.id}");

    var value = control.attrString("value", "")!;

    Widget markdown = Markdown(
        data: value,
        selectable: control.attrBool("selectable", false)!,
        imageDirectory: 'https://raw.githubusercontent.com',
        extensionSet: md.ExtensionSet.gitHubFlavored,
        onTapLink: (String text, String? href, String title) {
          // todo
        },
        padding:
            parseEdgeInsets(control, "padding") ?? const EdgeInsets.all(0));

    return constrainedControl(markdown, parent, control);
  }
}
