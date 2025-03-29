import 'package:flutter/widgets.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/responsive.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class ResponsiveRowControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final FletControlBackend backend;

  const ResponsiveRowControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("ResponsiveRowControl build: ${control.id}");

    final columns = parseResponsiveNumber(control, "columns", 12);
    final spacing = parseResponsiveNumber(control, "spacing", 10);
    final runSpacing = parseResponsiveNumber(control, "runSpacing", 10);
    bool disabled = control.disabled || parentDisabled;
    bool? adaptive = control.getBool("adaptive") ?? parentAdaptive;
    return withPageSize((context, view) {
      var w = LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint(
            "ResponsiveRow constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint(
            "ResponsiveRow constraints.maxHeight: ${constraints.maxHeight}");

        var bpSpacing =
            getBreakpointNumber(spacing, view.size.width, view.breakpoints);

        var bpColumns =
            getBreakpointNumber(columns, view.size.width, view.breakpoints);

        double totalCols = 0;
        List<Widget> controls = [];
        for (var ctrl in children.where((c) => c.visible)) {
          final col = parseResponsiveNumber(ctrl, "col", 12);
          var bpCol =
              getBreakpointNumber(col, view.size.width, view.breakpoints);
          totalCols += bpCol;

          // calculate child width
          var colWidth =
              (constraints.maxWidth - bpSpacing * (bpColumns - 1)) / bpColumns;
          var childWidth = colWidth * bpCol + bpSpacing * (bpCol - 1);

          controls.add(ConstrainedBox(
            constraints: BoxConstraints(
              minWidth: childWidth,
              maxWidth: childWidth,
            ),
            child: createControl(control, ctrl.id, disabled,
                parentAdaptive: adaptive),
          ));
        }

        var wrap = (totalCols > bpColumns);

        try {
          return wrap
              ? Wrap(
                  direction: Axis.horizontal,
                  spacing: bpSpacing - 0.1,
                  runSpacing: getBreakpointNumber(
                      runSpacing, view.size.width, view.breakpoints),
                  alignment: parseWrapAlignment(
                      control.getString("alignment"), WrapAlignment.start)!,
                  crossAxisAlignment: parseWrapCrossAlignment(
                      control.getString("verticalAlignment"),
                      WrapCrossAlignment.start)!,
                  children: controls,
                )
              : Row(
                  spacing: bpSpacing - 0.1,
                  mainAxisAlignment: parseMainAxisAlignment(
                      control.getString("alignment"), MainAxisAlignment.start)!,
                  mainAxisSize: MainAxisSize.max,
                  crossAxisAlignment: parseCrossAxisAlignment(
                      control.getString("verticalAlignment"),
                      CrossAxisAlignment.start)!,
                  children: controls,
                );
        } catch (e) {
          return ErrorControl(
            "Error displaying ResponsiveRow",
            description: e.toString(),
          );
        }
      });

      return constrainedControl(context, w, parent, control);
    });
  }
}
