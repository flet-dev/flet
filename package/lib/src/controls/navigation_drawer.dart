import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'flet_control_stateful_mixin.dart';

class NavigationDrawerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const NavigationDrawerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<NavigationDrawerControl> createState() =>
      _NavigationDrawerControlState();
}

class _NavigationDrawerControlState extends State<NavigationDrawerControl>
    with FletControlStatefulMixin {
  int _selectedIndex = 0;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    updateControlProps(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    sendControlEvent(widget.control.id, "change", _selectedIndex.toString());
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
            // backgroundColor: HexColor.fromString(Theme.of(context),
            //     destView.control.attrString("bgColor", "")!),
            // flutter issue https://github.com/flutter/flutter/issues/138105
            icon: iconContentCtrls.isNotEmpty
                ? createControl(
                    destView.control, iconContentCtrls.first.id, disabled)
                : Icon(icon),
            label: Text(destView.control.attrString("label", "")!),
            selectedIcon: selectedIconContentCtrls.isNotEmpty
                ? createControl(destView.control,
                    selectedIconContentCtrls.first.id, disabled)
                : selectedIcon != null
                    ? Icon(selectedIcon)
                    : null,
          );
        } else {
          return createControl(widget.control, destView.control.id, disabled);
        }
      }).toList();
      return NavigationDrawer(
        elevation: widget.control.attrDouble("elevation"),
        indicatorColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("indicatorColor", "")!),
        indicatorShape: parseOutlinedBorder(widget.control, "indicatorShape"),
        backgroundColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("bgColor", "")!),
        selectedIndex: _selectedIndex,
        shadowColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("shadowColor", "")!),
        surfaceTintColor: HexColor.fromString(Theme.of(context),
            widget.control.attrString("surfaceTintColor", "")!),
        tilePadding: parseEdgeInsets(widget.control, "tilePadding") ??
            const EdgeInsets.symmetric(horizontal: 12.0),
        onDestinationSelected: _destinationChanged,
        children: children,
      );
    });

    return navDrawer;
  }
}
