import 'dart:convert';
import 'dart:io' as io;

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_highlight/theme_map.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:flutter_svg/svg.dart';
import 'package:markdown/markdown.dart' as md;

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/collections.dart';
import '../utils/images.dart';
import '../utils/launch_url.dart';
import '../utils/markdown.dart';
import '../utils/text.dart';
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
    var codeTheme = control.attrString("codeTheme", "")!;
    md.ExtensionSet extensionSet = parseMarkdownExtensionSet(
        control.attrString("extensionSet"), md.ExtensionSet.none)!;

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
          imageBuilder: (Uri uri, String? title, String? alt) {
            Widget? image;
            String s = uri.toString();
            var srcBase64 = isBase64ImageString(s) ? s : null;
            var src = isUrlOrPath(s) ? s : null;
            var errorContentCtrls =
                children.where((c) => c.name == "error" && c.isVisible);

            if (srcBase64 != null) {
              try {
                Uint8List bytes = base64Decode(srcBase64);
                if (arrayIndexOf(
                        bytes, Uint8List.fromList(utf8.encode(svgTag))) !=
                    -1) {
                  image = SvgPicture.memory(bytes,
                      fit: BoxFit.contain, semanticsLabel: alt);
                } else {
                  image = Image.memory(bytes, semanticLabel: alt);
                }
              } catch (ex) {
                return ErrorControl("Error decoding base64: ${ex.toString()}");
              }
            } else if (src != null) {
              if (src.contains(svgTag)) {
                image = SvgPicture.memory(Uint8List.fromList(utf8.encode(src)),
                    fit: BoxFit.contain, semanticsLabel: alt);
              } else {
                var assetSrc =
                    getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);

                if (assetSrc.isFile) {
                  // from File
                  if (assetSrc.path.endsWith(".svg")) {
                    image = getSvgPictureFromFile(
                        src: assetSrc.path,
                        fit: BoxFit.contain,
                        blendMode: BlendMode.srcIn,
                        semanticsLabel: alt,
                        width: null,
                        height: null,
                        color: null);
                  } else {
                    image = Image.file(
                      io.File(assetSrc.path),
                      errorBuilder: errorContentCtrls.isNotEmpty
                          ? (context, error, stackTrace) {
                              return createControl(control,
                                  errorContentCtrls.first.id, disabled);
                            }
                          : null,
                    );
                  }
                } else {
                  // URL
                  if (assetSrc.path.endsWith(".svg")) {
                    image = SvgPicture.network(assetSrc.path,
                        fit: BoxFit.contain, semanticsLabel: alt);
                  } else {
                    image = Image.network(assetSrc.path,
                        semanticLabel: alt,
                        errorBuilder: errorContentCtrls.isNotEmpty
                            ? (context, error, stackTrace) {
                                return createControl(control,
                                    errorContentCtrls.first.id, disabled);
                              }
                            : null);
                  }
                }
              }
            } else {
              // src == null && srcBase64 == null
              return ErrorControl("Invalid image source: $s");
            }

            return image;
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
