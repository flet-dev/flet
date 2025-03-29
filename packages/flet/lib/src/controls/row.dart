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
    bool disabled = control.disabled || parentDisabled;
    bool? adaptive = control.getBool("adaptive") ?? parentAdaptive;

    var spacing = control.getDouble("spacing", 10)!;
    var mainAlignment = parseMainAxisAlignment(
        control.getString("alignment"), MainAxisAlignment.start)!;
    var tight = control.getBool("tight", false)!;
    var wrap = control.getBool("wrap", false)!;
    var verticalAlignment = control.getString("verticalAlignment");

    List<Widget> controls = children.where((c) => c.visible).map((c) {
      return createControl(control, c.id, disabled, parentAdaptive: adaptive);
    }).toList();

    Widget child = wrap
        ? Wrap(
            direction: Axis.horizontal,
            spacing: spacing,
            runSpacing: control.getDouble("runSpacing", 10)!,
            alignment: parseWrapAlignment(
                control.getString("alignment"), WrapAlignment.start)!,
            runAlignment: parseWrapAlignment(
                control.getString("runAlignment"), WrapAlignment.start)!,
            crossAxisAlignment: parseWrapCrossAlignment(
                verticalAlignment, WrapCrossAlignment.center)!,
            children: controls,
          )
        : Row(
            spacing: spacing,
            mainAxisAlignment: mainAlignment,
            mainAxisSize: tight ? MainAxisSize.min : MainAxisSize.max,
            crossAxisAlignment: parseCrossAxisAlignment(
                verticalAlignment, CrossAxisAlignment.center)!,
            children: controls,
          );

    child = ScrollableControl(
        control: control,
        scrollDirection: wrap ? Axis.vertical : Axis.horizontal,
        backend: backend,
        parentAdaptive: adaptive,
        child: child);

    if (control.getBool("onScroll", false)!) {
      child = ScrollNotificationControl(
          control: control, backend: backend, child: child);
    }

    return constrainedControl(context, child, parent, control);
  }
}
