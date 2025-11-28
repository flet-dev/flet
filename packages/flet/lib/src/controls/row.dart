import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class RowControl extends StatelessWidget {
  final Control control;

  const RowControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Row build: ${control.id}");

    var spacing = control.getDouble("spacing", 10)!;
    var mainAlignment = parseMainAxisAlignment(
        control.getString("alignment"), MainAxisAlignment.start)!;
    var tight = control.getBool("tight", false)!;
    var wrap = control.getBool("wrap", false)!;
    var intrinsicHeight = control.getBool("intrinsic_height", false)!;
    var verticalAlignment = control.getString("vertical_alignment");
    var controls = control.buildWidgets("controls");

    Widget child = wrap
        ? Wrap(
            direction: Axis.horizontal,
            spacing: spacing,
            runSpacing: control.getDouble("run_spacing", 10)!,
            alignment: parseWrapAlignment(
                control.getString("alignment"), WrapAlignment.start)!,
            runAlignment: parseWrapAlignment(
                control.getString("run_alignment"), WrapAlignment.start)!,
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

    if (intrinsicHeight) {
      child = IntrinsicHeight(child: child);
    }

    child = ScrollableControl(
        control: control,
        scrollDirection: wrap ? Axis.vertical : Axis.horizontal,
        wrapIntoScrollableView: true,
        child: child);

    if (control.getBool("on_scroll", false)!) {
      child = ScrollNotificationControl(control: control, child: child);
    }

    return LayoutControl(control: control, child: child);
  }
}
