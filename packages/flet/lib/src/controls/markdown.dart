import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/box.dart';
import '../utils/images.dart';
import '../utils/launch_url.dart';
import '../utils/markdown.dart';
import '../utils/numbers.dart';
import '../utils/uri.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
import 'highlight_view.dart';

class MarkdownControl extends StatelessWidget {
  final Control control;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const MarkdownControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Markdown build: ${control.id}");

    var value = control.getString("value", "")!;
    md.ExtensionSet extensionSet =
        control.getMarkdownExtensionSet("extension_set", md.ExtensionSet.none)!;

    var autoFollowLinks = control.getBool("auto_follow_links", false)!;
    var autoFollowLinksTarget = control.getString("auto_follow_links_target");

    bool selectable = control.getBool("selectable", false)!;
    var codeStyleSheet =
        control.getMarkdownStyleSheet("code_style_sheet", context) ??
            MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
                code: Theme.of(context)
                    .textTheme
                    .bodyMedium!
                    .copyWith(fontFamily: "monospace"));
    var mdStyleSheet = control.getMarkdownStyleSheet("md_style_sheet", context);
    var codeTheme =
        control.getMarkdownCodeTheme("code_theme", Theme.of(context));
    Widget markdown = MarkdownBody(
        data: value,
        selectable: selectable,
        imageDirectory: control.backend.assetsDir != ""
            ? control.backend.assetsDir
            : getBaseUri(control.backend.pageUri).toString(),
        extensionSet: extensionSet,
        builders: {
          'code': CodeElementBuilder(codeTheme, codeStyleSheet, selectable),
        },
        styleSheet: mdStyleSheet,
        imageBuilder: (Uri uri, String? title, String? alt) {
          String s = uri.toString();
          var srcBase64 = isBase64ImageString(s) ? s : null;
          var src = isUrlOrPath(s) ? s : null;
          if (src == null && srcBase64 == null) {
            return ErrorControl("Invalid image URI: $s");
          }

          return buildImage(
              context: context,
              src: src,
              srcBase64: srcBase64,
              semanticsLabel: alt,
              disabled: control.disabled,
              errorCtrl: control.buildWidget("image_error_content"));
        },
        shrinkWrap: control.getBool("shrink_wrap", true)!,
        fitContent: control.getBool("fit_content", true)!,
        softLineBreak: control.getBool("soft_line_break", false)!,
        onSelectionChanged: (String? text, TextSelection selection,
            SelectionChangedCause? cause) {
          control.triggerEvent("selection_change", {
            "text": text ?? "",
            "cause": cause?.name ?? "unknown",
            "selection": {
              "start": selection.start,
              "end": selection.end,
              "selection": text ?? "",
              "base_offset": selection.baseOffset,
              "extent_offset": selection.extentOffset,
              "affinity": selection.affinity.name,
              "directional": selection.isDirectional,
              "collapsed": selection.isCollapsed,
              "valid": selection.isValid,
              "normalized": selection.isNormalized,
            },
          });
        },
        onTapText: () => control.triggerEvent("tap_text"),
        onTapLink: (String text, String? href, String title) {
          if (autoFollowLinks && href != null) {
            openWebBrowser(Url(href, autoFollowLinksTarget));
          }
          control.triggerEvent("tap_link", href);
        });

    return ConstrainedControl(control: control, child: markdown);
  }
}

class CodeElementBuilder extends MarkdownElementBuilder {
  final Map<String, TextStyle> codeTheme;
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
          theme: codeTheme,
          padding: mdStyleSheet.codeblockPadding,
          decoration: mdStyleSheet.codeblockDecoration,
          textStyle: mdStyleSheet.code,

          selectable: selectable,
        ),
      );
    });
  }
}
