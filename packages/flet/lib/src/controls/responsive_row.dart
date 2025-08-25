import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/numbers.dart';
import '../utils/responsive.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';

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
      var result = LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
        // breakpoints
        final rawBreakpoints =
            control.get<Map>("breakpoints", view.breakpoints)!;
        final breakpoints = <String, double>{};
        rawBreakpoints.forEach((k, v) {
          final val = parseDouble(v);
          if (val != null) {
            breakpoints[k.toString()] = val;
          }
        });
        var bpSpacing =
            getBreakpointNumber(spacing, view.size.width, breakpoints);
        var bpColumns =
            getBreakpointNumber(columns, view.size.width, breakpoints);

        double totalCols = 0;
        List<Widget> controls = [];
        for (var ctrl in control.children("controls")) {
          final col = ctrl.getResponsiveNumber("col", 12)!;
          var bpCol = getBreakpointNumber(col, view.size.width, breakpoints);
          totalCols += bpCol;

          // calculate child width
          var colWidth =
              (constraints.maxWidth - bpSpacing * (bpColumns - 1)) / bpColumns;
          var childWidth = colWidth * bpCol + bpSpacing * (bpCol - 1);

          controls.add(ConstrainedBox(
            constraints:
                BoxConstraints(minWidth: childWidth, maxWidth: childWidth),
            child: ControlWidget(key: key, control: ctrl),
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
                  alignment: control.getWrapAlignment(
                      "alignment", WrapAlignment.start)!,
                  crossAxisAlignment: control.getWrapCrossAlignment(
                      "vertical_alignment", WrapCrossAlignment.start)!,
                  children: controls,
                )
              : Row(
                  spacing: bpSpacing - 0.1,
                  mainAxisAlignment: control.getMainAxisAlignment(
                      "alignment", MainAxisAlignment.start)!,
                  mainAxisSize: MainAxisSize.max,
                  crossAxisAlignment: control.getCrossAxisAlignment(
                      "vertical_alignment", CrossAxisAlignment.start)!,
                  children: controls,
                );
        } catch (e) {
          return ErrorControl("Error displaying ResponsiveRow",
              description: e.toString());
        }
      });

      return LayoutControl(control: control, child: result);
    });
  }
}
