import 'package:flutter/material.dart';
import 'package:flutter_highlight/theme_map.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:markdown/markdown.dart' as md;

import '../models/control.dart';
import 'alignment.dart';
import 'box.dart';
import 'edge_insets.dart';
import 'numbers.dart';
import 'text.dart';

md.ExtensionSet? parseMarkdownExtensionSet(String? value,
    [md.ExtensionSet? defaultValue]) {
  if (value == null) return defaultValue;
  switch (value.toLowerCase()) {
    case "commonmark":
      return md.ExtensionSet.commonMark;
    case "githubweb":
      return md.ExtensionSet.gitHubWeb;
    case "githubflavored":
      return md.ExtensionSet.gitHubFlavored;
    default:
      return defaultValue;
  }
}

Map<String, TextStyle> parseMarkdownCodeTheme(dynamic value, ThemeData theme) {
  if (value == null) return {};
  if (value is String) return themeMap[value.toLowerCase()] ?? {};
  if (value is Map<String, dynamic>) {
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
        value.map((key, value) => MapEntry(key, parseTextStyle(value, theme)));
    resultMap.removeWhere(
        (key, value) => value == null); // remove entries with null values
    return resultMap.map((key, value) => MapEntry(transformKey(key), value!));
  }
  return {};
}

MarkdownStyleSheet? parseMarkdownStyleSheet(dynamic value, BuildContext context,
    [MarkdownStyleSheet? defaultValue]) {
  if (value == null) return null;
  var theme = Theme.of(context);
  return MarkdownStyleSheet.fromTheme(theme).copyWith(
    a: parseTextStyle(
        value["a_text_style"], theme, const TextStyle(color: Colors.blue))!,
    p: parseTextStyle(value["p_text_style"], theme, theme.textTheme.bodyMedium),
    pPadding: parsePadding(value["p_padding"], EdgeInsets.zero)!,
    code: parseTextStyle(value["code_text_style"], theme,
        theme.textTheme.bodyMedium!.copyWith(fontFamily: "monospace")),
    h1: parseTextStyle(value["h1_text_style"], theme) ??
        theme.textTheme.headlineSmall,
    h1Padding: parsePadding(value["h1_padding"], EdgeInsets.zero)!,
    h2: parseTextStyle(
        value["h2_text_style"], theme, theme.textTheme.titleLarge),
    h2Padding: parsePadding(value["h2_padding"], EdgeInsets.zero)!,
    h3: parseTextStyle(
        value["h3_text_style"], theme, theme.textTheme.titleMedium),
    h3Padding: parsePadding(value["h3_padding"], EdgeInsets.zero)!,
    h4: parseTextStyle(
        value["h4_text_style"], theme, theme.textTheme.bodyLarge),
    h4Padding: parsePadding(value["h4_padding"], EdgeInsets.zero)!,
    h5: parseTextStyle(
        value["h5_text_style"], theme, theme.textTheme.bodyLarge),
    h5Padding: parsePadding(value["h5_padding"], EdgeInsets.zero)!,
    h6: parseTextStyle(
        value["h6_text_style"], theme, theme.textTheme.bodyLarge),
    h6Padding: parsePadding(value["h6_padding"], EdgeInsets.zero)!,
    em: parseTextStyle(value["em_text_style"], theme,
        const TextStyle(fontStyle: FontStyle.italic))!,
    strong: parseTextStyle(value["strong_text_style"], theme,
        const TextStyle(fontWeight: FontWeight.bold))!,
    del: parseTextStyle(value["del_text_style"], theme,
        const TextStyle(decoration: TextDecoration.lineThrough)),
    blockquote: parseTextStyle(
        value["blockquote_text_style"], theme, theme.textTheme.bodyMedium),
    img: parseTextStyle(
        value["img_text_style"], theme, theme.textTheme.bodyMedium),
    checkbox: parseTextStyle(value["checkbox_text_style"], theme,
        theme.textTheme.bodyMedium!.copyWith(color: theme.primaryColor)),
    blockSpacing: parseDouble(value["block_spacing"], 8.0)!,
    listIndent: parseDouble(value["list_indent"], 24.0)!,
    listBullet: parseTextStyle(
        value["list_bullet_text_style"], theme, theme.textTheme.bodyMedium),
    listBulletPadding: parsePadding(
        value["list_bullet_padding"], const EdgeInsets.only(right: 4))!,
    tableHead: parseTextStyle(value["table_head_text_style"], theme,
        const TextStyle(fontWeight: FontWeight.w600))!,
    tableBody: parseTextStyle(
        value["table_body_text_style"], theme, theme.textTheme.bodyMedium),
    tableHeadAlign:
        parseTextAlign(value["table_head_text_align"], TextAlign.center)!,
    tablePadding: parsePadding(
        value["table_padding"], const EdgeInsets.only(bottom: 4.0))!,
    tableBorder: TableBorder.all(color: theme.dividerColor),
    tableColumnWidth: const FlexColumnWidth(),
    tableCellsPadding: parsePadding(
        value["table_cells_padding"], const EdgeInsets.fromLTRB(16, 8, 16, 8))!,
    tableCellsDecoration: parseBoxDecoration(
        value["table_cells_decoration"], context, const BoxDecoration()),
    blockquotePadding:
        parsePadding(value["blockquote_padding"], const EdgeInsets.all(8.0))!,
    blockquoteDecoration: parseBoxDecoration(
        value["blockquote_decoration"],
        context,
        BoxDecoration(
            color: Colors.blue.shade100,
            borderRadius: BorderRadius.circular(2.0)))!,
    codeblockPadding:
        parsePadding(value["codeblock_padding"], const EdgeInsets.all(8.0))!,
    codeblockDecoration: parseBoxDecoration(
        value["codeblock_decoration"],
        context,
        BoxDecoration(
            color: theme.cardTheme.color ?? theme.cardColor,
            borderRadius: BorderRadius.circular(2.0)))!,
    horizontalRuleDecoration: parseBoxDecoration(
        value["horizontal_rule_decoration"],
        context,
        BoxDecoration(
            border: Border(
                top: BorderSide(width: 5.0, color: theme.dividerColor))))!,
    blockquoteAlign:
        parseWrapAlignment(value["blockquote_alignment"], WrapAlignment.start)!,
    codeblockAlign:
        parseWrapAlignment(value["codeblock_alignment"], WrapAlignment.start)!,
    h1Align: parseWrapAlignment(value["h1_alignment"], WrapAlignment.start)!,
    h2Align: parseWrapAlignment(value["h2_alignment"], WrapAlignment.start)!,
    h3Align: parseWrapAlignment(value["h3_alignment"], WrapAlignment.start)!,
    h4Align: parseWrapAlignment(value["h4_alignment"], WrapAlignment.start)!,
    h5Align: parseWrapAlignment(value["h5_alignment"], WrapAlignment.start)!,
    h6Align: parseWrapAlignment(value["h6_alignment"], WrapAlignment.start)!,
    textAlign:
        parseWrapAlignment(value["text_alignment"], WrapAlignment.start)!,
    orderedListAlign: parseWrapAlignment(
        value["ordered_list_alignment"], WrapAlignment.start)!,
    unorderedListAlign: parseWrapAlignment(
        value["unordered_list_alignment"], WrapAlignment.start)!,
  );
}

extension MarkdownParsers on Control {
  Map<String, TextStyle> getMarkdownCodeTheme(
      String propertyName, ThemeData theme) {
    return parseMarkdownCodeTheme(get(propertyName), theme);
  }

  md.ExtensionSet? getMarkdownExtensionSet(String propertyName,
      [md.ExtensionSet? defaultValue]) {
    return parseMarkdownExtensionSet(get(propertyName), defaultValue);
  }

  MarkdownStyleSheet? getMarkdownStyleSheet(
      String propertyName, BuildContext context,
      [MarkdownStyleSheet? defaultValue]) {
    return parseMarkdownStyleSheet(get(propertyName), context, defaultValue);
  }
}
