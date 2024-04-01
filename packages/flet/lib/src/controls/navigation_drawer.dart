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

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var navDrawer = withControls(
        widget.children
            .where((c) => c.isVisible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      List<Widget> children = viewModel.controlViews.map((destView) {
        if (destView.control.type == "navigationdrawerdestination") {
          var icon = parseIcon(destView.control.attrString("icon", "")!);
          var iconContentCtrls =
              destView.children.where((c) => c.name == "icon_content");
          var selectedIcon =
              parseIcon(destView.control.attrString("selectedIcon", "")!);
          var selectedIconContentCtrls =
              destView.children.where((c) => c.name == "selected_icon_content");
          return NavigationDrawerDestination(
            backgroundColor: destView.control.attrColor("bgColor", context),
            icon: iconContentCtrls.isNotEmpty
                ? createControl(
                    destView.control, iconContentCtrls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : Icon(icon),
            label: Text(destView.control.attrString("label", "")!),
            selectedIcon: selectedIconContentCtrls.isNotEmpty
                ? createControl(destView.control,
                    selectedIconContentCtrls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : selectedIcon != null
                    ? Icon(selectedIcon)
                    : null,
          );
        } else {
          return createControl(widget.control, destView.control.id, disabled,
              parentAdaptive: widget.parentAdaptive);
        }
      }).toList();
      return NavigationDrawer(
        elevation: widget.control.attrDouble("elevation"),
        indicatorColor: widget.control.attrColor("indicatorColor", context),
        indicatorShape: parseOutlinedBorder(widget.control, "indicatorShape"),
        backgroundColor: widget.control.attrColor("bgColor", context),
        selectedIndex: _selectedIndex,
        shadowColor: widget.control.attrColor("shadowColor", context),
        surfaceTintColor: widget.control.attrColor("surfaceTintColor", context),
        tilePadding: parseEdgeInsets(widget.control, "tilePadding") ??
            const EdgeInsets.symmetric(horizontal: 12.0),
        onDestinationSelected: _destinationChanged,
        children: children,
      );
    });

    return navDrawer;
  }
}
