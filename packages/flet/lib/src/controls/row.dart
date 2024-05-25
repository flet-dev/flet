import 'package:flutter/widgets.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import 'create_control.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class RowControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final List<Control> children;
  final FletControlBackend backend;

  const RowControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("Row build: ${control.id}");

    final spacing = control.attrDouble("spacing", 10)!;
    final mainAlignment = parseMainAxisAlignment(
        control.attrString("alignment"), MainAxisAlignment.start)!;
    bool tight = control.attrBool("tight", false)!;
    bool wrap = control.attrBool("wrap", false)!;
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;

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
      controls.add(
          createControl(control, ctrl.id, disabled, parentAdaptive: adaptive));
    }

    Widget child = wrap
        ? Wrap(
            direction: Axis.horizontal,
            spacing: spacing,
            runSpacing: control.attrDouble("runSpacing", 10)!,
            alignment: parseWrapAlignment(
                control.attrString("alignment"), WrapAlignment.start)!,
            crossAxisAlignment: parseWrapCrossAlignment(
                control.attrString("verticalAlignment"),
                WrapCrossAlignment.center)!,
            children: controls,
          )
        : Row(
            mainAxisAlignment: mainAlignment,
            mainAxisSize: tight ? MainAxisSize.min : MainAxisSize.max,
            crossAxisAlignment: parseCrossAxisAlignment(
                control.attrString("verticalAlignment"),
                CrossAxisAlignment.center)!,
            children: controls,
          );

    child = ScrollableControl(
        control: control,
        scrollDirection: wrap ? Axis.vertical : Axis.horizontal,
        backend: backend,
        parentAdaptive: adaptive,
        child: child);

    if (control.attrBool("onScroll", false)!) {
      child = ScrollNotificationControl(
          control: control, backend: backend, child: child);
    }

    return constrainedControl(context, child, parent, control);
  }
}
