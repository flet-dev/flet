import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'transforms.dart';

/// Keys a control's widget with the [BuildContext] of a `Builder` around it.
///
/// Changes to the control's badge move its widget in the tree. The key lets
/// Flutter keep the widget's state through those moves. Each mounted copy of
/// the control gets its own key, since some widgets mount the same content
/// twice at once.
class _BadgeChildKey extends GlobalObjectKey {
  const _BadgeChildKey(BuildContext super.value);
}

extension BadgeParsers on Control {
  /// Wraps [child] in the badge set in [propertyName], if any.
  ///
  /// [child] is keyed with a [_BadgeChildKey], with or without a badge.
  Widget wrapWithBadge(String propertyName, Widget child, ThemeData theme) {
    return Builder(builder: (context) {
      final keyed = KeyedSubtree(key: _BadgeChildKey(context), child: child);
      final badge = get(propertyName);
      return badge == null ? keyed : _buildBadge(badge, keyed, theme);
    });
  }

  Widget _buildBadge(dynamic badge, Widget child, ThemeData theme) {
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
