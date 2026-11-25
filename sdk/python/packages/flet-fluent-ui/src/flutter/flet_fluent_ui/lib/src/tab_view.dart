import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentTabViewControl extends StatefulWidget {
  final Control control;

  const FluentTabViewControl({super.key, required this.control});

  @override
  State<FluentTabViewControl> createState() => _FluentTabViewControlState();
}

class _FluentTabViewControlState extends State<FluentTabViewControl> {
  // fluent_ui tells tabs apart by instance (the body of each tab is keyed by
  // its Tab, which also holds a GlobalKey), so a new Tab would build the
  // tab's content from scratch. A Tab is reused for as long as the
  // properties it is built from stay the same.
  final _tabs = <int, (String, Tab)>{};

  Control get control => widget.control;

  Tab _buildTab(Control tab) {
    tab.notifyParent = true;
    final text = tab.get("text");
    final icon = tab.get("icon");
    final content = tab.child("content");
    final signature = [
      text is Control ? text.id : text,
      icon is Control ? icon.id : icon,
      content?.id,
      tab.disabled,
      tab.hasEventHandler("close"),
    ].join("|");
    final cached = _tabs[tab.id];
    if (cached != null && cached.$1 == signature) return cached.$2;

    final built = Tab(
      key: ValueKey(tab.id),
      text: tab.buildTextOrWidget("text", required: true)!,
      icon: tab.buildIconOrWidget("icon"),
      body: content == null
          ? const SizedBox.shrink()
          : ControlWidget(key: ValueKey(content.id), control: content),
      disabled: tab.disabled,
      onClosed: tab.hasEventHandler("close")
          ? () => tab.triggerEvent("close")
          : null,
    );
    _tabs[tab.id] = (signature, built);
    return built;
  }

  void _onChanged(int index) {
    control.updateProperties({"selected_index": index}, notify: true);
    control.triggerEvent("change", index);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTabView build: ${control.id}");

    final tabControls = control.children("tabs");
    final tabs = tabControls.map(_buildTab).toList();
    final ids = tabControls.map((tab) => tab.id).toSet();
    _tabs.removeWhere((id, _) => !ids.contains(id));

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        TabView(
          tabs: tabs,
          currentIndex: tabs.isEmpty
              ? 0
              : control.getInt("selected_index", 0)!.clamp(0, tabs.length - 1),
          onChanged: _onChanged,
          onNewPressed: control.hasEventHandler("add")
              ? () => control.triggerEvent("add")
              : null,
          onReorder: control.hasEventHandler("reorder")
              ? (oldIndex, newIndex) => control.triggerEvent("reorder", {
                  "old_index": oldIndex,
                  "new_index": newIndex,
                })
              : null,
          tabWidthBehavior: parseEnum(
            TabWidthBehavior.values,
            control.getString("tab_width_behavior"),
            TabWidthBehavior.equal,
          )!,
          closeButtonVisibility: parseEnum(
            CloseButtonVisibilityMode.values,
            control.getString("close_button_visibility"),
            CloseButtonVisibilityMode.always,
          )!,
          showScrollButtons: control.getBool("show_scroll_buttons", true)!,
          header: control.buildWidget("header"),
          footer: control.buildWidget("footer"),
        ),
      ),
    );
  }
}
