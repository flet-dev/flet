import '../models/page_breakpoint_view_model.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import 'create_control.dart';

class RowControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  const RowControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Row build: ${control.id}");

    final spacing = control.attrDouble("spacing", 10)!;
    final mainAlignment =
        parseMainAxisAlignment(control, "alignment", MainAxisAlignment.start);
    bool tight = control.attrBool("tight", false)!;
    bool wrap = control.attrBool("wrap", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    List<Widget> controls = [];

    bool firstControl = true;
    for (var ctrl in children.where((c) => c.isVisible)) {
      // spacer between displayed controls
      if (!wrap &&
          spacing > 0 &&
          !firstControl &&
          mainAlignment != MainAxisAlignment.spaceAround &&
          mainAlignment != MainAxisAlignment.spaceBetween &&
          mainAlignment != MainAxisAlignment.spaceEvenly) {
        controls.add(SizedBox(width: spacing));
      }
      firstControl = false;

      // displayed control
      controls.add(createControl(parent, ctrl.id, disabled));
    }

    return commonControl(
        wrap
            ? Wrap(
                direction: Axis.horizontal,
                children: controls,
                spacing: spacing,
                runSpacing: control.attrDouble("runSpacing", 10)!,
                alignment: parseWrapAlignment(
                    control, "alignment", WrapAlignment.start),
                crossAxisAlignment: parseWrapCrossAlignment(
                    control, "verticalAlignment", WrapCrossAlignment.center),
              )
            : Row(
                mainAxisAlignment: mainAlignment,
                mainAxisSize: tight ? MainAxisSize.min : MainAxisSize.max,
                crossAxisAlignment: parseCrossAxisAlignment(
                    control, "verticalAlignment", CrossAxisAlignment.center),
                children: controls,
              ),
        parent,
        control);
  }
}
