import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'cupertino_navigation_bar.dart';
import 'flet_control_state.dart';

class NavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const NavigationBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<NavigationBarControl> createState() => _NavigationBarControlState();
}

class _NavigationBarControlState extends State<NavigationBarControl>
    with FletControlState {
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
    debugPrint("NavigationBarControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool adaptive = widget.control.attrBool("adaptive", false)!;
      if (adaptive &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoNavigationBarControl(
            control: widget.control,
            children: widget.children,
            parentDisabled: widget.parentDisabled);
      }

      bool disabled = widget.control.isDisabled || widget.parentDisabled;
      var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

      if (_selectedIndex != selectedIndex) {
        _selectedIndex = selectedIndex;
      }

      NavigationDestinationLabelBehavior? labelBehavior =
          NavigationDestinationLabelBehavior.values.firstWhereOrNull((a) =>
              a.name.toLowerCase() ==
              widget.control.attrString("labelBehavior", "")!.toLowerCase());

      var navBar = withControls(
          widget.children
              .where((c) => c.isVisible && c.name == null)
              .map((c) => c.id), (content, viewModel) {
        return NavigationBar(
            labelBehavior: labelBehavior,
            height: widget.control.attrDouble("height"),
            elevation: widget.control.attrDouble("elevation"),
            shadowColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("shadowColor", "")!),
            surfaceTintColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("surfaceTintColor", "")!),
            indicatorColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("indicatorColor", "")!),
            indicatorShape:
                parseOutlinedBorder(widget.control, "indicatorShape"),
            backgroundColor: HexColor.fromString(
                Theme.of(context), widget.control.attrString("bgColor", "")!),
            selectedIndex: _selectedIndex,
            onDestinationSelected: _destinationChanged,
            destinations: viewModel.controlViews.map((destView) {
              var label = destView.control.attrString("label", "")!;

              var icon = parseIcon(destView.control.attrString("icon", "")!);
              var iconContentCtrls =
                  destView.children.where((c) => c.name == "icon_content");

              var selectedIcon =
                  parseIcon(destView.control.attrString("selectedIcon", "")!);
              var selectedIconContentCtrls = destView.children
                  .where((c) => c.name == "selected_icon_content");

              return NavigationDestination(
                  tooltip: destView.control.attrString("tooltip", "")!,
                  icon: iconContentCtrls.isNotEmpty
                      ? createControl(
                          destView.control, iconContentCtrls.first.id, disabled)
                      : Icon(icon),
                  selectedIcon: selectedIconContentCtrls.isNotEmpty
                      ? createControl(destView.control,
                          selectedIconContentCtrls.first.id, disabled)
                      : selectedIcon != null
                          ? Icon(selectedIcon)
                          : null,
                  label: label);
            }).toList());
      });

      return constrainedControl(context, navBar, widget.parent, widget.control);
    });
  }
}
