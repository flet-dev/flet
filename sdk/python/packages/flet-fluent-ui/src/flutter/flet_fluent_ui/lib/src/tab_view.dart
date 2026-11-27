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

  // fluent_ui's TabView owns its tabs and selection through a controller. The
  // server's `tabs` and `selected_index` are the source of truth: build()
  // copies them into the controller.
  final _controller = TabViewController();

  Control get control => widget.control;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

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

  // fluent_ui has already moved the tab in the controller.
  void _onReorder(int oldIndex, int newIndex) {
    if (!control.hasEventHandler("reorder")) {
      // Tabs are reordered only by an on_reorder handler: put it back.
      _controller.move(newIndex, oldIndex);
      return;
    }
    // Keep the moved selection without rebuilding: a rebuild now would
    // restore the old order until the handler's reordered `tabs` arrive.
    control.updateProperties({"selected_index": _controller.selectedIndex});
    control.triggerEvent("reorder", {
      "old_index": oldIndex,
      "new_index": newIndex,
    });
  }

  // Marks the TabView for rebuild when something changed. That's allowed
  // here: this widget is its ancestor and is building.
  void _syncController(List<Tab> tabs) {
    _controller.replaceTabs(tabs);
    if (tabs.isEmpty) return;
    final index = control
        .getInt("selected_index", 0)!
        .clamp(0, tabs.length - 1);
    if (_controller.selectedIndex != index) _controller.select(index);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTabView build: ${control.id}");

    final tabControls = control.children("tabs");
    final tabs = tabControls.map(_buildTab).toList();
    final ids = tabControls.map((tab) => tab.id).toSet();
    _tabs.removeWhere((id, _) => !ids.contains(id));
    _syncController(tabs);

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        TabView(
          controller: _controller,
          onChanged: _onChanged,
          onNewPressed: control.hasEventHandler("add")
              ? () => control.triggerEvent("add")
              : null,
          onReorder: _onReorder,
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
