import 'dart:math';

import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/numbers.dart';
import '../utils/responsive.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ResponsiveRowControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const ResponsiveRowControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ResponsiveRowControl build: ${control.id}");

    final columns = control.getResponsiveNumber("columns", 12)!;
    final spacing = control.getResponsiveNumber("spacing", 10)!;
    final runSpacing = control.getResponsiveNumber("run_spacing", 10)!;

    return withPageSize((context, view) {
      Widget result = LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
        if (!constraints.hasBoundedWidth) {
          return const ErrorControl(
            "Error displaying ResponsiveRow: width is unbounded.",
            description:
                "Set a fixed width, a non-zero expand, or place it inside a control with bounded width.",
          );
        }

        // Resolve the active breakpoint map once per layout pass. Responsive
        // properties such as `columns`, `spacing`, and child `col` values are
        // all interpreted against this map.
        final rawBreakpoints =
            control.get<Map>("breakpoints", view.breakpoints)!;
        final breakpoints = <String, double>{};
        rawBreakpoints.forEach((k, v) {
          final val = parseDouble(v);
          if (val != null) {
            breakpoints[k.toString()] = val;
          }
        });
        var bpSpacing = max(
            0.0, getBreakpointNumber(spacing, view.size.width, breakpoints));
        var bpColumns =
            getBreakpointNumber(columns, view.size.width, breakpoints);

        double totalCols = 0;
        double totalWidth = 0;
        List<Widget> controls = [];
        for (var ctrl in control.children("controls")) {
          final col = ctrl.getResponsiveNumber("col", 12)!;
          var bpCol = getBreakpointNumber(col, view.size.width, breakpoints);

          // `col=0` means "do not occupy any columns" for the current
          // breakpoint, so the child should not participate in layout.
          if (bpCol <= 0) {
            continue;
          }

          totalCols += bpCol;

          // Convert virtual columns into a fixed pixel width for this child.
          // We first remove the total horizontal gaps from the available width,
          // then divide the remaining width across the configured columns.
          // 0.1px is left unused so rounding never makes a full row of
          // children wider than the available width.
          var colWidth =
              (constraints.maxWidth - 0.1 - bpSpacing * (bpColumns - 1)) /
                  bpColumns;
          var childWidth = colWidth * bpCol + bpSpacing * (bpCol - 1);

          // Guard against tiny/invalid available widths so Flutter never sees
          // negative box constraints.
          if (childWidth < 0) {
            childWidth = 0;
          }
          totalWidth += childWidth + (controls.isEmpty ? 0 : bpSpacing);

          // Key the child with a GlobalKey tied to its Control identity so
          // that when this build switches between Row and Wrap (a different
          // widget type at the same slot), Flutter re-parents the existing
          // Element instead of re-inflating the subtree — otherwise stateful
          // descendants (video players, WebViews, scroll positions) would
          // lose their State on every breakpoint change.
          controls.add(ConstrainedBox(
            constraints:
                BoxConstraints(minWidth: childWidth, maxWidth: childWidth),
            child: ControlWidget(key: GlobalObjectKey(ctrl), control: ctrl),
          ));
        }

        // Wrap when the children take more columns than the row has, or when
        // they don't fit in pixels: widths clamped to zero still leave their gaps.
        var wrap = totalCols > bpColumns || totalWidth > constraints.maxWidth;

        try {
          // Keep a single row when everything fits; otherwise switch to Wrap so
          // children can continue on the next line.
          if (wrap) {
            return Wrap(
              direction: Axis.horizontal,
              spacing: bpSpacing,
              runSpacing: max(
                  0.0,
                  getBreakpointNumber(
                      runSpacing, view.size.width, breakpoints)),
              alignment:
                  control.getWrapAlignment("alignment", WrapAlignment.start)!,
              crossAxisAlignment: control.getWrapCrossAlignment(
                  "vertical_alignment", WrapCrossAlignment.start)!,
              children: controls,
            );
          }

          final crossAxisAlignment = control.getCrossAxisAlignment(
              "vertical_alignment", CrossAxisAlignment.start)!;

          Widget row = Row(
            spacing: bpSpacing,
            mainAxisAlignment: control.getMainAxisAlignment(
                "alignment", MainAxisAlignment.start)!,
            mainAxisSize: MainAxisSize.max,
            crossAxisAlignment: crossAxisAlignment,
            // Required by `CrossAxisAlignment.baseline`, ignored otherwise.
            textBaseline: TextBaseline.alphabetic,
            children: controls,
          );

          // `IntrinsicHeight` is only needed when the row is both vertically
          // scrollable (unbounded height) and asked to stretch children
          // cross-axis — otherwise the row sizes to its children naturally,
          // so we avoid the extra intrinsic-sizing pass.
          if (control.get("scroll") != null &&
              crossAxisAlignment == CrossAxisAlignment.stretch) {
            row = IntrinsicHeight(child: row);
          }

          return row;
        } catch (e) {
          return ErrorControl("Error displaying ResponsiveRow",
              description: e.toString());
        }
      });

      result = ScrollableControl(
          control: control,
          scrollDirection: Axis.vertical,
          wrapIntoScrollableView: true,
          child: result);

      if (control.hasEventHandler("scroll")) {
        result = ScrollNotificationControl(control: control, child: result);
      }

      return LayoutControl(control: control, child: result);
    });
  }
}
