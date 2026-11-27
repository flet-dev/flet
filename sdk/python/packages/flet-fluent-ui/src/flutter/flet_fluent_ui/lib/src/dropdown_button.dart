import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/menu.dart';
import 'utils/theme.dart';

class FluentDropDownButtonControl extends StatelessWidget {
  final Control control;

  const FluentDropDownButtonControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentDropDownButton build: ${control.id}");

    final items = buildMenuFlyoutItems(control, "items");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        DropDownButton(
          title: control.buildTextOrWidget("content"),
          leading: control.buildIconOrWidget("leading"),
          // fluent_ui asserts that there is an item; the button is disabled
          // without any, so the placeholder never shows.
          items: items.isEmpty ? [const MenuFlyoutSeparator()] : items,
          disabled: control.disabled || items.isEmpty,
          autofocus: control.getBool("autofocus", false)!,
          placement: parseEnum(
            FlyoutPlacementMode.values,
            control.getString("placement"),
            FlyoutPlacementMode.bottomCenter,
          )!,
          onOpen: () => control.triggerEvent("open"),
          onClose: () => control.triggerEvent("dismiss"),
        ),
      ),
    );
  }
}

class FluentSplitButtonControl extends StatelessWidget {
  final Control control;

  const FluentSplitButtonControl({super.key, required this.control});

  void _onInvoked() {
    final checked = control.getBool("checked");
    if (checked != null) {
      control.updateProperties({"checked": !checked}, notify: true);
      control.triggerEvent("change", !checked);
    }
    control.triggerEvent("click");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentSplitButton build: ${control.id}");

    final checked = control.getBool("checked");
    final enabled = !control.disabled;
    // fluent_ui shows the label without padding; this is Button's.
    final child = Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(11, 5, 11, 6),
      child: control.buildTextOrWidget("content", required: true),
    );
    final flyoutContent = control.buildWidget("flyout");
    final flyout = flyoutContent != null
        ? FlyoutContent(child: flyoutContent)
        : MenuFlyout(items: buildMenuFlyoutItems(control, "items"));

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        checked == null
            ? SplitButton(
                enabled: enabled,
                onInvoked: _onInvoked,
                flyout: flyout,
                child: child,
              )
            : SplitButton.toggle(
                checked: checked,
                enabled: enabled,
                onInvoked: _onInvoked,
                flyout: flyout,
                child: child,
              ),
      ),
    );
  }
}
