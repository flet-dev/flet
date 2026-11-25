import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

/// Builds fluent_ui pane items from the `PaneItem`, `PaneItemHeader` and
/// `PaneItemSeparator` children of [parent] under [propertyName].
///
/// NavigationPane takes NavigationPaneItem objects, not widgets, so the item
/// controls are not rendered themselves; a change to an item rebuilds the
/// view. Items are keyed by control id, which also keeps the content of each
/// page alive when the view is rebuilt.
List<NavigationPaneItem> _buildPaneItems(Control parent, String propertyName) {
  return parent.children(propertyName).map((item) {
    item.notifyParent = true;
    final key = ValueKey(item.id);
    switch (item.type) {
      case "FluentPaneItemHeader":
        return PaneItemHeader(
          key: key,
          header: item.buildTextOrWidget("content", required: true)!,
        );
      case "FluentPaneItemSeparator":
        return PaneItemSeparator(
          key: key,
          color: item.getColor("color", null),
          thickness: item.getDouble("thickness"),
        );
      case "FluentPaneItem":
        return _buildPaneItem(item, key);
      default:
        return PaneItemWidgetAdapter(
          key: key,
          child: ControlWidget(control: item),
        );
    }
  }).toList();
}

PaneItem _buildPaneItem(Control item, Key key) {
  final icon = item.buildIconOrWidget("icon") ?? const SizedBox.shrink();
  final title = item.buildTextOrWidget("title", required: true);
  final body = item.buildWidget("content");
  final infoBadge = item.buildWidget("info_badge");
  final trailing = item.buildWidget("trailing");
  final tooltip = item.get("tooltip") is String
      ? item.getString("tooltip")
      : null;
  final onTap = item.disabled ? null : () => item.triggerEvent("click");
  final children = _buildPaneItems(item, "items");

  if (children.isNotEmpty) {
    return PaneItemExpander(
      key: key,
      icon: icon,
      title: title,
      body: body,
      items: children,
      infoBadge: infoBadge,
      trailing: trailing ?? PaneItemExpander.kDefaultTrailing,
      initiallyExpanded: item.getBool("expanded", false)!,
      onTap: onTap,
    );
  }
  if (body == null) {
    // Not a page: it only reports clicks.
    return PaneItemAction(
      key: key,
      icon: icon,
      title: title,
      infoBadge: infoBadge,
      trailing: trailing,
      enabled: !item.disabled,
      tooltip: tooltip,
      onTap: onTap ?? () {},
    );
  }
  return PaneItem(
    key: key,
    icon: icon,
    title: title,
    body: body,
    infoBadge: infoBadge,
    trailing: trailing,
    enabled: !item.disabled,
    tooltip: tooltip,
    onTap: onTap,
  );
}

/// The number of pages (pane items with content) under [propertyName] of
/// [parent], including the items of expandable items, in the order
/// fluent_ui counts them for `selected`.
int _countPages(Control parent, String propertyName) {
  return parent.children(propertyName).fold(0, (count, item) {
    if (item.type != "FluentPaneItem") return count;
    return count +
        (item.child("content") != null ? 1 : 0) +
        _countPages(item, "items");
  });
}

class FluentNavigationViewControl extends StatefulWidget {
  final Control control;

  const FluentNavigationViewControl({super.key, required this.control});

  @override
  State<FluentNavigationViewControl> createState() =>
      _FluentNavigationViewControlState();
}

class _FluentNavigationViewControlState
    extends State<FluentNavigationViewControl> {
  final _viewKey = GlobalKey<NavigationViewState>();

  Control get control => widget.control;

  void _onChanged(int index) {
    // fluent_ui leaves a compact or minimal pane open over the content after
    // an item is picked in it; WinUI closes it.
    _viewKey.currentState?.closePane();
    control.updateProperties({"selected_index": index}, notify: true);
    control.triggerEvent("change", index);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentNavigationView build: ${control.id}");

    final selectedIndex = control.getInt("selected_index");
    final pageCount =
        _countPages(control, "items") + _countPages(control, "footer_items");
    // fluent_ui asserts that the index is one of the pages.
    final selected =
        selectedIndex != null && selectedIndex >= 0 && selectedIndex < pageCount
        ? selectedIndex
        : null;

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        NavigationView(
          key: _viewKey,
          // fluent_ui's content area shows the selected page and fails when
          // there is none, unless it is given a builder; the builder is used
          // only then, as the content area without it animates page changes
          // and keeps pages alive.
          paneBodyBuilder: selected == null
              ? (item, body) => const SizedBox.shrink()
              : null,
          pane: NavigationPane(
            selected: selected,
            items: _buildPaneItems(control, "items"),
            footerItems: _buildPaneItems(control, "footer_items"),
            header: control.buildTextOrWidget("header"),
            displayMode: parseEnum(
              PaneDisplayMode.values,
              control.getString("display_mode"),
              PaneDisplayMode.auto,
            )!,
            onChanged: control.disabled ? null : _onChanged,
          ),
        ),
      ),
    );
  }
}

class FluentScaffoldPageControl extends StatelessWidget {
  final Control control;

  const FluentScaffoldPageControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentScaffoldPage build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        ScaffoldPage(
          header: control.buildWidget("header"),
          content: control.buildWidget("content") ?? const SizedBox.expand(),
          footer: control.buildWidget("footer"),
          padding: control.getPadding("padding"),
          backgroundColor: control.getColor("bgcolor", context),
        ),
      ),
    );
  }
}

class FluentPageHeaderControl extends StatelessWidget {
  final Control control;

  const FluentPageHeaderControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentPageHeader build: ${control.id}");

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        PageHeader(
          title: control.buildTextOrWidget("title"),
          leading: control.buildWidget("leading"),
          commandBar: control.buildWidget("command_bar"),
        ),
      ),
    );
  }
}
