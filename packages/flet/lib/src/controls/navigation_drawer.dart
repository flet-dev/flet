import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';
import '../widgets/scaffold_key_provider.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class NavigationDrawerControl extends StatefulWidget {
  final Control control;

  const NavigationDrawerControl({super.key, required this.control});

  @override
  State<NavigationDrawerControl> createState() =>
      _NavigationDrawerControlState();
}

class _NavigationDrawerControlState extends State<NavigationDrawerControl> {
  int _selectedIndex = 0;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.control
        .updateProperties({"selected_index": _selectedIndex}, notify: true);
    widget.control.triggerEvent("change", _selectedIndex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationDrawerControl build: ${widget.control.id}");

    var selectedIndex = widget.control.getInt("selected_index", 0)!;
    var endDrawer = widget.control.get("position") == "end";

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var drawer = NavigationDrawer(
      elevation: widget.control.getDouble("elevation"),
      indicatorColor: widget.control.getColor("indicator_color", context),
      indicatorShape: widget.control
          .getOutlinedBorder("indicator_shape", Theme.of(context)),
      backgroundColor: widget.control.getColor("bgcolor", context),
      selectedIndex: _selectedIndex,
      shadowColor: widget.control.getColor("shadow_color", context),
      surfaceTintColor: widget.control.getColor("surface_tint_color", context),
      tilePadding: parseEdgeInsets(widget.control.get("tile_padding"),
          const EdgeInsets.symmetric(horizontal: 12.0))!,
      onDestinationSelected: _destinationChanged,
      children: widget.control.children("controls").map((dest) {
        dest.notifyParent = true;
        if (dest.type == "NavigationDrawerDestination") {
          var icon = dest.get("icon");
          var selectedIcon = dest.get("selected_icon");

          return NavigationDrawerDestination(
            enabled: !dest.disabled,
            backgroundColor: dest.getColor("bgcolor", context),
            icon: icon is Control
                ? ControlWidget(
                    control: icon,
                  )
                : Icon(parseIcon(icon)),
            label: Text(dest.getString("label", "")!),
            selectedIcon: selectedIcon is Control
                ? ControlWidget(
                    control: selectedIcon,
                  )
                : selectedIcon is String
                    ? Icon(parseIcon(selectedIcon))
                    : null,
          );
        } else {
          return ControlWidget(control: dest);
        }
      }).toList(),
    );

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.control.getBool("open", false) == false) {
        if (endDrawer &&
            ScaffoldKeyProvider.of(context)?.currentState?.isEndDrawerOpen ==
                true) {
          ScaffoldKeyProvider.of(context)?.currentState?.closeEndDrawer();
        } else if (ScaffoldKeyProvider.of(context)
                ?.currentState
                ?.isDrawerOpen ==
            true) {
          ScaffoldKeyProvider.of(context)?.currentState?.closeDrawer();
        }
      }
    });

    return BaseControl(control: widget.control, child: drawer);
  }
}
