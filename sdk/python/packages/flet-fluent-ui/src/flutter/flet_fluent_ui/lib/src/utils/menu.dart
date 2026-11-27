import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

/// Builds fluent_ui menu items from the `MenuFlyoutItem`,
/// `ToggleMenuFlyoutItem`, `RadioMenuFlyoutItem` and `MenuFlyoutSeparator`
/// children of [parent]
/// under [propertyName].
///
/// fluent_ui menus take [MenuFlyoutItemBase] objects, not widgets, and check
/// their types (a [MenuFlyoutSubItem] opens a submenu), so the item controls
/// are not rendered themselves. Each item notifies [parent] when it changes,
/// so the menu is rebuilt with the new items. Other controls are shown as
/// they are.
/// The `trailing` text or control of a menu [item].
///
/// fluent_ui draws trailing text, such as a keyboard shortcut, in a stroke
/// color that is barely visible; WinUI uses the secondary text color.
Widget? _buildTrailing(Control item) {
  final trailing = item.get("trailing");
  if (trailing is! String) return item.buildWidget("trailing");
  return Builder(
    builder: (context) => Text(
      trailing,
      style: TextStyle(
        color: FluentTheme.of(context).resources.textFillColorSecondary,
      ),
    ),
  );
}

List<MenuFlyoutItemBase> buildMenuFlyoutItems(
  Control parent,
  String propertyName,
) {
  return parent.children(propertyName).map((item) {
    item.notifyParent = true;
    final key = ValueKey(item.id);
    switch (item.type) {
      case "FluentMenuFlyoutSeparator":
        return MenuFlyoutSeparator(key: key);
      case "FluentRadioMenuFlyoutItem":
        final group = item.getString("group");
        return RadioMenuFlyoutItem<bool>(
          text: item.buildTextOrWidget("content", required: true)!,
          value: true,
          groupValue: item.getBool("checked", false)!,
          trailing: _buildTrailing(item),
          closeAfterClick: item.getBool("close_on_click", true)!,
          onChanged: item.disabled
              ? null
              : (_) {
                  // Unchecks the other items of the group in this menu.
                  for (final other in parent.children(propertyName)) {
                    if (other != item &&
                        other.type == "FluentRadioMenuFlyoutItem" &&
                        other.getString("group") == group &&
                        other.getBool("checked", false)!) {
                      other.updateProperties({"checked": false});
                    }
                  }
                  item.updateProperties({"checked": true}, notify: true);
                  item.triggerEvent("change", true);
                },
        );
      case "FluentToggleMenuFlyoutItem":
        final value = item.getBool("value", false)!;
        return ToggleMenuFlyoutItem(
          text: item.buildTextOrWidget("content", required: true)!,
          value: value,
          trailing: _buildTrailing(item),
          closeAfterClick: item.getBool("close_on_click", true)!,
          onChanged: item.disabled
              ? null
              : (value) {
                  item.updateProperties({"value": value}, notify: true);
                  item.triggerEvent("change", value);
                },
        );
      case "FluentMenuFlyoutItem":
        final text = item.buildTextOrWidget("content", required: true)!;
        final leading = item.buildIconOrWidget("leading");
        if (item.children("items").isNotEmpty) {
          return MenuFlyoutSubItem(
            key: key,
            text: text,
            leading: leading,
            items: (context) => buildMenuFlyoutItems(item, "items"),
          );
        }
        return MenuFlyoutItem(
          key: key,
          text: text,
          leading: leading,
          trailing: _buildTrailing(item),
          selected: item.getBool("selected", false)!,
          closeAfterClick: item.getBool("close_on_click", true)!,
          onPressed: item.disabled ? null : () => item.triggerEvent("click"),
        );
      default:
        return MenuFlyoutItemBuilder(
          key: key,
          builder: (context) => ControlWidget(control: item),
        );
    }
  }).toList();
}
