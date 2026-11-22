import 'package:material_ui/material_ui.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'transforms.dart';

/// Keys the child of a [Badge] with the [BuildContext] of a `Builder`
/// around it.
///
/// [Badge] places its child alone while the label is hidden and inside a
/// [Stack] while the label is shown, so the child moves when `label_visible`
/// changes. The key, stable while the `Builder` lives, lets Flutter move the
/// child with its state instead of rebuilding it - an open `PopupMenuButton`
/// then still reports `on_cancel` or `on_select`. Each mounted copy of the
/// control gets its own key: widgets like `Draggable` or `DropdownButton`
/// mount the same content twice at once.
class _BadgeChildKey extends GlobalObjectKey {
  const _BadgeChildKey(BuildContext super.value);
}

extension BadgeParsers on Control {
  Widget wrapWithBadge(String propertyName, Widget child, ThemeData theme) {
    var badge = get(propertyName);
    if (badge == null) {
      return child;
    }
    return Builder(
        builder: (context) => _buildBadge(badge,
            KeyedSubtree(key: _BadgeChildKey(context), child: child), theme));
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
