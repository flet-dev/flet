import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class NavigationDrawerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const NavigationDrawerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<NavigationDrawerControl> createState() =>
      _NavigationDrawerControlState();
}

class _NavigationDrawerControlState extends State<NavigationDrawerControl>
    with FletStoreMixin {
  int _selectedIndex = 0;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationDrawerControl build: ${widget.control.id}");

    bool disabled = widget.control.disabled || widget.parentDisabled;
    var selectedIndex = widget.control.getInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    return withControls(
        widget.children
            .where((c) => c.visible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      List<Widget> children = viewModel.controlViews.map((destView) {
        if (destView.control.type == "navigationdrawerdestination") {
          var iconStr = parseIcon(destView.control.getString("icon"));
          var iconCtrls =
              destView.children.where((c) => c.name == "icon" && c.visible);
          // if no control provided in "icon" property, replace iconCtrls with control provided in icon_content, if any
          // the line below needs to be deleted after icon_content is deprecated
          iconCtrls = iconCtrls.isEmpty
              ? destView.children
                  .where((c) => c.name == "icon_content" && c.visible)
              : iconCtrls;

          var selectedIconStr =
              parseIcon(destView.control.getString("selectedIcon"));
          var selectedIconCtrls = destView.children
              .where((c) => c.name == "selected_icon" && c.visible);
          // if no control provided in "selected_icon" property, replace selectedIconCtrls with control provided in selected_icon_content, if any
          // the line below needs to be deleted after selected_icon_content is deprecated
          selectedIconCtrls = selectedIconCtrls.isEmpty
              ? destView.children
                  .where((c) => c.name == "selected_icon_content" && c.visible)
              : selectedIconCtrls;
          return NavigationDrawerDestination(
            enabled: !(disabled || destView.control.disabled),
            backgroundColor: destView.control.getColor("bgColor", context),
            icon: iconCtrls.isNotEmpty
                ? createControl(destView.control, iconCtrls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : Icon(iconStr),
            label: Text(destView.control.getString("label", "")!),
            selectedIcon: selectedIconCtrls.isNotEmpty
                ? createControl(
                    destView.control, selectedIconCtrls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : selectedIconStr != null
                    ? Icon(selectedIconStr)
                    : null,
          );
        } else {
          return createControl(widget.control, destView.control.id, disabled,
              parentAdaptive: widget.parentAdaptive);
        }
      }).toList();

      var drawer = NavigationDrawer(
        elevation: widget.control.getDouble("elevation"),
        indicatorColor: widget.control.getColor("indicatorColor", context),
        indicatorShape: parseOutlinedBorder(widget.control, "indicatorShape"),
        backgroundColor: widget.control.getColor("bgColor", context),
        selectedIndex: _selectedIndex,
        shadowColor: widget.control.getColor("shadowColor", context),
        surfaceTintColor: widget.control.getColor("surfaceTintColor", context),
        tilePadding: parseEdgeInsets(widget.control, "tilePadding",
            const EdgeInsets.symmetric(horizontal: 12.0))!,
        onDestinationSelected: _destinationChanged,
        children: children,
      );

      return baseControl(context, drawer, widget.parent, widget.control);
    });
  }
}
