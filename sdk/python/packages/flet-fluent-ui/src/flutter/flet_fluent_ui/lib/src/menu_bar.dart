import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/menu.dart';
import 'utils/theme.dart';

class FluentMenuBarControl extends StatelessWidget {
  final Control control;

  const FluentMenuBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentMenuBar build: ${control.id}");

    // MenuBarItem controls are not rendered: fluent_ui's MenuBar takes
    // MenuBarItem objects. Changes to them, or to their items, rebuild the
    // bar.
    final items = control.children("items").map((item) {
      item.notifyParent = true;
      return MenuBarItem(
        title: item.getString("text", "")!,
        items: buildMenuFlyoutItems(item, "items"),
      );
    }).toList();

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        // fluent_ui asserts that there is a menu.
        items.isEmpty ? const SizedBox.shrink() : MenuBar(items: items),
      ),
    );
  }
}
