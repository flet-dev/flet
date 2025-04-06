import 'package:flet/src/extensions/control.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class DataTableControl extends StatelessWidget {
  final Control control;

  const DataTableControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("DataTableControl build: ${control.id}");

    var bgColor = control.getString("bgcolor");
    var border = parseBorder(Theme.of(context), control, "border");
    var borderRadius = parseBorderRadius(control, "border_radius");
    var gradient = parseGradient(Theme.of(context), control, "gradient");
    var horizontalLines =
        parseBorderSide(Theme.of(context), control, "horizontal_lLines");
    var verticalLines =
        parseBorderSide(Theme.of(context), control, "vertical_lines");
    var defaultDecoration =
        Theme.of(context).dataTableTheme.decoration ?? const BoxDecoration();

    BoxDecoration? decoration;
    if (bgColor != null ||
        border != null ||
        borderRadius != null ||
        gradient != null) {
      decoration = (defaultDecoration as BoxDecoration).copyWith(
          color: parseColor(Theme.of(context), bgColor),
          border: border,
          borderRadius: borderRadius,
          gradient: gradient);
    }

    TableBorder? tableBorder;
    if (horizontalLines != null || verticalLines != null) {
      tableBorder = TableBorder(
          horizontalInside: horizontalLines ?? BorderSide.none,
          verticalInside: verticalLines ?? BorderSide.none);
    }

    Clip clipBehavior =
        parseClip(control.getString("clip_behavior"), Clip.none)!;

    var backend = FletBackend.of(context);

    var datatable = DataTable(
      decoration: decoration,
      border: tableBorder,
      clipBehavior: clipBehavior,
      checkboxHorizontalMargin: control.getDouble("checkbox_horizontal_margin"),
      columnSpacing: control.getDouble("column_spacing"),
      dataRowColor:
          parseWidgetStateColor(Theme.of(context), control, "data_row_color"),
      dataRowMinHeight: control.getDouble("data_row_min_height"),
      dataRowMaxHeight: control.getDouble("data_row_max_height"),
      dataTextStyle:
          parseTextStyle(Theme.of(context), control, "data_text_style"),
      headingRowColor: parseWidgetStateColor(
          Theme.of(context), control, "heading_row_color"),
      headingRowHeight: control.getDouble("heading_row_height"),
      headingTextStyle:
          parseTextStyle(Theme.of(context), control, "heading_text_style"),
      dividerThickness: control.getDouble("divider_thickness"),
      horizontalMargin: control.getDouble("horizontal_margin"),
      showBottomBorder: control.getBool("show_bottom_border", false)!,
      showCheckboxColumn: control.getBool("show_checkbox_column", false)!,
      sortAscending: control.getBool("sort_ascending", false)!,
      sortColumnIndex: control.getInt("sort_column_index"),
      onSelectAll: control.getBool("on_select_all", false)!
          ? (bool? selected) {
              backend.triggerControlEvent(control, "select_all", selected);
            }
          : null,
      columns: control.children("columns").map((column) {
        column.notifyParent = true;
        return DataColumn(
          numeric: column.getBool("numeric", false)!,
          tooltip: column.getString("tooltip"),
          headingRowAlignment:
              parseMainAxisAlignment(column.getString("heading_row_alignment")),
          mouseCursor: WidgetStateMouseCursor.clickable,
          onSort: column.getBool("on_sort", false)!
              ? (columnIndex, ascending) {
                  backend.triggerControlEvent(
                      column, "sort", {"i": columnIndex, "a": ascending});
                }
              : null,
          label: column.buildWidget("label")!,
        );
      }).toList(),
      rows: control.children("rows").map((row) {
        row.notifyParent = true;
        return DataRow(
          key: ValueKey(row.id),
          selected: row.getBool("selected", false)!,
          color: parseWidgetStateColor(Theme.of(context), row, "color"),
          onSelectChanged: row.getBool("on_select_changed", false)!
              ? (selected) {
                  backend.triggerControlEvent(row, "select_changed", selected);
                }
              : null,
          onLongPress: row.getBool("on_long_press", false)!
              ? () {
                  backend.triggerControlEvent(row, "long_press");
                }
              : null,
          cells: row.children("cells").map((cell) {
            cell.notifyParent = true;
            return DataCell(
              cell.buildWidget("content")!,
              placeholder: cell.getBool("placeholder", false)!,
              showEditIcon: cell.getBool("show_edit_icon", false)!,
              onDoubleTap: cell.getBool("on_double_tap", false)!
                  ? () {
                      backend.triggerControlEvent(cell, "double_tap");
                    }
                  : null,
              onLongPress: cell.getBool("on_long_press", false)!
                  ? () {
                      backend.triggerControlEvent(cell, "long_press");
                    }
                  : null,
              onTap: cell.getBool("on_tap", false)!
                  ? () {
                      backend.triggerControlEvent(cell, "tap");
                    }
                  : null,
              onTapCancel: cell.getBool("on_tap_cancel", false)!
                  ? () {
                      backend.triggerControlEvent(cell, "tap_cancel");
                    }
                  : null,
              onTapDown: cell.getBool("on_tap_down", false)!
                  ? (details) {
                      backend.triggerControlEvent(cell, "tap_down", {
                        "kind": details.kind?.name,
                        "lx": details.localPosition.dx,
                        "ly": details.localPosition.dy,
                        "gx": details.globalPosition.dx,
                        "gy": details.globalPosition.dy,
                      });
                    }
                  : null,
            );
          }).toList(),
        );
      }).toList(),
    );

    return ConstrainedControl(control: control, child: datatable);
  }
}
