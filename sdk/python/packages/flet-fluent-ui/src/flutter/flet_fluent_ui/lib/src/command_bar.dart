import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// A control other than a command, such as a search box, shown as it is.
class _ControlCommandBarItem extends CommandBarItem {
  final Control control;

  _ControlCommandBarItem(this.control) : super(key: ValueKey(control.id));

  @override
  Widget build(BuildContext context, CommandBarItemDisplayMode displayMode) =>
      ControlWidget(control: control);
}

/// Builds fluent_ui command bar items from the `CommandBarButton` and
/// `CommandBarSeparator` children of [control] under [propertyName].
///
/// fluent_ui's CommandBar takes [CommandBarItem] objects, which it builds
/// differently in the bar and in the "More" menu, so the item controls are
/// not rendered themselves. Each item notifies [control] when it changes.
List<CommandBarItem> _buildItems(Control control, String propertyName) {
  return control.children(propertyName).map((item) {
    final key = ValueKey(item.id);
    switch (item.type) {
      case "FluentCommandBarButton":
        item.notifyParent = true;
        return CommandBarButton(
          key: key,
          label: item.buildTextOrWidget("content"),
          icon: item.buildIconOrWidget("icon"),
          tooltip: item.getString("tooltip"),
          onPressed: item.disabled ? null : () => item.triggerEvent("click"),
        );
      case "FluentCommandBarSeparator":
        item.notifyParent = true;
        return CommandBarSeparator(
          key: key,
          color: item.getColor("color", null),
          thickness: item.getDouble("thickness"),
        );
      default:
        return _ControlCommandBarItem(item);
    }
  }).toList();
}

class FluentCommandBarControl extends StatelessWidget {
  final Control control;

  const FluentCommandBarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentCommandBar build: ${control.id}");

    final commandBar = CommandBar(
      primaryItems: _buildItems(control, "primary_items"),
      secondaryItems: _buildItems(control, "secondary_items"),
      overflowBehavior: parseEnum(
        CommandBarOverflowBehavior.values,
        control.getString("overflow_behavior"),
        CommandBarOverflowBehavior.dynamicOverflow,
      )!,
      isCompact: control.getBool("compact", false)!,
      mainAxisAlignment: control.getMainAxisAlignment(
        "alignment",
        MainAxisAlignment.start,
      )!,
    );

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        control.getBool("card", false)!
            ? CommandBarCard(child: commandBar)
            : commandBar,
      ),
    );
  }
}
