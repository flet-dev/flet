import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class CupertinoNavigationBarControl extends StatefulWidget {
  final Control control;

  const CupertinoNavigationBarControl({super.key, required this.control});

  @override
  State<CupertinoNavigationBarControl> createState() =>
      _CupertinoNavigationBarControlState();
}

class _CupertinoNavigationBarControlState
    extends State<CupertinoNavigationBarControl> with FletStoreMixin {
  int _selectedIndex = 0;

  void _onTap(int index) {
    _selectedIndex = index;
    widget.control.updateProperties({"selected_index": _selectedIndex});
    widget.control.triggerEvent("change", _selectedIndex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoNavigationBarControl build: ${widget.control.id}");

    var selectedIndex = widget.control.getInt("selected_index", 0)!;
    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }
    var navBar = CupertinoTabBar(
        backgroundColor: widget.control.getColor("bgcolor", context),
        activeColor: widget.control.getColor("active_color", context) ??
            widget.control.getColor("indicator_color", context),
        // "indicator_color" from adaptive Material NavBar
        inactiveColor: widget.control
            .getColor("inactive_color", context, CupertinoColors.inactiveGray)!,
        iconSize: widget.control.getDouble("icon_size", 30.0)!,
        currentIndex: _selectedIndex,
        border: widget.control.getBorder("border", Theme.of(context)),
        onTap: widget.control.disabled ? null : _onTap,
        items: widget.control.children("destinations").map((dest) {
          var icon = parseIcon(dest.getString("icon"));
          var selectedIcon = parseIcon(dest.getString("selected_icon"));
          return BottomNavigationBarItem(
              tooltip: !dest.disabled ? dest.getString("tooltip") : null,
              backgroundColor: dest.getColor("bgcolor", context),
              icon: dest.buildWidget("icon") ?? Icon(icon),
              activeIcon: dest.buildWidget("selected_icon") ??
                  (selectedIcon != null ? Icon(selectedIcon) : null),
              label: dest.getString("label", "")!);
        }).toList());

    return ConstrainedControl(control: widget.control, child: navBar);
  }
}
