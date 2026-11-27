import 'package:flet/flet.dart';
import 'package:fluent_ui/fluent_ui.dart';

import 'utils/theme.dart';

class FluentTreeViewControl extends StatefulWidget {
  final Control control;

  const FluentTreeViewControl({super.key, required this.control});

  @override
  State<FluentTreeViewControl> createState() => _FluentTreeViewControlState();
}

class _FluentTreeViewControlState extends State<FluentTreeViewControl> {
  // TreeViewItem creates a FocusNode unless it is given one, and nothing
  // disposes it; items are rebuilt on every build, so the nodes are kept
  // here, one per item control.
  final _focusNodes = <int, FocusNode>{};
  // The item controls of the last build, and the TreeViewItems built from
  // them, by control id.
  final _itemControls = <int, Control>{};
  final _treeItems = <int, TreeViewItem>{};

  Control get control => widget.control;

  @override
  void dispose() {
    for (final node in _focusNodes.values) {
      node.dispose();
    }
    super.dispose();
  }

  /// Builds fluent_ui's TreeViewItem objects from the item controls, which
  /// are not rendered themselves. A change to an item rebuilds the tree.
  List<TreeViewItem> _buildItems(Control parent) {
    return parent.children("items").map((item) {
      item.notifyParent = true;
      _itemControls[item.id] = item;
      return _treeItems[item.id] = TreeViewItem(
        key: ValueKey(item.id),
        value: item.id,
        content: item.buildTextOrWidget("content", required: true)!,
        leading: item.buildIconOrWidget("leading"),
        children: _buildItems(item),
        expanded: item.getBool("expanded", false)!,
        selected:
            item.get("selected") == null &&
                item.properties.containsKey("selected")
            ? null
            : item.getBool("selected", false)!,
        focusNode: _focusNodes.putIfAbsent(item.id, FocusNode.new),
      );
    }).toList();
  }

  void _disposeUnusedFocusNodes() {
    final unused = _focusNodes.keys
        .where((id) => !_itemControls.containsKey(id))
        .toList();
    if (unused.isEmpty) return;
    final nodes = [for (final id in unused) _focusNodes.remove(id)!];
    // The old items may still use them until the frame is built.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      for (final node in nodes) {
        node.dispose();
      }
    });
  }

  Future<void> _onItemInvoked(
    TreeViewItem item,
    TreeViewItemInvokeReason reason,
  ) async {
    if (reason == TreeViewItemInvokeReason.pressed) {
      _itemControls[item.value]?.triggerEvent("click");
    }
  }

  Future<void> _onExpandToggle(TreeViewItem item, bool expanded) async {
    final itemControl = _itemControls[item.value];
    if (itemControl == null) return;
    // The tree view expands the item itself; no rebuild is needed.
    itemControl.updateProperties({"expanded": expanded});
    itemControl.triggerEvent("expand_change", expanded);
  }

  Future<void> _onSelectionChanged(Iterable<TreeViewItem> _) async {
    // The tree view updates `selected` of its items, including parents
    // with only some children selected (null) in multiple selection mode.
    _treeItems.forEach((id, treeItem) {
      _itemControls[id]?.updateProperties({"selected": treeItem.selected});
    });
    control.triggerEvent("selection_change");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("FluentTreeView build: ${control.id}");

    _itemControls.clear();
    _treeItems.clear();
    final items = _buildItems(control);
    _disposeUnusedFocusNodes();

    return LayoutControl(
      control: control,
      child: withFluentTheme(
        context,
        TreeView(
          items: items,
          selectionMode: parseEnum(
            TreeViewSelectionMode.values,
            control.getString("selection_mode"),
            TreeViewSelectionMode.none,
          )!,
          onItemInvoked: _onItemInvoked,
          onItemExpandToggle: _onExpandToggle,
          onSelectionChanged: control.disabled ? null : _onSelectionChanged,
        ),
      ),
    );
  }
}
