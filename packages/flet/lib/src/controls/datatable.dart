import 'dart:math' as math;

import 'package:flutter/rendering.dart';
import 'package:flutter/scheduler.dart';
import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/events.dart';
import '../utils/gradient.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/tooltip.dart';
import 'base_controls.dart';
import 'text.dart';

/// A table with at least this many rows, all of one fixed height, builds only
/// the rows near the visible area. See [_LazyDataTable].
const int _lazyMinRows = 100;

/// Rows per chunk of a lazy table. Each chunk is its own small [DataTable].
const int _chunkRows = 10;

/// How many of each column's widest texts, and texts with the widest word,
/// measure its width up front.
const int _seedWidestTexts = 4;
const int _seedWidestWords = 2;

class DataTableControl extends StatelessWidget {
  final Control control;

  const DataTableControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("DataTableControl build: ${control.id}");

    var theme = Theme.of(context);
    var dataTableTheme = DataTableTheme.of(context);
    var bgcolor = control.getString("bgcolor");
    var border = control.getBorder("border", theme);
    var borderRadius = control.getBorderRadius("border_radius");
    var gradient = control.getGradient("gradient", theme);
    var horizontalLines = control.getBorderSide("horizontal_lines", theme);
    var verticalLines = control.getBorderSide("vertical_lines", theme);
    var defaultDecoration = theme.dataTableTheme.decoration as BoxDecoration? ??
        const BoxDecoration();

    BoxDecoration? decoration;

    if (bgcolor != null ||
        border != null ||
        borderRadius != null ||
        gradient != null) {
      decoration = defaultDecoration.copyWith(
          color: parseColor(bgcolor, theme),
          border: border,
          borderRadius: borderRadius,
          gradient: gradient);
    }

    var tableBorder = (horizontalLines != null || verticalLines != null)
        ? TableBorder(
            horizontalInside: horizontalLines ?? BorderSide.none,
            verticalInside: verticalLines ?? BorderSide.none)
        : null;
    var clipBehavior = control.getClipBehavior("clip_behavior", Clip.none)!;
    var dataRowMinHeight = control.getDouble("data_row_min_height");
    var dataRowMaxHeight = control.getDouble("data_row_max_height");
    var headingRowHeight = control.getDouble("heading_row_height");
    var headingRowColor =
        control.getWidgetStateColor("heading_row_color", theme);
    var showCheckboxColumn = control.getBool("show_checkbox_column", false)!;
    var sortAscending = control.getBool("sort_ascending", false)!;
    var sortColumnIndex = control.getInt("sort_column_index");

    var columnControls = control.children("columns");
    var rowControls = control.children("rows");

    DataTable buildTable({
      required List<DataColumn> columns,
      required List<DataRow> rows,
      required Decoration decoration,
      TableBorder? border,
      double? headingRowHeight,
      WidgetStateProperty<Color?>? headingRowColor,
      int? sortColumnIndex,
      ValueSetter<bool?>? onSelectAll,
      bool? showsHeading,
    }) {
      return _DataTable(
        showsHeading: showsHeading,
        decoration: decoration,
        border: border,
        clipBehavior: clipBehavior,
        checkboxHorizontalMargin:
            control.getDouble("checkbox_horizontal_margin"),
        columnSpacing: control.getDouble("column_spacing"),
        dataRowColor: control.getWidgetStateColor("data_row_color", theme),
        dataRowMinHeight: dataRowMinHeight,
        dataRowMaxHeight: dataRowMaxHeight,
        dataTextStyle: control.getTextStyle("data_text_style", theme),
        headingRowColor: headingRowColor,
        headingRowHeight: headingRowHeight,
        headingTextStyle: control.getTextStyle("heading_text_style", theme),
        dividerThickness: control.getDouble("divider_thickness"),
        horizontalMargin: control.getDouble("horizontal_margin"),
        showBottomBorder: control.getBool("show_bottom_border", false)!,
        showCheckboxColumn: showCheckboxColumn,
        sortAscending: sortAscending,
        sortColumnIndex: sortColumnIndex,
        onSelectAll: onSelectAll,
        columns: columns,
        rows: rows,
      );
    }

    DataColumn buildColumn(Control column,
        {TableColumnWidth? width, bool label = true}) {
      column.notifyParent = true;
      var tooltip = label
          ? parseTooltip(column.get("tooltip"), context, const Placeholder())
          : null;
      return DataColumn(
        numeric: column.getBool("numeric", false)!,
        columnWidth: width,
        tooltip: tooltip?.message,
        headingRowAlignment:
            column.getMainAxisAlignment("heading_row_alignment"),
        mouseCursor: WidgetStateMouseCursor.clickable,
        onSort: label && column.hasEventHandler("sort")
            ? (columnIndex, ascending) => column
                .triggerEvent("sort", {"ci": columnIndex, "asc": ascending})
            : null,
        label: label
            ? column.buildTextOrWidget("label", notifyParent: width != null)!
            : const SizedBox.shrink(),
      );
    }

