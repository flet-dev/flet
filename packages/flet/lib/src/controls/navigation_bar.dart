import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/others.dart';
import '../utils/time.dart';
import 'create_control.dart';
import 'cupertino_navigation_bar.dart';
import 'flet_store_mixin.dart';

class NavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const NavigationBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<NavigationBarControl> createState() => _NavigationBarControlState();
}

class _NavigationBarControlState extends State<NavigationBarControl>
    with FletStoreMixin {
  int _selectedIndex = 0;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedIndex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationBarControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive = widget.control.isAdaptive ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoNavigationBarControl(
            control: widget.control,
            children: widget.children,
            parentDisabled: widget.parentDisabled,
            parentAdaptive: adaptive,
            backend: widget.backend);
      }

      bool disabled = widget.control.isDisabled || widget.parentDisabled;
      var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

      if (_selectedIndex != selectedIndex) {
        _selectedIndex = selectedIndex;
      }
      var navBar = withControls(
          widget.children
              .where((c) => c.isVisible && c.name == null)
              .map((c) => c.id), (content, viewModel) {
        return NavigationBar(
            labelBehavior: parseNavigationDestinationLabelBehavior(
                widget.control.attrString("labelBehavior")),
            height: widget.control.attrDouble("height"),
            animationDuration:
                parseDuration(widget.control, "animationDuration"),
            elevation: widget.control.attrDouble("elevation"),
            shadowColor: widget.control.attrColor("shadowColor", context),
            surfaceTintColor:
                widget.control.attrColor("surfaceTintColor", context),
            overlayColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "overlayColor"),
            indicatorColor: widget.control.attrColor("indicatorColor", context),
            indicatorShape:
                parseOutlinedBorder(widget.control, "indicatorShape"),
            backgroundColor: widget.control.attrColor("bgColor", context),
            selectedIndex: _selectedIndex,
            onDestinationSelected: disabled ? null : _destinationChanged,
            destinations: viewModel.controlViews.map((destView) {
              var label = destView.control.attrString("label", "")!;
              var iconStr = parseIcon(destView.control.attrString("icon"));
              var iconCtrls = destView.children
                  .where((c) => c.name == "icon" && c.isVisible);
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
              var destinationAdaptive = destView.control.isAdaptive ?? adaptive;
              var destinationTooltip = destView.control.attrString("tooltip");
              return NavigationDestination(
                  enabled: !destinationDisabled,
                  tooltip: !destinationDisabled && destinationTooltip != null
                      ? jsonDecode(destinationTooltip)
                      : null,
                  icon: iconCtrls.isNotEmpty
                      ? createControl(destView.control, iconCtrls.first.id,
                          destinationDisabled,
                          parentAdaptive: destinationAdaptive)
                      : Icon(iconStr),
                  selectedIcon: selectedIconCtrls.isNotEmpty
                      ? createControl(destView.control,
                          selectedIconCtrls.first.id, destinationDisabled,
                          parentAdaptive: destinationAdaptive)
                      : selectedIconStr != null
                          ? Icon(selectedIconStr)
                          : null,
                  label: label);
            }).toList());
      });

      return constrainedControl(context, navBar, widget.parent, widget.control);
    });
  }
}
