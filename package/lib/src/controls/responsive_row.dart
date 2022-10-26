import 'package:flet/src/controls/error.dart';
import 'package:flet/src/utils/responsive.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/page_size_view_model.dart';
import '../utils/alignment.dart';
import 'create_control.dart';

class ResponsiveRowControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const ResponsiveRowControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("ResponsiveRowControl build: ${control.id}");

    final columns = parseResponsiveNumber(control, "columns", 12);
    final spacing = parseResponsiveNumber(control, "spacing", 10);
    final runSpacing = parseResponsiveNumber(control, "runSpacing", 10);
    bool disabled = control.isDisabled || parentDisabled;

    return StoreConnector<AppState, PageSizeViewModel>(
        distinct: true,
        converter: (store) => PageSizeViewModel.fromStore(store),
        builder: (context, view) {
          var w = LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
            // debugPrint("constraints.maxWidth: ${constraints.maxWidth}");
            // debugPrint("constraints.maxHeight: ${constraints.maxHeight}");

            var bpSpacing =
                getBreakpointNumber(spacing, view.size.width, view.breakpoints);

            var bpColumns =
                getBreakpointNumber(columns, view.size.width, view.breakpoints);

            double totalCols = 0;
            List<Widget> controls = [];
            for (var ctrl in children.where((c) => c.isVisible)) {
              final col = parseResponsiveNumber(ctrl, "col", 12);
              var bpCol =
                  getBreakpointNumber(col, view.size.width, view.breakpoints);
              totalCols += bpCol;

              // calculate child width
              var colWidth =
                  (constraints.maxWidth - bpSpacing * (bpColumns - 1)) /
                      bpColumns;
              var childWidth = colWidth * bpCol + bpSpacing * (bpCol - 1);

              controls.add(ConstrainedBox(
                constraints: BoxConstraints(
                  minWidth: childWidth,
                  maxWidth: childWidth,
                ),
                child: createControl(control, ctrl.id, disabled),
              ));
            }

            var wrap = (totalCols > bpColumns);

            if (!wrap && bpSpacing > 0) {
              var i = 1;
              while (i < controls.length) {
                controls.insert(i, SizedBox(width: bpSpacing));
                i += 2;
              }
            }

            try {
              return wrap
                  ? Wrap(
                      direction: Axis.horizontal,
                      spacing: bpSpacing - 0.1,
                      runSpacing: getBreakpointNumber(
                          runSpacing, view.size.width, view.breakpoints),
                      alignment: parseWrapAlignment(
                          control, "alignment", WrapAlignment.start),
                      crossAxisAlignment: parseWrapCrossAlignment(control,
                          "verticalAlignment", WrapCrossAlignment.center),
                      children: controls,
                    )
                  : Row(
                      mainAxisAlignment: parseMainAxisAlignment(
                          control, "alignment", MainAxisAlignment.start),
                      mainAxisSize: MainAxisSize.max,
                      crossAxisAlignment: parseCrossAxisAlignment(control,
                          "verticalAlignment", CrossAxisAlignment.center),
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
