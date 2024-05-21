import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class DataTableControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const DataTableControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<DataTableControl> createState() => _DataTableControlState();
}

class _DataTableControlState extends State<DataTableControl>
    with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint("DataTableControl build: ${widget.control.id}");

    bool tableDisabled = widget.control.isDisabled || widget.parentDisabled;

    var datatable =
        withControls(widget.children.where((c) => c.isVisible).map((c) => c.id),
            (content, viewModel) {
      var bgColor = widget.control.attrString("bgColor");
      var border = parseBorder(Theme.of(context), widget.control, "border");
      var borderRadius = parseBorderRadius(widget.control, "borderRadius");
      var gradient =
          parseGradient(Theme.of(context), widget.control, "gradient");
      var horizontalLines =
          parseBorderSide(Theme.of(context), widget.control, "horizontalLines");
      var verticalLines =
          parseBorderSide(Theme.of(context), widget.control, "verticalLines");
      var defaultDecoration =
          Theme.of(context).dataTableTheme.decoration ?? const BoxDecoration();

      BoxDecoration? decoration;
      if (bgColor != null ||
          border != null ||
          borderRadius != null ||
          gradient != null) {
        decoration = (defaultDecoration as BoxDecoration).copyWith(
            color: HexColor.fromString(Theme.of(context), bgColor ?? ""),
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

      Clip clipBehavior = Clip.values.firstWhere(
          (c) => c.toString() == widget.control.attrString("clipBehavior", "")!,
          orElse: () => Clip.none);

      return DataTable(
          decoration: decoration,
          border: tableBorder,
          clipBehavior: clipBehavior,
          checkboxHorizontalMargin:
              widget.control.attrDouble("checkboxHorizontalMargin"),
          columnSpacing: widget.control.attrDouble("columnSpacing"),
          dataRowColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "dataRowColor"),
          dataRowMinHeight: widget.control.attrDouble("dataRowMinHeight"),
          dataRowMaxHeight: widget.control.attrDouble("dataRowMaxHeight"),
          dataTextStyle: parseTextStyle(
              Theme.of(context), widget.control, "dataTextStyle"),
          headingRowColor: parseMaterialStateColor(
              Theme.of(context), widget.control, "headingRowColor"),
          headingRowHeight: widget.control.attrDouble("headingRowHeight"),
          headingTextStyle: parseTextStyle(
              Theme.of(context), widget.control, "headingTextStyle"),
          dividerThickness: widget.control.attrDouble("dividerThickness"),
          horizontalMargin: widget.control.attrDouble("horizontalMargin"),
          showBottomBorder: widget.control.attrBool("showBottomBorder", false)!,
          showCheckboxColumn:
              widget.control.attrBool("showCheckboxColumn", false)!,
          sortAscending: widget.control.attrBool("sortAscending", false)!,
          sortColumnIndex: widget.control.attrInt("sortColumnIndex"),
          onSelectAll: widget.control.attrBool("onSelectAll", false)!
              ? (selected) {
                  widget.backend.triggerControlEvent(
                      widget.control.id,
                      "select_all",
                      selected != null ? selected.toString() : "");
                }
              : null,
          columns: viewModel.controlViews
              .where((c) => c.control.type == "c")
              .map((column) {
            var labelCtrls = column.children.where((c) => c.name == "l");
            return DataColumn(
                numeric: column.control.attrBool("numeric", false)!,
                tooltip: column.control.attrString("tooltip"),
                onSort: column.control.attrBool("onSort", false)!
                    ? (columnIndex, ascending) {
                        widget.backend.triggerControlEvent(
                            column.control.id,
                            "sort",
                            json.encode({"i": columnIndex, "a": ascending}));
                      }
                    : null,
                label: createControl(column.control, labelCtrls.first.id,
                    column.control.isDisabled || tableDisabled));
          }).toList(),
          rows: viewModel.controlViews
              .where((c) => c.control.type == "r")
              .map((row) {
            return DataRow(
                key: ValueKey(row.control.id),
                selected: row.control.attrBool("selected", false)!,
                color: parseMaterialStateColor(
                    Theme.of(context), row.control, "color"),
                onSelectChanged: row.control.attrBool("onSelectChanged", false)!
                    ? (selected) {
                        widget.backend.triggerControlEvent(
                            row.control.id,
                            "select_changed",
                            selected != null ? selected.toString() : "");
                      }
                    : null,
                onLongPress: row.control.attrBool("onLongPress", false)!
                    ? () {
                        widget.backend.triggerControlEvent(row.control.id, "long_press");
                      }
                    : null,
                cells: row.children
                    .map((cell) => DataCell(
                          createControl(row.control, cell.childIds.first,
                              row.control.isDisabled || tableDisabled),
                          placeholder: cell.attrBool("placeholder", false)!,
                          showEditIcon: cell.attrBool("showEditIcon", false)!,
                          onDoubleTap: cell.attrBool("onDoubleTap", false)!
                              ? () {
                                  widget.backend.triggerControlEvent(
                                      cell.id, "double_tap");
                                }
                              : null,
                          onLongPress: cell.attrBool("onLongPress", false)!
                              ? () {
                                  widget.backend.triggerControlEvent(
                                      cell.id, "long_press");
                                }
                              : null,
                          onTap: cell.attrBool("onTap", false)!
                              ? () {
                                  widget.backend
                                      .triggerControlEvent(cell.id, "tap");
                                }
                              : null,
                          onTapCancel: cell.attrBool("onTapCancel", false)!
                              ? () {
                                  widget.backend.triggerControlEvent(
                                      cell.id, "tap_cancel");
                                }
                              : null,
                          onTapDown: cell.attrBool("onTapDown", false)!
                              ? (details) {
                                  widget.backend.triggerControlEvent(
                                      cell.id,
                                      "tap_down",
                                      json.encode({
                                        "kind": details.kind?.name,
                                        "lx": details.localPosition.dx,
                                        "ly": details.localPosition.dy,
                                        "gx": details.globalPosition.dx,
                                        "gy": details.globalPosition.dy,
                                      }));
                                }
                              : null,
                        ))
                    .toList());
          }).toList());
    });

    return constrainedControl(
        context, datatable, widget.parent, widget.control);
  }
}
