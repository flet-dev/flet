import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
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
      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
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
      var animationDuration = widget.control.attrInt("animationDuration");

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
            animationDuration: animationDuration != null
                ? Duration(milliseconds: animationDuration)
                : null,
            elevation: widget.control.attrDouble("elevation"),
            shadowColor: widget.control.attrColor("shadowColor", context),
            surfaceTintColor:
                widget.control.attrColor("surfaceTintColor", context),
            overlayColor: parseMaterialStateColor(
                Theme.of(context), widget.control, "overlayColor"),
            indicatorColor: widget.control.attrColor("indicatorColor", context),
            indicatorShape:
                parseOutlinedBorder(widget.control, "indicatorShape"),
            backgroundColor: widget.control.attrColor("bgColor", context),
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
                  enabled: !disabled || !destView.control.isDisabled,
                  tooltip: destView.control.attrString("tooltip", "")!,
                  icon: iconContentCtrls.isNotEmpty
                      ? createControl(
                          destView.control, iconContentCtrls.first.id, disabled,
                          parentAdaptive: adaptive)
                      : Icon(icon),
                  selectedIcon: selectedIconContentCtrls.isNotEmpty
                      ? createControl(destView.control,
                          selectedIconContentCtrls.first.id, disabled,
                          parentAdaptive: adaptive)
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
