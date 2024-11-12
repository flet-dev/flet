import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_highlight/theme_map.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../models/control.dart';
import '../models/page_args_model.dart';
import 'alignment.dart';
import 'box.dart';
import 'edge_insets.dart';
import 'numbers.dart';
import 'text.dart';

md.ExtensionSet? parseMarkdownExtensionSet(String? value,
    [md.ExtensionSet? defValue]) {
  if (value == null) {
    return defValue;
  }
  switch (value.toLowerCase()) {
    case "commonmark":
      return md.ExtensionSet.commonMark;
    case "githubweb":
      return md.ExtensionSet.gitHubWeb;
    case "githubflavored":
      return md.ExtensionSet.gitHubFlavored;
    default:
      return defValue;
  }
}

Map<String, TextStyle> parseMarkdownCodeTheme(
  Control control,
  String propName,
  ThemeData theme,
) {
  final v = control.attrString(propName);
  if (v == null) {
    return {};
  }
  dynamic j = json.decode(v);
  if (j is String) {
    return themeMap[j.toLowerCase()] ?? {};
  } else if (j is Map<String, dynamic>) {
    String transformKey(String key) {
      switch (key) {
        case 'class_name':
          return 'class';
        case 'built_in':
          return key;
        default:
          return key.replaceAll('_', '-');
      }
    }

    final resultMap =
        j.map((key, value) => MapEntry(key, textStyleFromJson(theme, value)));
    resultMap.removeWhere(
        (key, value) => value == null); // remove entries with null values
    return resultMap.map((key, value) => MapEntry(transformKey(key), value!));
  }
  return {};
}

MarkdownStyleSheet? parseMarkdownStyleSheet(Control control, String propName,
    ThemeData theme, PageArgsModel? pageArgs) {
  var v = control.attrString(propName);
  if (v == null) {
    return null;
  }
  dynamic j = json.decode(v);
  return markdownStyleSheetFromJson(theme, j, pageArgs);
}

