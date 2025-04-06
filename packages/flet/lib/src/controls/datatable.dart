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

    var bgColor = control.getString("bgColor");
    var border = parseBorder(Theme.of(context), control, "border");
    var borderRadius = parseBorderRadius(control, "borderRadius");
    var gradient = parseGradient(Theme.of(context), control, "gradient");
    var horizontalLines =
        parseBorderSide(Theme.of(context), control, "horizontalLines");
    var verticalLines =
        parseBorderSide(Theme.of(context), control, "verticalLines");
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
        parseClip(control.getString("clipBehavior"), Clip.none)!;

    var backend = FletBackend.of(context);

    var datatable = DataTable(
        decoration: decoration,
        border: tableBorder,
        clipBehavior: clipBehavior,
        checkboxHorizontalMargin: control.getDouble("checkboxHorizontalMargin"),
        columnSpacing: control.getDouble("columnSpacing"),
        dataRowColor:
            parseWidgetStateColor(Theme.of(context), control, "dataRowColor"),
        dataRowMinHeight: control.getDouble("dataRowMinHeight"),
        dataRowMaxHeight: control.getDouble("dataRowMaxHeight"),
        dataTextStyle:
            parseTextStyle(Theme.of(context), control, "dataTextStyle"),
        headingRowColor: parseWidgetStateColor(
            Theme.of(context), control, "headingRowColor"),
        headingRowHeight: control.getDouble("headingRowHeight"),
        headingTextStyle:
            parseTextStyle(Theme.of(context), control, "headingTextStyle"),
        dividerThickness: control.getDouble("dividerThickness"),
        horizontalMargin: control.getDouble("horizontalMargin"),
        showBottomBorder: control.getBool("showBottomBorder", false)!,
        showCheckboxColumn: control.getBool("showCheckboxColumn", false)!,
        sortAscending: control.getBool("sortAscending", false)!,
        sortColumnIndex: control.getInt("sortColumnIndex"),
        onSelectAll: control.getBool("onSelectAll", false)!
            ? (bool? selected) {
                backend.triggerControlEvent(control, "select_all", selected);
              }
            : null,
        columns: control.children("columns").map((column) {
          column.notifyParent = true;
          return DataColumn(
              numeric: column.getBool("numeric", false)!,
              tooltip: column.getString("tooltip"),
              headingRowAlignment: parseMainAxisAlignment(
                  column.getString("headingRowAlignment")),
              mouseCursor: WidgetStateMouseCursor.clickable,
              onSort: column.getBool("onSort", false)!
                  ? (columnIndex, ascending) {
                      backend.triggerControlEvent(
                          column, "sort", {"i": columnIndex, "a": ascending});
                    }
                  : null,
              label: column.buildWidget("label")!);
        }).toList(),
        rows: control.children("rows").map((row) {
          row.notifyParent = true;
          return DataRow(
              key: ValueKey(row.id),
              selected: row.getBool("selected", false)!,
              color: parseWidgetStateColor(Theme.of(context), row, "color"),
              onSelectChanged: row.getBool("onSelectChanged", false)!
                  ? (selected) {
                      backend.triggerControlEvent(
                          row, "select_changed", selected);
                    }
                  : null,
              onLongPress: row.getBool("onLongPress", false)!
                  ? () {
                      backend.triggerControlEvent(row, "long_press");
                    }
                  : null,
              cells: row.children("cells").map((cell) {
                cell.notifyParent = true;
                return DataCell(
                  cell.buildWidget("content")!,
                  placeholder: cell.getBool("placeholder", false)!,
                  showEditIcon: cell.getBool("showEditIcon", false)!,
                  onDoubleTap: cell.getBool("onDoubleTap", false)!
                      ? () {
                          backend.triggerControlEvent(cell, "double_tap");
                        }
                      : null,
                  onLongPress: cell.getBool("onLongPress", false)!
                      ? () {
                          backend.triggerControlEvent(cell, "long_press");
                        }
                      : null,
                  onTap: cell.getBool("onTap", false)!
                      ? () {
                          backend.triggerControlEvent(cell, "tap");
                        }
                      : null,
                  onTapCancel: cell.getBool("onTapCancel", false)!
                      ? () {
                          backend.triggerControlEvent(cell, "tap_cancel");
                        }
                      : null,
                  onTapDown: cell.getBool("onTapDown", false)!
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
              }).toList());
        }).toList());

    return ConstrainedControl(control: control, child: datatable);
  }
}
