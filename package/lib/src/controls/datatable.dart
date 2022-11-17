import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:flet/src/controls/error.dart';
import 'package:flet/src/models/control_view_model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';

class DataTableControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const DataTableControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<DataTableControl> createState() => _DataTableControlState();
}

class _DataTableControlState extends State<DataTableControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("DataTableControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var ws = FletAppServices.of(context).ws;

    var datatable = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store, widget.children.where((c) => c.isVisible).map((c) => c.id)),
        builder: (content, viewModel) {
          return DataTable(
              columns: viewModel.controlViews
                  .where((c) => c.control.type == "c")
                  .map((column) {
                var labelCtrls = column.children.where((c) => c.name == "l");
                return DataColumn(
                    numeric: column.control.attrBool("numeric", false)!,
                    tooltip: column.control.attrString("tooltip"),
                    onSort: column.control.attrBool("onSort", false)!
                        ? (columnIndex, ascending) {
                            ws.pageEventFromWeb(
                                eventTarget: column.control.id,
                                eventName: "sort",
                                eventData: json.encode(
                                    {"i": columnIndex, "a": ascending}));
                          }
                        : null,
                    label: createControl(
                        column.control, labelCtrls.first.id, disabled));
              }).toList(),
              rows: viewModel.controlViews
                  .where((c) => c.control.type == "r")
                  .map((row) {
                return DataRow(
                    key: ValueKey(row.control.id),
                    selected: row.control.attrBool("selected", false)!,
                    color: parseMaterialStateColor(
                        Theme.of(context), row.control, "color"),
                    onSelectChanged:
                        row.control.attrBool("onSelectChanged", false)!
                            ? (selected) {
                                ws.pageEventFromWeb(
                                    eventTarget: row.control.id,
                                    eventName: "select_changed",
                                    eventData: selected != null
                                        ? selected.toString()
                                        : "");
                              }
                            : null,
                    onLongPress: row.control.attrBool("onLongPress", false)!
                        ? () {
                            ws.pageEventFromWeb(
                                eventTarget: row.control.id,
                                eventName: "long_press",
                                eventData: "");
                          }
                        : null,
                    cells: row.children
                        .map((cell) => DataCell(createControl(
                            row.control, cell.childIds.first, disabled)))
                        .toList());
              }).toList());
        });

    return constrainedControl(
        context, datatable, widget.parent, widget.control);
  }
}