MarkdownStyleSheet markdownStyleSheetFromJson(
    ThemeData theme, Map<String, dynamic> j, PageArgsModel? pageArgs) {
  TextStyle? parseTextStyle(String propName) {
    return j[propName] != null ? textStyleFromJson(theme, j[propName]) : null;
  }

  return MarkdownStyleSheet.fromTheme(theme).copyWith(
    a: parseTextStyle("a_text_style") ?? const TextStyle(color: Colors.blue),
    p: parseTextStyle("p_text_style") ?? theme.textTheme.bodyMedium,
    pPadding: edgeInsetsFromJson(j["p_padding"], EdgeInsets.zero)!,
    code: parseTextStyle("code_text_style") ??
        theme.textTheme.bodyMedium!.copyWith(fontFamily: "monospace"),
    h1: parseTextStyle("h1_text_style") ?? theme.textTheme.headlineSmall,
    h1Padding: edgeInsetsFromJson(j["h1_padding"], EdgeInsets.zero)!,
    h2: parseTextStyle("h2_text_style") ?? theme.textTheme.titleLarge,
    h2Padding: edgeInsetsFromJson(j["h2_padding"], EdgeInsets.zero)!,
    h3: parseTextStyle("h3_text_style") ?? theme.textTheme.titleMedium,
    h3Padding: edgeInsetsFromJson(j["h3_padding"], EdgeInsets.zero)!,
    h4: parseTextStyle("h4_text_style") ?? theme.textTheme.bodyLarge,
    h4Padding: edgeInsetsFromJson(j["h4_padding"], EdgeInsets.zero)!,
    h5: parseTextStyle("h5_text_style") ?? theme.textTheme.bodyLarge,
    h5Padding: edgeInsetsFromJson(j["h5_padding"], EdgeInsets.zero)!,
    h6: parseTextStyle("h6_text_style") ?? theme.textTheme.bodyLarge,
    h6Padding: edgeInsetsFromJson(j["h6_padding"], EdgeInsets.zero)!,
    em: parseTextStyle("em_text_style") ??
        const TextStyle(fontStyle: FontStyle.italic),
    strong: parseTextStyle("strong_text_style") ??
        const TextStyle(fontWeight: FontWeight.bold),
    del: parseTextStyle("del_text_style") ??
        const TextStyle(decoration: TextDecoration.lineThrough),
    blockquote:
        parseTextStyle("blockquote_text_style") ?? theme.textTheme.bodyMedium,
    img: parseTextStyle("img_text_style") ?? theme.textTheme.bodyMedium,
    checkbox: parseTextStyle("checkbox_text_style") ??
        theme.textTheme.bodyMedium!.copyWith(
          color: theme.primaryColor,
        ),
    blockSpacing: parseDouble(j["block_spacing"], 8.0)!,
    listIndent: parseDouble(j["list_indent"], 24.0)!,
    listBullet:
        parseTextStyle("list_bullet_text_style") ?? theme.textTheme.bodyMedium,
    listBulletPadding: edgeInsetsFromJson(
        j["list_bullet_padding"], const EdgeInsets.only(right: 4))!,
    tableHead: parseTextStyle("table_head_text_style") ??
        const TextStyle(fontWeight: FontWeight.w600),
    tableBody:
        parseTextStyle("table_body_text_style") ?? theme.textTheme.bodyMedium,
    tableHeadAlign:
        parseTextAlign(j["table_head_text_align"], TextAlign.center)!,
    tablePadding: edgeInsetsFromJson(
        j["table_padding"], const EdgeInsets.only(bottom: 4.0))!,
    tableBorder: TableBorder.all(
      color: theme.dividerColor,
    ),
    tableColumnWidth: const FlexColumnWidth(),
    tableCellsPadding: edgeInsetsFromJson(
        j["table_cells_padding"], const EdgeInsets.fromLTRB(16, 8, 16, 8))!,
    tableCellsDecoration:
        boxDecorationFromJSON(theme, j["table_cells_decoration"], pageArgs) ??
            const BoxDecoration(),
    blockquotePadding: edgeInsetsFromJson(j["blockquote_padding"]) ??
        const EdgeInsets.all(8.0),
    blockquoteDecoration:
        boxDecorationFromJSON(theme, j["blockquote_decoration"], pageArgs) ??
            BoxDecoration(
              color: Colors.blue.shade100,
              borderRadius: BorderRadius.circular(2.0),
            ),
    codeblockPadding:
        edgeInsetsFromJson(j["codeblock_padding"], const EdgeInsets.all(8.0))!,
    codeblockDecoration:
        boxDecorationFromJSON(theme, j["codeblock_decoration"], pageArgs) ??
            BoxDecoration(
              color: theme.cardTheme.color ?? theme.cardColor,
              borderRadius: BorderRadius.circular(2.0),
            ),
    horizontalRuleDecoration: boxDecorationFromJSON(
            theme, j["horizontal_rule_decoration"], pageArgs) ??
        BoxDecoration(
          border: Border(
            top: BorderSide(
              width: 5.0,
              color: theme.dividerColor,
            ),
          ),
        ),
    blockquoteAlign:
        parseWrapAlignment(j["blockquote_alignment"], WrapAlignment.start)!,
    codeblockAlign:
        parseWrapAlignment(j["codeblock_alignment"], WrapAlignment.start)!,
    h1Align: parseWrapAlignment(j["h1_alignment"], WrapAlignment.start)!,
    h2Align: parseWrapAlignment(j["h2_alignment"], WrapAlignment.start)!,
    h3Align: parseWrapAlignment(j["h3_alignment"], WrapAlignment.start)!,
    h4Align: parseWrapAlignment(j["h4_alignment"], WrapAlignment.start)!,
    h5Align: parseWrapAlignment(j["h5_alignment"], WrapAlignment.start)!,
    h6Align: parseWrapAlignment(j["h6_alignment"], WrapAlignment.start)!,
    textAlign: parseWrapAlignment(j["text_alignment"], WrapAlignment.start)!,
    orderedListAlign:
        parseWrapAlignment(j["ordered_list_alignment"], WrapAlignment.start)!,
    unorderedListAlign:
        parseWrapAlignment(j["unordered_list_alignment"], WrapAlignment.start)!,
  );
}
