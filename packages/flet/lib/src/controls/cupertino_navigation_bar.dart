import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class CupertinoNavigationBarControl extends StatefulWidget {
  final Control control;

  CupertinoNavigationBarControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoNavigationBarControl> createState() =>
      _CupertinoNavigationBarControlState();
}

class _CupertinoNavigationBarControlState
    extends State<CupertinoNavigationBarControl> with FletStoreMixin {
  int _selectedIndex = 0;

  void _onTap(int index) {
    _selectedIndex = index;
    widget.control
        .updateProperties({"selected_index": _selectedIndex}, notify: true);
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
        // "indicator_color" from adaptive Material NavBar
        activeColor: widget.control.getColor("active_color", context) ??
            widget.control.getColor("indicator_color", context),
        inactiveColor: widget.control
            .getColor("inactive_color", context, CupertinoColors.inactiveGray)!,
        iconSize: widget.control.getDouble("icon_size", 30.0)!,
        currentIndex: _selectedIndex,
        border: widget.control.getBorder("border", Theme.of(context)),
        onTap: widget.control.disabled ? null : _onTap,
        items: widget.control.children("destinations").map((dest) {
          return BottomNavigationBarItem(
              tooltip: !dest.disabled ? dest.getString("tooltip") : null,
              backgroundColor: dest.getColor("bgcolor", context),
              icon: dest.buildIconOrWidget("icon")!,
              activeIcon: dest.buildIconOrWidget("selected_icon"),
              label: dest.getString("label", "")!);
        }).toList());

    return ConstrainedControl(control: widget.control, child: navBar);
  }
}
