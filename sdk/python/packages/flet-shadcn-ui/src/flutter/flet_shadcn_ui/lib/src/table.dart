import 'dart:math';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/intrinsics.dart';
import 'utils/theme.dart';

class ShadTableControl extends StatelessWidget {
  final Control control;

  const ShadTableControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadTable build: ${control.id}");

    final columns = control.children("columns");
    if (columns.isEmpty) return const SizedBox.shrink();
    final rows = control.children("rows");
    final footer = control.children("footer");
    final hasHeader = columns.any((c) => c.get("header") != null);
    final hasFooter = footer.isNotEmpty;
    final rowHeight = control.getDouble("row_height", 48)!;

    Alignment? columnAlignment(int column) =>
        columns[column].getAlignment("alignment");

    ShadTableCell cell(
      Control cellControl,
      int column,
      ShadTableCellVariant variant,
    ) => ShadTableCell.raw(
      variant: variant,
      alignment:
          cellControl.getAlignment("alignment") ?? columnAlignment(column),
      child:
          cellControl.buildTextOrWidget("content") ?? const SizedBox.shrink(),
    );

    double widthOf(Control column) => column.getDouble("width", 100)!;
    bool fills(Control column) => column.getBool("fill", false)!;
    final fillCount = columns.where(fills).length;
    final fixedWidth = columns
        .where((c) => !fills(c))
        .fold<double>(0, (sum, c) => sum + widthOf(c));

    final table = ShadTable(
      columnCount: columns.length,
      rowCount: rows.length,
      builder: (context, vicinity) => cell(
        rows[vicinity.row].children("cells")[vicinity.column],
        vicinity.column,
        ShadTableCellVariant.cell,
      ),
      header: hasHeader
          ? (context, column) => ShadTableCell.header(
              alignment: columnAlignment(column),
              child:
                  columns[column].buildTextOrWidget("header") ??
                  const SizedBox.shrink(),
            )
          : null,
      footer: hasFooter
          ? (context, column) =>
                cell(footer[column], column, ShadTableCellVariant.footer)
          : null,
      columnSpanExtent: (column) => fills(columns[column])
          ? _FillTableSpanExtent(
              fixedWidth: fixedWidth,
              fillCount: fillCount,
              minWidth: widthOf(columns[column]),
            )
          : FixedTableSpanExtent(widthOf(columns[column])),
      rowSpanExtent: (row) => FixedTableSpanExtent(rowHeight),
      pinnedRowCount: control.getInt("pinned_row_count", 0),
      onRowTap: control.hasEventHandler("row_click")
          ? (row) {
              // ShadTable counts the header and footer rows; report the index
              // into `rows` and ignore clicks on the header and footer.
              final index = hasHeader ? row - 1 : row;
              if (index >= 0 && index < rows.length) {
                control.triggerEvent("row_click", index);
              }
            }
          : null,
    );

    // ShadTable is a scroll viewport: it has no natural size and throws when
    // asked for one. It is given its content size here, which applies only
    // where the parent leaves a direction unbounded (e.g. height in a
    // Column); smaller bounded sizes make it scroll.
    final naturalWidth = columns.fold<double>(0, (sum, c) => sum + widthOf(c));
    final naturalHeight =
        rowHeight * (rows.length + (hasHeader ? 1 : 0) + (hasFooter ? 1 : 0));

    Widget sized = LimitedBox(
      maxWidth: naturalWidth,
      maxHeight: naturalHeight,
      child: table,
    );
    if (fillCount == 0) {
      // Without a filling column, extra width would only be empty space.
      sized = ConstrainedBox(
        constraints: BoxConstraints(maxWidth: naturalWidth),
        child: sized,
      );
    }

    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        FixedIntrinsics(
          minWidth: naturalWidth,
          maxWidth: naturalWidth,
          height: naturalHeight,
          child: sized,
        ),
      ),
    );
  }
}

/// Width of a `fill` column: the viewport width left over by all fixed
/// columns, shared equally by the filling columns, but at least [minWidth].
///
/// shadcn_ui's RemainingTableSpanExtent only subtracts the columns before
/// it, so a filling column in the middle pushed later columns out of view.
class _FillTableSpanExtent extends TableSpanExtent {
  final double fixedWidth;
  final int fillCount;
  final double minWidth;

  const _FillTableSpanExtent({
    required this.fixedWidth,
    required this.fillCount,
    required this.minWidth,
  });

  @override
  double calculateExtent(TableSpanExtentDelegate delegate) =>
      max(minWidth, (delegate.viewportExtent - fixedWidth) / fillCount);
}