    DataRow buildRow(Control row) {
      row.notifyParent = true;
      return DataRow(
        key: ValueKey(row.id),
        selected: row.getBool("selected", false)!,
        color: row.getWidgetStateColor("color", theme),
        onSelectChanged: row.hasEventHandler("select_change")
            ? (selected) => row.triggerEvent("select_change", selected)
            : null,
        onLongPress: row.hasEventHandler("long_press")
            ? () => row.triggerEvent("long_press")
            : null,
        cells: row.children("cells").map((cell) {
          cell.notifyParent = true;
          // A built cell's content rebuilds only itself when it changes; its
          // table measures it again as it lays out.
          return DataCell(
            cell.buildTextOrWidget("content")!,
            placeholder: cell.getBool("placeholder", false)!,
            showEditIcon: cell.getBool("show_edit_icon", false)!,
            onDoubleTap: cell.hasEventHandler("double_tap")
                ? () => cell.triggerEvent("double_tap")
                : null,
            onLongPress: cell.hasEventHandler("long_press")
                ? () => cell.triggerEvent("long_press")
                : null,
            onTap: cell.hasEventHandler("tap")
                ? () => cell.triggerEvent("tap")
                : null,
            onTapCancel: cell.hasEventHandler("tap_cancel")
                ? () => cell.triggerEvent("tap_cancel")
                : null,
            onTapDown: cell.hasEventHandler("tap_down")
                ? (TapDownDetails details) =>
                    cell.triggerEvent("tap_down", details.toMap())
                : null,
          );
        }).toList(),
      );
    }

    var rowHeight = dataRowMinHeight ??
        dataTableTheme.dataRowMinHeight ??
        theme.dataTableTheme.dataRowMinHeight ??
        kMinInteractiveDimension;
    var maxRowHeight = dataRowMaxHeight ??
        dataTableTheme.dataRowMaxHeight ??
        theme.dataTableTheme.dataRowMaxHeight ??
        kMinInteractiveDimension;
    var selectableRows = rowControls
        .where((row) => row.hasEventHandler("select_change"))
        .toList();
    var selectableCount = selectableRows.length;

    // Every chunk must draw the same columns and row states as one big table
    // would, so rows that mix selectable and not fall back to one table.
    if (!control.getBool("build_rows_on_demand", true)! ||
        rowControls.length < _lazyMinRows ||
        !rowHeight.isFinite ||
        rowHeight <= 0 ||
        rowHeight != maxRowHeight ||
        (selectableCount != 0 && selectableCount != rowControls.length)) {
      // DataTable paints every row on each paint, with no culling. Inside a
      // scrolling parent, every scroll frame would repaint the whole table;
      // the boundary keeps its recorded picture and only moves it.
      return LayoutControl(
          control: control,
          child: RepaintBoundary(
              child: buildTable(
            decoration: decoration ?? defaultDecoration,
            border: tableBorder,
            headingRowHeight: headingRowHeight,
            headingRowColor: headingRowColor,
            sortColumnIndex: sortColumnIndex,
            onSelectAll: control.hasEventHandler("select_all")
                ? (bool? selected) =>
                    control.triggerEvent("select_all", selected)
                : null,
            columns: columnControls.map(buildColumn).toList(),
            rows: rowControls.map(buildRow).toList(),
          )));
    }

    // Rows that aren't built still rebuild the table when they change, and
    // their widest texts measure the column widths.
    var glyphs = _GlyphWidths.of(
        DefaultTextStyle.of(context).style.merge(
            control.getTextStyle("data_text_style", theme) ??
                dataTableTheme.dataTextStyle ??
                theme.dataTableTheme.dataTextStyle ??
                theme.textTheme.bodyMedium),
        MediaQuery.textScalerOf(context));
    var widest = [
      for (var _ in columnControls) _Widest<Control>(_seedWidestTexts)
    ];
    var widestWords = [
      for (var _ in columnControls) _Widest<Control>(_seedWidestWords)
    ];
    for (var row in rowControls) {
      row.notifyParent = true;
      var cells = row.children("cells");
      for (var c = 0; c < cells.length; c++) {
        var cell = cells[c]..notifyParent = true;
        // The content of a row that isn't built has no widget to rebuild, so
        // its changes rebuild the table instead. Built rows turn this off.
        var content = cell.child("content", visibleOnly: false);
        if (content != null) _notifyTable(content);
        var text = _cellText(cell);
        if (text == null || c >= widest.length) continue;
        var (width, word) = glyphs.estimate(text);
        widest[c].add(width, cell);
        widestWords[c].add(word, cell);
      }
    }
    // What changes every column's width at once: the columns, the text style
    // and the spacing. A change starts the measurements over.
    var widthsKey = Object.hash(
        Object.hashAll(columnControls.map((column) => column.id)),
        glyphs.style,
        glyphs.textScaler,
        dataTableTheme,
        theme.dataTableTheme,
        control.getTextStyle("heading_text_style", theme),
        control.getDouble("checkbox_horizontal_margin"),
        control.getDouble("column_spacing"),
        control.getDouble("horizontal_margin"),
        showCheckboxColumn);
    // Each column's candidates, a few rows deep: the table that measures them
    // only needs each column's cells, not whole rows.
    var seedCells = [
      for (var c = 0; c < columnControls.length; c++)
        {...widest[c].items, ...widestWords[c].items}.toList()
    ];
    var seedDepth = seedCells.fold(0, (n, cells) => math.max(n, cells.length));

    var selectedCount =
        selectableRows.where((row) => row.getBool("selected", false)!).length;
    List<DataColumn> hiddenColumns(List<TableColumnWidth> widths) => [
          for (var i = 0; i < columnControls.length; i++)
            buildColumn(columnControls[i], width: widths[i], label: false)
        ];

