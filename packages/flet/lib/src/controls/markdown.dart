import 'package:flutter/material.dart';
import 'package:flutter_highlight/theme_map.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/launch_url.dart';
import '../utils/text.dart';
import '../utils/uri.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';
import 'highlight_view.dart';

class MarkdownControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const MarkdownControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Markdown build: ${control.id}");

    var value = control.attrString("value", "")!;
    var codeTheme = control.attrString("codeTheme", "")!;
    md.ExtensionSet extensionSet = md.ExtensionSet.none;
    switch (control.attrString("extensionSet", "")!.toLowerCase()) {
      case "commonmark":
        extensionSet = md.ExtensionSet.commonMark;
        break;
      case "githubweb":
        extensionSet = md.ExtensionSet.gitHubWeb;
        break;
      case "githubflavored":
        extensionSet = md.ExtensionSet.gitHubFlavored;
        break;
    }

    TextStyle? codeStyle =
        parseTextStyle(Theme.of(context), control, "codeStyle");

    var mdStyleSheet = MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
        code: codeStyle ??
            Theme.of(context)
                .textTheme
                .bodyMedium!
                .copyWith(fontFamily: "monospace"));

    var autoFollowLinks = control.attrBool("autoFollowLinks", false)!;
    var autoFollowLinksTarget = control.attrString("autoFollowLinksTarget");

    return withPageArgs((context, pageArgs) {
      bool selectable = control.attrBool("selectable", false)!;
      Widget markdown = MarkdownBody(
          data: value,
          selectable: selectable,
          imageDirectory: pageArgs.assetsDir != ""
              ? pageArgs.assetsDir
              : getBaseUri(pageArgs.pageUri!).toString(),
          extensionSet: extensionSet,
          builders: {
            'code': CodeElementBuilder(
                codeTheme.toLowerCase(), mdStyleSheet, selectable),
          },
          styleSheet: mdStyleSheet,
          onTapLink: (String text, String? href, String title) {
            debugPrint("Markdown link tapped ${control.id} clicked: $href");
            if (autoFollowLinks && href != null) {
              openWebBrowser(href, webWindowName: autoFollowLinksTarget);
            }
            backend.triggerControlEvent(
                control.id, "tap_link", href?.toString() ?? "");
          });

      return constrainedControl(context, markdown, parent, control);
    });
  }
}

class CodeElementBuilder extends MarkdownElementBuilder {
  final String codeTheme;
  final MarkdownStyleSheet mdStyleSheet;
  final bool selectable;

  CodeElementBuilder(this.codeTheme, this.mdStyleSheet, this.selectable);

  @override
  Widget? visitElementAfter(md.Element element, TextStyle? preferredStyle) {
    if (!element.textContent.endsWith('\n')) {
      return null;
    }

    var language = '';
    if (element.attributes['class'] != null) {
      String lg = element.attributes['class'] as String;
      language = lg.substring(9);
    }

    return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
      return SizedBox(
        width:
            (constraints.maxWidth == double.infinity) ? 10000 : double.infinity,
        child: HighlightView(
          // The original code to be highlighted
          element.textContent.substring(0, element.textContent.length - 1),

          // Specify language
          // It is recommended to give it a value for performance
          language: language,

          // Specify highlight theme
          // All available themes are listed in `themes` folder
          theme: themeMap[codeTheme] ?? {},

          // Specify padding
          padding: mdStyleSheet.codeblockPadding,

          decoration: mdStyleSheet.codeblockDecoration,

          // Specify text style
          textStyle: mdStyleSheet.code,

          selectable: selectable,
        ),
      );
    });
  }
}
