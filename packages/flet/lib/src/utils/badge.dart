import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'transforms.dart';

/// A key per control with a badge, stable while the control lives.
///
/// [Badge] places its child alone while the label is hidden and inside a
/// [Stack] while the label is shown. The child is keyed with a
/// [GlobalObjectKey] made from this object, so it keeps its state when the
/// label is shown or hidden, or the badge is replaced.
final Expando<Object> _badgedChildKeys = Expando('badged child keys');

extension BadgeParsers on Control {
  Widget wrapWithBadge(String propertyName, Widget child, ThemeData theme) {
    var badge = get(propertyName);
    if (badge == null) {
      return child;
    }
    child = KeyedSubtree(
        key: GlobalObjectKey(_badgedChildKeys[this] ??= Object()),
        child: child);
    if (badge is Control) {
      badge.notifyParent = true;
      return Badge(
        label: badge.buildTextOrWidget("label"),
        isLabelVisible: badge.getBool("label_visible", true)!,
        offset: badge.getOffset("offset"),
        alignment: badge.getAlignment("alignment"),
        backgroundColor: parseColor(badge.get("bgcolor"), theme),
        largeSize: badge.getDouble("large_size"),
        padding: badge.getPadding("padding"),
        smallSize: badge.getDouble("small_size"),
        textColor: parseColor(badge.get("text_color"), theme),
        textStyle: badge.getTextStyle("text_style", theme),
        child: child,
      );
    }
    return Badge(label: Text(badge.toString()), child: child);
  }
}
