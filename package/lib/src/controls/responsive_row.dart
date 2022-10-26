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

    final spacing = parseResponsiveNumber(control, "spacing", 10);
    final runSpacing = parseResponsiveNumber(control, "runSpacing", 10);
    bool disabled = control.isDisabled || parentDisabled;

    List<Widget> controls = [];

    //bool firstControl = true;
    for (var ctrl in children.where((c) => c.isVisible)) {
      // // spacer between displayed controls
      // if (!firstControl) {
      //   controls.add(SizedBox(width: spacing));
      // }
      // firstControl = false;

      // displayed control
      controls.add(ConstrainedBox(
        constraints: BoxConstraints(
          minWidth: 100,
          maxWidth: 100,
        ),
        child: createControl(control, ctrl.id, disabled),
      ));
    }

    return StoreConnector<AppState, PageSizeViewModel>(
        distinct: true,
        converter: (store) => PageSizeViewModel.fromStore(store),
        builder: (context, view) {
          var w = LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
            debugPrint("constraints.maxWidth: ${constraints.maxWidth}");
            debugPrint("constraints.maxHeight: ${constraints.maxHeight}");

            try {
              return Wrap(
                direction: Axis.horizontal,
                spacing: getBreakpointNumber(
                    spacing, view.size.width, view.breakpoints),
                runSpacing: getBreakpointNumber(
                    runSpacing, view.size.width, view.breakpoints),
                alignment: parseWrapAlignment(
                    control, "alignment", WrapAlignment.start),
                crossAxisAlignment: parseWrapCrossAlignment(
                    control, "verticalAlignment", WrapCrossAlignment.center),
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
