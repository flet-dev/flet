import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

class CupertinoNavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoNavigationBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoNavigationBarControl> createState() =>
      _CupertinoNavigationBarControlState();
}

class _CupertinoNavigationBarControlState
    extends State<CupertinoNavigationBarControl> with FletStoreMixin {
  int _selectedIndex = 0;

  void _onTap(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoNavigationBarControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var navBar = withControls(
        widget.children
            .where((c) => c.isVisible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return CupertinoTabBar(
          backgroundColor: widget.control.attrColor("bgColor", context),
          activeColor: widget.control.attrColor("activeColor", context),
          inactiveColor: widget.control.attrColor("inactiveColor", context) ??
              CupertinoColors.inactiveGray,
          iconSize: widget.control.attrDouble("iconSize", 30.0)!,
          currentIndex: _selectedIndex,
          border: parseBorder(Theme.of(context), widget.control, "border"),
          onTap: _onTap,
          items: viewModel.controlViews.map((destView) {
            var label = destView.control.attrString("label", "")!;

            var icon = parseIcon(destView.control.attrString("icon", "")!);
            var iconContentCtrls =
                destView.children.where((c) => c.name == "icon_content");

            var selectedIcon =
                parseIcon(destView.control.attrString("selectedIcon", "")!);
            var selectedIconContentCtrls = destView.children
                .where((c) => c.name == "selected_icon_content");

            return BottomNavigationBarItem(
                tooltip: destView.control.attrString("tooltip", "")!,
                backgroundColor: widget.control.attrColor("bgColor", context),
                icon: iconContentCtrls.isNotEmpty
                    ? createControl(
                        destView.control, iconContentCtrls.first.id, disabled,
                        parentAdaptive: widget.parentAdaptive)
                    : Icon(icon),
                activeIcon: selectedIconContentCtrls.isNotEmpty
                    ? createControl(destView.control,
                        selectedIconContentCtrls.first.id, disabled,
                        parentAdaptive: widget.parentAdaptive)
                    : selectedIcon != null
                        ? Icon(selectedIcon)
                        : null,
                label: label);
          }).toList());
    });

    return constrainedControl(context, navBar, widget.parent, widget.control);
  }
}
