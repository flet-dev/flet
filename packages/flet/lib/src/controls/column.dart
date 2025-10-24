import 'package:flutter/widgets.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';
import 'scroll_notification_control.dart';
import 'scrollable_control.dart';

class ColumnControl extends StatelessWidget {
  final Control control;

  const ColumnControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("Column build: ${control.id}");

    var spacing = control.getDouble("spacing", 10)!;
    var alignment = control.getString("alignment");
    var tight = control.getBool("tight", false)!;
    var wrap = control.getBool("wrap", false)!;
    var horizontalAlignment = control.getString("horizontal_alignment");
    var intrinsicWidth = control.getBool("intrinsic_width", false)!;
    var controls = control.buildWidgets("controls");

    Widget child = wrap
        ? Wrap(
            direction: Axis.vertical,
            spacing: spacing,
            runSpacing: control.getDouble("run_spacing", 10)!,
            alignment: parseWrapAlignment(alignment, WrapAlignment.start)!,
            runAlignment: parseWrapAlignment(
                control.getString("run_alignment"), WrapAlignment.start)!,
            crossAxisAlignment: parseWrapCrossAlignment(
                horizontalAlignment, WrapCrossAlignment.start)!,
            children: controls,
          )
        : Column(
            mainAxisAlignment:
                parseMainAxisAlignment(alignment, MainAxisAlignment.start)!,
            spacing: spacing,
            mainAxisSize: tight ? MainAxisSize.min : MainAxisSize.max,
            crossAxisAlignment: parseCrossAxisAlignment(
                horizontalAlignment, CrossAxisAlignment.start)!,
            children: controls,
          );

    if (intrinsicWidth) {
      child = IntrinsicWidth(child: child);
    }

    child = ScrollableControl(
      control: control,
      scrollDirection: wrap ? Axis.horizontal : Axis.vertical,
      wrapIntoScrollableView: true,
      child: child,
    );

    if (control.getBool("on_scroll", false)!) {
      child = ScrollNotificationControl(control: control, child: child);
    }

    return LayoutControl(control: control, child: child);
  }
}