    return LayoutControl(
      control: control,
      child: Container(
        decoration: decoration ?? defaultDecoration,
        child: Material(
          type: MaterialType.transparency,
          borderRadius: tableBorder?.borderRadius,
          clipBehavior: clipBehavior,
          child: _LazyDataTable(
            rowCount: rowControls.length,
            columnCount: columnControls.length,
            flexColumn: _onlyTextColumn(columnControls),
            chunkKey: (start, end) {
              var key = 0;
              for (var r = start; r < math.min(end, rowControls.length); r++) {
                var row = rowControls[r];
                key = Object.hash(key, row.id);
                for (var cell in row.children("cells")) {
                  // A change anywhere in a cell of a row that isn't built
                  // reaches the cell and its content: see _notifyTable.
                  var content = cell.child("content", visibleOnly: false);
                  key = Object.hash(key, cell.id, cell.changeCount, content?.id,
                      content?.changeCount);
                }
              }
              return key;
            },
            widthsKey: widthsKey,
            rowHeight: rowHeight,
            headingRowHeight: headingRowHeight ??
                dataTableTheme.headingRowHeight ??
                theme.dataTableTheme.headingRowHeight ??
                56.0,
            lineWidth: horizontalLines?.width ?? 0,
            buildHeader: (widths) => buildTable(
              showsHeading: true,
              decoration: const BoxDecoration(),
              border: verticalLines != null
                  ? TableBorder(verticalInside: verticalLines)
                  : null,
              headingRowHeight: headingRowHeight,
              headingRowColor: headingRowColor,
              sortColumnIndex: sortColumnIndex,
              onSelectAll: (bool? selected) {
                if (control.hasEventHandler("select_all")) {
                  control.triggerEvent("select_all", selected);
                  return;
                }
                for (var row in selectableRows) {
                  if (row.getBool("selected", false)! != selected) {
                    row.triggerEvent("select_change", selected);
                  }
                }
              },
              columns: [
                for (var i = 0; i < columnControls.length; i++)
                  buildColumn(columnControls[i], width: widths[i])
              ],
              // The header's checkbox shows whether none, some or all rows
              // are selected; these two hidden rows stand in for all of them.
              rows: [
                if (showCheckboxColumn && selectableCount > 0)
                  for (var selected in [
                    selectedCount > 0,
                    selectedCount == selectableCount
                  ])
                    DataRow(
                      selected: selected,
                      onSelectChanged: (_) {},
                      cells: [
                        for (var _ in columnControls)
                          const DataCell(SizedBox.shrink())
                      ],
                    ),
              ],
            ),
            buildChunk: (start, end, widths) => buildTable(
              showsHeading: false,
              decoration: const BoxDecoration(),
              border: tableBorder,
              headingRowHeight: kMinInteractiveDimension,
              headingRowColor: const WidgetStatePropertyAll(Colors.transparent),
              // The hidden heading's checkbox would select only this chunk.
              onSelectAll: (_) {},
              columns: hiddenColumns(widths),
              rows: [
                for (var r = start; r < end; r++) buildRow(rowControls[r])
              ],
            ),
            releaseRows: (start, end) {
              for (var r = start; r < math.min(end, rowControls.length); r++) {
                for (var cell in rowControls[r].children("cells")) {
                  var content = cell.child("content", visibleOnly: false);
                  if (content != null) _notifyTable(content);
                }
              }
            },
            buildSeed: (widths) => buildTable(
              decoration: const BoxDecoration(),
              columns: hiddenColumns(widths),
              rows: [
                for (var r = 0; r < seedDepth; r++)
                  DataRow(
                    onSelectChanged: selectableCount > 0 ? (_) {} : null,
                    cells: [
                      for (var cells in seedCells)
                        r < cells.length
                            ? DataCell(
                                _seedContent(cells[r]),
                                placeholder:
                                    cells[r].getBool("placeholder", false)!,
                                showEditIcon:
                                    cells[r].getBool("show_edit_icon", false)!,
                              )
                            : const DataCell(SizedBox.shrink())
                    ],
                  )
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Makes [control], and every control inside it, notify its parent of a
/// change instead of its own widget, which it doesn't have while its row isn't
/// built. A change anywhere in a cell's content then counts as a change of
/// the content and the cell, and rebuilds the table. Building the row turns
/// this off again, as each control builds its children.
void _notifyTable(Control control) {
  control.notifyParent = true;
  for (var value in control.properties.values) {
    _notifyTableIn(value);
  }
}

void _notifyTableIn(Object? value) {
  if (value is Control) {
    _notifyTable(value);
  } else if (value is List) {
    for (var item in value) {
      _notifyTableIn(item);
    }
  } else if (value is Map) {
    for (var item in value.values) {
      _notifyTableIn(item);
    }
  }
}

/// The text a cell shows, if its content is a plain string or a `Text`.
String? _cellText(Control cell) {
  var content = cell.get("content");
  if (content is String) return content;
  if (content is Control && content.type == "Text" && content.visible) {
    return content.getString("value");
  }
  return null;
}

/// A copy of a cell's text for measuring. Other content is left out: a second
/// live copy of an arbitrary control could register itself twice.
Widget _seedContent(Control cell) {
  var content = cell.get("content");
  if (content is String) return Text(content);
  if (content is Control && content.type == "Text" && content.visible) {
    // The Text of a built row changes without rebuilding the table, so the
    // copy follows the control itself.
    return ListenableBuilder(
        listenable: content,
        builder: (context, _) => TextControl(control: content));
  }
  return const SizedBox.shrink();
}

/// A [DataTable] of which a lazy table shows only part: just the heading row
/// of the header ([showsHeading] true), or just the data rows of a chunk
/// (false). The rows that don't show still hold checkboxes and ink wells, so
/// they are kept out of keyboard focus. With [showsHeading] null, every row
/// shows, as in a plain [DataTable].
class _DataTable extends DataTable {
  _DataTable({
    required this.showsHeading,
    super.decoration,
    super.border,
    super.clipBehavior,
    super.checkboxHorizontalMargin,
    super.columnSpacing,
    super.dataRowColor,
    super.dataRowMinHeight,
    super.dataRowMaxHeight,
    super.dataTextStyle,
    super.headingRowColor,
    super.headingRowHeight,
    super.headingTextStyle,
    super.dividerThickness,
    super.horizontalMargin,
    super.showBottomBorder,
    super.showCheckboxColumn,
    super.sortAscending,
    super.sortColumnIndex,
    super.onSelectAll,
    required super.columns,
    required super.rows,
  });

  final bool? showsHeading;

  @override
  Widget build(BuildContext context) {
    var built = super.build(context);
    var showsHeading = this.showsHeading;
    if (showsHeading == null) return built;
    var table = _tableIn(built);
    assert(table != null, "DataTable no longer builds its Table as expected");
    if (table == null) return built;
    for (var r = 0; r < table.children.length; r++) {
      if ((r == 0) == showsHeading) continue;
      var cells = table.children[r].children;
      for (var c = 0; c < cells.length; c++) {
        // ExcludeFocus adds no render object, so each cell stays a direct
        // child of the Table.
        cells[c] = ExcludeFocus(child: cells[c]);
      }
    }
    return built;
  }

  /// The [Table] that [DataTable.build] returns, inside its decoration.
  static Table? _tableIn(Widget widget) => switch (widget) {
        Table() => widget,
        Container(:var child?) => _tableIn(child),
        Material(:var child?) => _tableIn(child),
        _ => null,
      };
}

/// Estimates how wide a text lays out by adding up the advance of each
/// character, measured once per style. Far cheaper than laying the text out,
/// and close enough to pick the widest texts of a column.
class _GlyphWidths {
  _GlyphWidths._(this.style, this.textScaler);

  static final _cache = <(TextStyle, TextScaler), _GlyphWidths>{};

  static _GlyphWidths of(TextStyle style, TextScaler textScaler) {
    if (_cache.length > 16) _cache.clear();
    return _cache[(style, textScaler)] ??= _GlyphWidths._(style, textScaler);
  }

  final TextStyle style;
  final TextScaler textScaler;
  final _advances = <int, double>{};

  double _advance(int codeUnit) => _advances[codeUnit] ??= () {
        var painter = TextPainter(
            text: TextSpan(text: String.fromCharCode(codeUnit), style: style),
            textDirection: TextDirection.ltr,
            textScaler: textScaler)
          ..layout();
        var width = painter.width;
        painter.dispose();
        return width;
      }();

  /// The text's width on one line, and the width of its widest word: what the
  /// column needs at most, and at least.
  (double, double) estimate(String text) {
    var width = 0.0, word = 0.0, widestWord = 0.0;
    for (var codeUnit in text.codeUnits) {
      var advance = _advance(codeUnit);
      width += advance;
      if (codeUnit == 0x20) {
        widestWord = math.max(widestWord, word);
        word = 0;
      } else {
        word += advance;
      }
    }
    return (width, math.max(widestWord, word));
  }
}

/// The [count] items added with the largest values.
class _Widest<T> {
  _Widest(this.count);

  final int count;
  final _entries = <(double, T)>[];

  Iterable<T> get items => _entries.map((e) => e.$2);

  void add(double value, T item) {
    if (_entries.length == count) {
      if (value <= _entries.last.$1) return;
      _entries.removeLast();
    }
    var i = _entries.indexWhere((e) => e.$1 < value);
    _entries.insert(i < 0 ? _entries.length : i, (value, item));
  }
}

/// The column [DataTable] lets grow into spare width: the only non-numeric
/// one, if there is exactly one.
int? _onlyTextColumn(List<Control> columns) {
  int? result;
  for (var i = 0; i < columns.length; i++) {
    if (!columns[i].getBool("numeric", false)!) {
      if (result != null) return null;
      result = i;
    }
  }
  return result;
}

/// A [DataTable] that builds only the rows near the visible area.
///
/// A Flutter [DataTable] builds, measures and lays out every cell, so a table
/// of a few thousand rows freezes the app while it loads. Here the rows are
/// split into chunks of [_chunkRows], each its own [DataTable] with its
/// heading row hidden, stacked under a header [DataTable]. Only the chunks
/// near the nearest vertical [Scrollable]'s viewport are built, so the table
/// still scrolls with its parent, like a single [DataTable] does.
///
/// All of them share column widths through [_ColumnWidths]: a column is as
/// wide as the widest cell measured so far, starting with the header and the
/// widest texts of each column.
class _LazyDataTable extends StatefulWidget {
  const _LazyDataTable({
    required this.rowCount,
    required this.columnCount,
    required this.flexColumn,
    required this.chunkKey,
    required this.widthsKey,
    required this.rowHeight,
    required this.headingRowHeight,
    required this.lineWidth,
    required this.buildHeader,
    required this.buildChunk,
    required this.releaseRows,
    required this.buildSeed,
  });

  final int rowCount;
  final int columnCount;

  final int? flexColumn;

  /// What the rows from start to end show, as far as it changes their
  /// widths: their ids, and how often their cells and content changed.
  final int Function(int start, int end) chunkKey;

  /// What changes the width of every column at once.
  final Object widthsKey;
  final double rowHeight;
  final double headingRowHeight;

  /// Width of the line drawn between rows, which reaches above a chunk.
  final double lineWidth;
  final DataTable Function(List<TableColumnWidth> widths) buildHeader;
  final DataTable Function(int start, int end, List<TableColumnWidth> widths)
      buildChunk;

  /// Called for the rows of a chunk that is no longer built.
  final void Function(int start, int end) releaseRows;
  final DataTable Function(List<TableColumnWidth> widths) buildSeed;

  @override
  State<_LazyDataTable> createState() => _LazyDataTableState();
}

class _LazyDataTableState extends State<_LazyDataTable> {
  late _ColumnWidths _widths = _newWidths();
  final _tableKey = GlobalKey();
  final _chunks = <int, Widget>{};
  Widget? _seed;
  int _first = 0;
  int _last = -1;

  /// The chunks the last build built, from first to last.
  (int, int) _built = (0, -1);

  /// For each chunk measured and no longer built, its [_LazyDataTable.chunkKey]
  /// when it stopped being built. A built chunk measures again whenever its
  /// cells change size, so this is what its measurement saw.
  final _releasedKeys = <int, int>{};
  Size _viewSize = Size.zero;
  ScrollableState? _scrollable;

  /// The position [_check] listens to. A [Scrollable] can swap in a new one,
  /// so it's kept apart from [_scrollable].
  ScrollPosition? _position;
  bool _checkScheduled = false;

  int get _chunkCount => (widget.rowCount + _chunkRows - 1) ~/ _chunkRows;

  int _chunkStart(int chunk) => chunk * _chunkRows;
  int _chunkEnd(int chunk) =>
      math.min(widget.rowCount, (chunk + 1) * _chunkRows);

  int _chunkAt(double y) =>
      ((y - widget.headingRowHeight) / (_chunkRows * widget.rowHeight))
          .floor()
          .clamp(0, _chunkCount - 1);

  /// Whether a widget in the chunk [i] still has to rebuild. A cell that
  /// changes marks its widget to rebuild; every widget built is laid out in
  /// the same frame, so without one, the chunk's last measurement is current.
  bool _hasPendingBuild(int i) {
    var table = _tableKey.currentContext as Element?;
    if (table == null) return false;
    var pending = false;
    void visit(Element element) {
      if (pending) return;
      if (element.dirty) {
        pending = true;
        return;
      }
      element.visitChildren(visit);
    }

    table.visitChildren((slot) {
      var widget = slot.widget;
      if (widget is _TableSlot && widget.slot == i) visit(slot);
    });
    return pending;
  }

  _ColumnWidths _newWidths() =>
      _ColumnWidths(widget.columnCount, widget.flexColumn)
        ..addListener(_onWidthsChanged);

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _scrollable = Scrollable.maybeOf(context, axis: Axis.vertical);
    var position = _scrollable?.position;
    if (position != _position) {
      _position?.removeListener(_check);
      position?.addListener(_check);
      _position = position;
    }
  }

  @override
  void didUpdateWidget(_LazyDataTable oldWidget) {
    super.didUpdateWidget(oldWidget);
    _chunks.clear();
    _seed = null;
    if (widget.widthsKey != oldWidget.widthsKey ||
        widget.columnCount != oldWidget.columnCount ||
        widget.flexColumn != oldWidget.flexColumn) {
      _widths.dispose();
      _widths = _newWidths();
      _releasedKeys.clear();
    } else {
      // A chunk that isn't built keeps the widths it measured, unless its
      // rows changed since. The ones built measure again.
      _releasedKeys.removeWhere((i, key) =>
          i >= _chunkCount ||
          widget.chunkKey(_chunkStart(i), _chunkEnd(i)) != key);
      _widths.forget((slot) =>
          slot >= 0 &&
          (slot >= _chunkCount ||
              (!_releasedKeys.containsKey(slot) &&
                  (slot < _built.$1 || slot > _built.$2))));
      // Every shown table is built again, so laid out again.
      _widths.relayout();
    }
    if (_last >= _chunkCount) {
      _last = _chunkCount - 1;
      _first = math.min(_first, _last);
    }
  }

  @override
  void dispose() {
    _position?.removeListener(_check);
    _widths.dispose();
    super.dispose();
  }

  void _onWidthsChanged() {
    if (mounted) setState(_chunks.clear);
  }

  void _scheduleCheck() {
    if (_checkScheduled) return;
    _checkScheduled = true;
    SchedulerBinding.instance.addPostFrameCallback((_) {
      _checkScheduled = false;
      _check();
    });
  }

  /// Builds other chunks if the visible part of the table moved past the ones
  /// built, keeping about a viewport's worth above and below.
  void _check() {
    if (!mounted) return;
    var box = _tableKey.currentContext?.findRenderObject();
    if (box is! RenderBox || !box.attached || !box.hasSize) return;
    var screenToTable = box.getTransformTo(null);
    if (screenToTable.invert() == 0) return;
    var visible =
        MatrixUtils.transformRect(screenToTable, Offset.zero & _viewSize);
    var viewport = _scrollable?.context.findRenderObject();
    if (viewport is RenderBox && viewport.attached && viewport.hasSize) {
      var viewportToTable = box.getTransformTo(viewport);
      if (viewportToTable.invert() == 0) return;
      visible = visible.intersect(MatrixUtils.transformRect(
          viewportToTable, Offset.zero & viewport.size));
    }
    if (!visible.isFinite || visible.isEmpty) return;
    var top = visible.top, bottom = visible.bottom;
    var extent = bottom - top;
    if (_chunkAt(top - extent / 2) >= _first &&
        _chunkAt(bottom + extent / 2) <= _last) {
      return;
    }
    setState(() {
      _first = _chunkAt(top - extent);
      _last = _chunkAt(bottom + extent);
    });
  }

  @override
  Widget build(BuildContext context) {
    var view = View.of(context);
    _viewSize = view.physicalSize / view.devicePixelRatio;
    if (_last < 0) {
      _first = 0;
      _last = _chunkAt(2 * _viewSize.height);
    }
    for (var i = _built.$1; i <= _built.$2; i++) {
      if ((i < _first || i > _last) && i < _chunkCount) {
        widget.releaseRows(_chunkStart(i), _chunkEnd(i));
        if (_hasPendingBuild(i)) {
          // A cell changed since the chunk was last laid out, and its
          // widget goes before it is: what the chunk measured is out of date.
          _releasedKeys.remove(i);
          _widths.forget((slot) => slot == i);
        } else {
          _releasedKeys[i] = widget.chunkKey(_chunkStart(i), _chunkEnd(i));
        }
      }
    }
    for (var i = _first; i <= _last; i++) {
      _releasedKeys.remove(i);
    }
    _built = (_first, _last);
    _chunks.removeWhere((i, _) => i < _first || i > _last);
    _scheduleCheck();

    return _ChunkedTable(
      key: _tableKey,
      rowCount: widget.rowCount,
      rowHeight: widget.rowHeight,
      headingRowHeight: widget.headingRowHeight,
      lineWidth: widget.lineWidth,
      onPaint: _scheduleCheck,
      children: [
        _seed ??= _TableSlot(
            key: const ValueKey(_TableSlot.seed),
            slot: _TableSlot.seed,
            child: Offstage(
                child: ExcludeFocus(
                    child: widget.buildSeed(_widths.of(_TableSlot.seed))))),
        for (var i = _first; i <= _last; i++)
          _chunks[i] ??= _TableSlot(
              key: ValueKey(i),
              slot: i,
              child: RepaintBoundary(
                  child: widget.buildChunk(
                      i * _chunkRows,
                      math.min(widget.rowCount, (i + 1) * _chunkRows),
                      _widths.of(i)))),
        _TableSlot(
            key: const ValueKey(_TableSlot.header),
            slot: _TableSlot.header,
            child: RepaintBoundary(
                child: widget.buildHeader(_widths.of(_TableSlot.header)))),
      ],
    );
  }
}

/// Column widths shared by the tables of a [_LazyDataTable]: each column is as
/// wide as the widest of its cells that any table measured, the chunks that
/// are no longer built included.
class _ColumnWidths extends ChangeNotifier {
  _ColumnWidths(int count, this.flexColumn)
      : _min = [for (var i = 0; i < count; i++) _ColumnMeasure()],
        _max = [for (var i = 0; i < count; i++) _ColumnMeasure()];

  final int? flexColumn;
  final List<_ColumnMeasure> _min;
  final List<_ColumnMeasure> _max;
  bool _notifyScheduled = false;
  bool _disposed = false;

  /// The column widths of the table in [slot].
  List<TableColumnWidth> of(int slot) =>
      [for (var i = 0; i < _min.length; i++) _SharedColumnWidth(this, i, slot)];

  double _measure(_ColumnMeasure measure, int slot, Iterable<RenderBox> cells,
      double Function(RenderBox cell) width) {
    var measured = 0.0;
    for (var cell in cells) {
      measured = math.max(measured, width(cell));
    }
    // The seed table is never shown, so it can't be out of line.
    if (measure.update(slot, measured, shown: slot != _TableSlot.seed)) {
      _scheduleNotify();
    }
    return measure.width;
  }

  /// Drops what the tables in the slots [test] picks measured.
  void forget(bool Function(int slot) test) {
    for (var measure in [..._min, ..._max]) {
      measure.forget(test);
    }
  }

  /// Starts over tracking the widths given to shown tables, as all of them
  /// are about to be laid out again.
  void relayout() {
    for (var measure in [..._min, ..._max]) {
      measure.relayout();
    }
  }

  /// A table was laid out with a width that no longer fits the column: lay
  /// them all out again once this frame is done.
  void _scheduleNotify() {
    if (_notifyScheduled) return;
    _notifyScheduled = true;
    SchedulerBinding.instance.addPostFrameCallback((_) {
      _notifyScheduled = false;
      if (_disposed) return;
      relayout();
      notifyListeners();
    });
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}

/// One intrinsic width of one column: the largest that the tables measured,
/// each table's last measurement counting.
class _ColumnMeasure {
  final _bySlot = <int, double>{};
  double width = 0;

  /// The narrowest and widest [width] given to a shown table since all of
  /// them were last laid out again.
  double _givenLo = double.infinity;
  double _givenHi = double.negativeInfinity;

  /// Records what the table in [slot] measured. Returns whether a shown
  /// table was given a width other than [width].
  bool update(int slot, double measured, {required bool shown}) {
    var old = _bySlot[slot];
    _bySlot[slot] = measured;
    if (measured >= width) {
      width = measured;
    } else if (old != null && old >= width) {
      _recompute();
    }
    var stale = _givenLo < width || _givenHi > width;
    if (shown) {
      _givenLo = math.min(_givenLo, width);
      _givenHi = math.max(_givenHi, width);
    }
    return stale;
  }

  void forget(bool Function(int slot) test) {
    var before = _bySlot.length;
    _bySlot.removeWhere((slot, _) => test(slot));
    if (_bySlot.length != before) _recompute();
  }

  void relayout() {
    _givenLo = double.infinity;
    _givenHi = double.negativeInfinity;
  }

  void _recompute() =>
      width = _bySlot.values.fold(0.0, (a, b) => math.max(a, b));
}

class _SharedColumnWidth extends TableColumnWidth {
  const _SharedColumnWidth(this.widths, this.index, this.slot);

  final _ColumnWidths widths;
  final int index;

  /// The [_TableSlot] of the table this width is for.
  final int slot;

  @override
  double minIntrinsicWidth(Iterable<RenderBox> cells, double containerWidth) =>
      widths._measure(widths._min[index], slot, cells,
          (cell) => cell.getMinIntrinsicWidth(double.infinity));

  @override
  double maxIntrinsicWidth(Iterable<RenderBox> cells, double containerWidth) =>
      widths._measure(widths._max[index], slot, cells,
          (cell) => cell.getMaxIntrinsicWidth(double.infinity));

  @override
  double? flex(Iterable<RenderBox> cells) =>
      index == widths.flexColumn ? 1.0 : null;
}

/// Places a child of [_ChunkedTable]: the header, a chunk of rows by index,
/// or the hidden table that measures column widths.
class _TableSlot extends ParentDataWidget<_ChunkedTableParentData> {
  const _TableSlot({super.key, required this.slot, required super.child});

  static const int header = -1;
  static const int seed = -2;

  final int slot;

  @override
  void applyParentData(RenderObject renderObject) {
    var data = renderObject.parentData! as _ChunkedTableParentData;
    if (data.slot != slot) {
      data.slot = slot;
      renderObject.parent?.markNeedsLayout();
    }
  }

  @override
  Type get debugTypicalAncestorWidgetClass => _ChunkedTable;
}

class _ChunkedTableParentData extends ContainerBoxParentData<RenderBox> {
  int slot = _TableSlot.header;

  /// The part of the child that shows, in the child's coordinates.
  Rect visible = Rect.zero;
  double? bodyTop;
  final clipLayer = LayerHandle<ClipRectLayer>();
}

class _ChunkedTable extends MultiChildRenderObjectWidget {
  const _ChunkedTable({
    super.key,
    required this.rowCount,
    required this.rowHeight,
    required this.headingRowHeight,
    required this.lineWidth,
    required this.onPaint,
    super.children,
  });

  final int rowCount;
  final double rowHeight;
  final double headingRowHeight;
  final double lineWidth;
  final VoidCallback onPaint;

  @override
  _RenderChunkedTable createRenderObject(BuildContext context) =>
      _RenderChunkedTable(
          rowCount: rowCount,
          rowHeight: rowHeight,
          headingRowHeight: headingRowHeight,
          lineWidth: lineWidth,
          onPaint: onPaint);

  @override
  void updateRenderObject(
      BuildContext context, _RenderChunkedTable renderObject) {
    renderObject
      ..rowCount = rowCount
      ..rowHeight = rowHeight
      ..headingRowHeight = headingRowHeight
      ..lineWidth = lineWidth
      ..onPaint = onPaint;
  }
}

/// Lays out a [_LazyDataTable]: the header at the top, showing only its
/// heading row, and each chunk at its rows' place, showing only its rows.
///
/// Every child gets the same width constraints as one big table would, so
/// with the same column widths they come out the same width.
class _RenderChunkedTable extends RenderBox
    with
        ContainerRenderObjectMixin<RenderBox, _ChunkedTableParentData>,
        RenderBoxContainerDefaultsMixin<RenderBox, _ChunkedTableParentData> {
  _RenderChunkedTable({
    required int rowCount,
    required double rowHeight,
    required double headingRowHeight,
    required double lineWidth,
    required this.onPaint,
  })  : _rowCount = rowCount,
        _rowHeight = rowHeight,
        _headingRowHeight = headingRowHeight,
        _lineWidth = lineWidth;

  /// Called on every paint, which is when the table may have moved.
  VoidCallback onPaint;

  int get rowCount => _rowCount;
  int _rowCount;
  set rowCount(int value) {
    if (value == _rowCount) return;
    _rowCount = value;
    markNeedsLayout();
  }

  double get rowHeight => _rowHeight;
  double _rowHeight;
  set rowHeight(double value) {
    if (value == _rowHeight) return;
    _rowHeight = value;
    markNeedsLayout();
  }

  double get headingRowHeight => _headingRowHeight;
  double _headingRowHeight;
  set headingRowHeight(double value) {
    if (value == _headingRowHeight) return;
    _headingRowHeight = value;
    markNeedsLayout();
  }

  double get lineWidth => _lineWidth;
  double _lineWidth;
  set lineWidth(double value) {
    if (value == _lineWidth) return;
    _lineWidth = value;
    markNeedsLayout();
  }

  double get _height => headingRowHeight + rowCount * rowHeight;

  /// How far the clips reach past the table's sides. Only the tops and
  /// bottoms of the children need clipping; a hard clip at a side would cut
  /// the anti-aliased ends of the lines between rows.
  static const double _sideOverdraw = 2;

  RenderBox? get _header {
    for (var child = firstChild; child != null; child = childAfter(child)) {
      if ((child.parentData! as _ChunkedTableParentData).slot ==
          _TableSlot.header) {
        return child;
      }
    }
    return null;
  }

  /// The children that show, in paint order. The header goes first: the line
  /// under it is drawn by the first chunk, on top, as in one [DataTable].
  List<RenderBox> get _shown => [
        if (_header case var header?) header,
        for (var child = firstChild; child != null; child = childAfter(child))
          if ((child.parentData! as _ChunkedTableParentData).slot >= 0) child
      ];

  BoxConstraints _childConstraints(BoxConstraints constraints) =>
      BoxConstraints(
          minWidth: constraints.minWidth, maxWidth: constraints.maxWidth);

  @override
  void setupParentData(RenderBox child) {
    if (child.parentData is! _ChunkedTableParentData) {
      child.parentData = _ChunkedTableParentData();
    }
  }

  @override
  double computeMinIntrinsicWidth(double height) =>
      _header?.getMinIntrinsicWidth(double.infinity) ?? 0;

  @override
  double computeMaxIntrinsicWidth(double height) =>
      _header?.getMaxIntrinsicWidth(double.infinity) ?? 0;

  @override
  double computeMinIntrinsicHeight(double width) => _height;

  @override
  double computeMaxIntrinsicHeight(double width) => _height;

  @override
  Size computeDryLayout(covariant BoxConstraints constraints) {
    var width =
        _header?.getDryLayout(_childConstraints(constraints)).width ?? 0;
    return constraints.constrain(Size(width, _height));
  }

  @override
  void performLayout() {
    var childConstraints = _childConstraints(constraints);
    var width = 0.0;
    for (var child = firstChild; child != null; child = childAfter(child)) {
      var data = child.parentData! as _ChunkedTableParentData;
      if (data.slot == _TableSlot.seed) {
        child.layout(childConstraints);
        continue;
      }
      child.layout(childConstraints, parentUsesSize: true);
      var size = child.size;
      if (data.slot == _TableSlot.header) {
        data.offset = Offset.zero;
        data.bodyTop = null;
        data.visible = Rect.fromLTRB(
            -_sideOverdraw, 0, size.width + _sideOverdraw, headingRowHeight);
        width = size.width;
      } else {
        // The chunk's own heading row sits above its rows, out of sight,
        // except for the line between it and the first row: that is the line
        // above this chunk's rows. The clip takes the line's full width, as a
        // hard clip through a half-pixel would cut the line's edge off.
        var rows = math.min(_chunkRows, rowCount - data.slot * _chunkRows);
        var hidden = size.height - rows * rowHeight;
        data.bodyTop = hidden;
        data.offset = Offset(
            0, headingRowHeight + data.slot * _chunkRows * rowHeight - hidden);
        // Below, a cell that overflows its row still shows over the next
        // row, as it does in one table.
        data.visible = Rect.fromLTRB(-_sideOverdraw, hidden - lineWidth,
            size.width + _sideOverdraw, size.height + rowHeight);
      }
    }
    size = constraints.constrain(Size(width, _height));
  }

  @override
  void paint(PaintingContext context, Offset offset) {
    onPaint();
    for (var child in _shown) {
      var data = child.parentData! as _ChunkedTableParentData;
      data.clipLayer.layer = context.pushClipRect(
          needsCompositing,
          offset + data.offset,
          data.visible,
          (context, offset) => context.paintChild(child, offset),
          oldLayer: data.clipLayer.layer);
    }
  }

  /// The part of the child that takes taps and shows to accessibility, in
  /// the child's coordinates: what shows, less the line above a chunk's rows,
  /// which is drawn over the row above.
  static Rect _body(_ChunkedTableParentData data) {
    var bodyTop = data.bodyTop;
    if (bodyTop == null) return data.visible;
    return Rect.fromLTRB(
        data.visible.left, bodyTop, data.visible.right, data.visible.bottom);
  }

  @override
  bool hitTestChildren(BoxHitTestResult result, {required Offset position}) {
    for (var child in _shown.reversed) {
      var data = child.parentData! as _ChunkedTableParentData;
      if (!_body(data).shift(data.offset).contains(position)) continue;
      if (result.addWithPaintOffset(
          offset: data.offset,
          position: position,
          hitTest: (result, transformed) =>
              child.hitTest(result, position: transformed))) {
        return true;
      }
    }
    return false;
  }

  @override
  Rect describeApproximatePaintClip(RenderBox child) {
    var data = child.parentData! as _ChunkedTableParentData;
    return data.visible.shift(data.offset);
  }

  @override
  Rect? describeSemanticsClip(RenderBox child) {
    var data = child.parentData! as _ChunkedTableParentData;
    return _body(data).shift(data.offset);
  }

  @override
  void visitChildrenForSemantics(RenderObjectVisitor visitor) {
    for (var child = firstChild; child != null; child = childAfter(child)) {
      if ((child.parentData! as _ChunkedTableParentData).slot !=
          _TableSlot.seed) {
        visitor(child);
      }
    }
  }

  @override
  void dropChild(RenderObject child) {
    (child.parentData! as _ChunkedTableParentData).clipLayer.layer = null;
    super.dropChild(child);
  }

  @override
  void dispose() {
    for (var child = firstChild; child != null; child = childAfter(child)) {
      (child.parentData! as _ChunkedTableParentData).clipLayer.layer = null;
    }
    super.dispose();
  }
}
