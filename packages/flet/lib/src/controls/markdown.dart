import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/box.dart';
import '../utils/images.dart';
import '../utils/launch_url.dart';
import '../utils/markdown.dart';
import '../utils/uri.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';
import 'highlight_view.dart';

class MarkdownControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final List<Control> children;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  static const String svgTag = " xmlns=\"http://www.w3.org/2000/svg\"";

  const MarkdownControl(
      {super.key,
      required this.parent,
      required this.children,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Markdown build: ${control.id}");
    bool disabled = control.isDisabled || parentDisabled;

    var value = control.attrString("value", "")!;
    md.ExtensionSet extensionSet = parseMarkdownExtensionSet(
        control.attrString("extensionSet"), md.ExtensionSet.none)!;

    var autoFollowLinks = control.attrBool("autoFollowLinks", false)!;
    var autoFollowLinksTarget = control.attrString("autoFollowLinksTarget");

    return withPageArgs((context, pageArgs) {
      bool selectable = control.attrBool("selectable", false)!;
      var codeStyleSheet = parseMarkdownStyleSheet(
              control, "codeStyleSheet", Theme.of(context), pageArgs) ??
          MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
              code: Theme.of(context)
                  .textTheme
                  .bodyMedium!
                  .copyWith(fontFamily: "monospace"));
      var mdStyleSheet = parseMarkdownStyleSheet(
          control, "mdStyleSheet", Theme.of(context), pageArgs);
      var codeTheme =
          parseMarkdownCodeTheme(control, "codeTheme", Theme.of(context));
      Widget markdown = MarkdownBody(
          data: value,
          selectable: selectable,
          imageDirectory: pageArgs.assetsDir != ""
              ? pageArgs.assetsDir
              : getBaseUri(pageArgs.pageUri!).toString(),
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
            var errorContentCtrls =
                children.where((c) => c.name == "error" && c.isVisible);

            var errorContent = errorContentCtrls.isNotEmpty
                ? createControl(control, errorContentCtrls.first.id, disabled)
                : null;

            return buildImage(
              context: context,
              control: control,
              src: src,
              srcBase64: srcBase64,
              semanticsLabel: alt,
              disabled: disabled,
              pageArgs: pageArgs,
              errorCtrl: errorContent,
            );
          },
          shrinkWrap: control.attrBool("shrinkWrap", true)!,
          fitContent: control.attrBool("fitContent", true)!,
          softLineBreak: control.attrBool("softLineBreak", false)!,
          onSelectionChanged: (String? text, TextSelection selection,
              SelectionChangedCause? cause) {
            debugPrint("Markdown ${control.id} selection changed");
            backend.triggerControlEvent(
                control.id,
                "selection_change",
                jsonEncode({
                  "text": text ?? "",
                  "start": selection.start,
                  "end": selection.end,
                  "base_offset": selection.baseOffset,
                  "extent_offset": selection.extentOffset,
                  "affinity": selection.affinity.name,
                  "directional": selection.isDirectional,
                  "collapsed": selection.isCollapsed,
                  "valid": selection.isValid,
                  "normalized": selection.isNormalized,
                  "cause": cause?.name ?? "unknown",
                }));
          },
          onTapText: () {
            debugPrint("Markdown ${control.id} text tapped");
            backend.triggerControlEvent(control.id, "tap_text");
          },
          onTapLink: (String text, String? href, String title) {
            debugPrint("Markdown ${control.id} link tapped clicked");
            if (autoFollowLinks && href != null) {
              openWebBrowser(href, webWindowName: autoFollowLinksTarget);
            }
            backend.triggerControlEvent(
                control.id, "tap_link", href?.toString());
          });

      return constrainedControl(context, markdown, parent, control);
    });
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
