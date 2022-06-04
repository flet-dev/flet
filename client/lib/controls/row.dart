import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import 'create_control.dart';
import 'scrollable_control.dart';

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
    ScrollMode scrollMode = ScrollMode.values.firstWhere(
        (m) =>
            m.name.toLowerCase() ==
            control.attrString("scroll", "")!.toLowerCase(),
        orElse: () => ScrollMode.none);
    final autoScroll = control.attrBool("autoScroll", false)!;
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
      controls.add(createControl(control, ctrl.id, disabled));
    }

    return constrainedControl(
        wrapAutoScroll(
            wrap
                ? Wrap(
                    direction: Axis.horizontal,
                    children: controls,
                    spacing: spacing,
                    runSpacing: control.attrDouble("runSpacing", 10)!,
                    alignment: parseWrapAlignment(
                        control, "alignment", WrapAlignment.start),
                    crossAxisAlignment: parseWrapCrossAlignment(control,
                        "verticalAlignment", WrapCrossAlignment.center),
                  )
                : Row(
                    mainAxisAlignment: mainAlignment,
                    mainAxisSize: tight ? MainAxisSize.min : MainAxisSize.max,
                    crossAxisAlignment: parseCrossAxisAlignment(control,
                        "verticalAlignment", CrossAxisAlignment.center),
                    children: controls,
                  ),
            wrap: wrap,
            scrollMode: scrollMode,
            autoScroll: autoScroll),
        parent,
        control);
  }

  Widget wrapAutoScroll(Widget child,
      {required bool wrap,
      required ScrollMode scrollMode,
      required bool autoScroll}) {
    return scrollMode != ScrollMode.none
        ? ScrollableControl(
            child: child,
            scrollDirection: wrap ? Axis.vertical : Axis.horizontal,
            scrollMode: scrollMode,
            autoScroll: autoScroll,
          )
        : child;
  }
}
