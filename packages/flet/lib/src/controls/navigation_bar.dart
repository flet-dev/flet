import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/misc.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/time.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'cupertino_navigation_bar.dart';

class NavigationBarControl extends StatefulWidget {
  final Control control;

  const NavigationBarControl({super.key, required this.control});

  @override
  State<NavigationBarControl> createState() => _NavigationBarControlState();
}

class _NavigationBarControlState extends State<NavigationBarControl>
    with FletStoreMixin {
  int _selectedIndex = 0;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    widget.control.updateProperties({"selectedIndex": _selectedIndex});
    widget.control.triggerEvent("change", _selectedIndex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationBarControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      if (widget.control.adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoNavigationBarControl(control: widget.control);
      }

      var selectedIndex = widget.control.getInt("selected_index", 0)!;

      if (_selectedIndex != selectedIndex) {
        _selectedIndex = selectedIndex;
      }
      var navBar = NavigationBar(
          labelBehavior: widget.control
              .getNavigationDestinationLabelBehavior("label_behavior"),
          height: widget.control.getDouble("height"),
          animationDuration: widget.control.getDuration("animation_duration"),
          elevation: widget.control.getDouble("elevation"),
          labelPadding: widget.control.getPadding("label_padding"),
          shadowColor: widget.control.getColor("shadow_color", context),
          surfaceTintColor:
              widget.control.getColor("surface_tint_color", context),
          overlayColor: widget.control
              .getWidgetStateColor("overlay_color", Theme.of(context)),
          indicatorColor: widget.control.getColor("indicator_color", context),
          indicatorShape: widget.control.getShape("indicator_shape"),
          backgroundColor: widget.control.getColor("bgcolor", context),
          selectedIndex: _selectedIndex,
          onDestinationSelected:
              widget.control.disabled ? null : _destinationChanged,
          destinations: widget.control.children("controls").map((dest) {
            var icon = parseIcon(dest.getString("icon"));
            var selectedIcon = parseIcon(dest.getString("selected_icon"));
            return NavigationDestination(
                enabled: !dest.disabled,
                tooltip: !dest.disabled ? dest.getString("tooltip") : null,
                icon: dest.buildWidget("icon") ?? Icon(icon),
                selectedIcon: dest.buildWidget("selected_icon") ??
                    (selectedIcon != null ? Icon(selectedIcon) : null),
                label: dest.getString("label", "")!);
          }).toList());

      return ConstrainedControl(control: widget.control, child: navBar);
    });
  }
}
