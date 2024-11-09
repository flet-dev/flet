import 'dart:convert';

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

  bool get disabled => widget.control.isDisabled || widget.parentDisabled;

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
          activeColor: widget.control.attrColor("activeColor", context) ??
              widget.control.attrColor("indicatorColor", context),
          inactiveColor: widget.control.attrColor("inactiveColor", context) ??
              CupertinoColors.inactiveGray,
          iconSize: widget.control.attrDouble("iconSize", 30.0)!,
          currentIndex: _selectedIndex,
          border: parseBorder(Theme.of(context), widget.control, "border"),
          onTap: disabled ? null : _onTap,
          items: viewModel.controlViews.map((destView) {
            var label = destView.control.attrString("label", "")!;
            var iconStr = parseIcon(destView.control.attrString("icon"));
            var iconCtrls =
                destView.children.where((c) => c.name == "icon" && c.isVisible);
            // if no control provided in "icon" property, replace iconCtrls with control provided in icon_content, if any
            // the line below needs to be deleted after icon_content is deprecated
            iconCtrls = iconCtrls.isEmpty
                ? destView.children
                    .where((c) => c.name == "icon_content" && c.isVisible)
                : iconCtrls;

            var selectedIconStr =
                parseIcon(destView.control.attrString("selectedIcon"));
            var selectedIconCtrls = destView.children
                .where((c) => c.name == "selected_icon" && c.isVisible);
            // if no control provided in "selected_icon" property, replace selectedIconCtrls with control provided in selected_icon_content, if any
            // the line below needs to be deleted after selected_icon_content is deprecated
            selectedIconCtrls = selectedIconCtrls.isEmpty
                ? destView.children.where(
                    (c) => c.name == "selected_icon_content" && c.isVisible)
                : selectedIconCtrls;

            var destinationDisabled = disabled || destView.control.isDisabled;
            var destinationTooltip = destView.control.attrString("tooltip");
            return BottomNavigationBarItem(
                tooltip: !destinationDisabled && destinationTooltip != null
                    ? jsonDecode(destinationTooltip)
                    : null,
                backgroundColor: widget.control.attrColor("bgColor", context),
                icon: iconCtrls.isNotEmpty
                    ? createControl(destView.control, iconCtrls.first.id,
                        destinationDisabled,
                        parentAdaptive: widget.parentAdaptive)
                    : Icon(iconStr),
                activeIcon: selectedIconCtrls.isNotEmpty
                    ? createControl(destView.control,
                        selectedIconCtrls.first.id, destinationDisabled,
                        parentAdaptive: widget.parentAdaptive)
                    : selectedIconStr != null
                        ? Icon(selectedIconStr)
                        : null,
                label: label);
          }).toList());
    });

    return constrainedControl(context, navBar, widget.parent, widget.control);
  }
}
