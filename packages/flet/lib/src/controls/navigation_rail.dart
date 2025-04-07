import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';

class NavigationRailControl extends StatefulWidget {
  final Control control;

  const NavigationRailControl({super.key, required this.control});

  @override
  State<NavigationRailControl> createState() => _NavigationRailControlState();
}

class _NavigationRailControlState extends State<NavigationRailControl>
    with FletStoreMixin {
  int? _selectedIndex;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("NavigationRail selected_index: $_selectedIndex");
    FletBackend.of(context)
        .updateControl(widget.control.id, {"selected_index": _selectedIndex});
    FletBackend.of(context)
        .triggerControlEvent(widget.control, "change", _selectedIndex);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationRailControl build: ${widget.control.id}");

    bool disabled = widget.control.disabled;
    var selectedIndex = widget.control.getInt("selected_index");

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var labelType = parseNavigationRailLabelType(
        widget.control.getString("label_type"), NavigationRailLabelType.all)!;

    var extended = widget.control.getBool("extended", false)!;

    var rail = LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) {
        debugPrint(
            "NavigationRail constraints.maxWidth: ${constraints.maxWidth}");
        debugPrint(
            "NavigationRail constraints.maxHeight: ${constraints.maxHeight}");

        if (constraints.maxHeight == double.infinity &&
            widget.control.getDouble("height") == null) {
          return const ErrorControl("Error displaying NavigationRail",
              description:
                  "Control's height is unbounded. Either set \"expand\" property, set a fixed \"height\" or nest NavigationRail inside another control with a fixed height.");
        }

        return NavigationRail(
          labelType: extended ? NavigationRailLabelType.none : labelType,
          extended: extended,
          elevation: widget.control.getDouble("elevation"),
          selectedLabelTextStyle: parseTextStyle(
              widget.control.get("selected_label_text_style"),
              Theme.of(context)),
          unselectedLabelTextStyle: parseTextStyle(
              widget.control.get("unselected_label_text_style"),
              Theme.of(context)),
          indicatorShape: widget.control.getOutlinedBorder("indicator_shape"),
          minWidth: widget.control.getDouble("min_width"),
          minExtendedWidth: widget.control.getDouble("min_extended_width"),
          groupAlignment: widget.control.getDouble("group_alignment"),
          backgroundColor: widget.control.getColor("bgcolor", context),
          indicatorColor: widget.control.getColor("indicator_color", context),
          leading: widget.control.buildWidget("leading"),
          trailing: widget.control.buildWidget("trailing"),
          selectedIndex: _selectedIndex,
          onDestinationSelected: _destinationChanged,
          destinations:
              widget.control.children("destinations").map((destinationControl) {
            destinationControl.notifyParent = true;
            var label = destinationControl.getString("label", "")!;
            var icon = destinationControl.buildWidget("icon") ??
                Icon(parseIcon(destinationControl.getString("icon")));
            var selectedIcon = destinationControl
                    .buildWidget("selected_icon") ??
                Icon(parseIcon(destinationControl.getString("selected_icon")));
            return NavigationRailDestination(
              disabled: disabled || destinationControl.disabled,
              padding: parseEdgeInsets(destinationControl.get("padding")),
              indicatorColor:
                  destinationControl.getColor("indicator_color", context),
              indicatorShape: parseOutlinedBorder(
                  destinationControl.get("indicator_shape")),
              icon: icon,
              selectedIcon: selectedIcon,
              label: destinationControl.buildWidget("label") ??
                  destinationControl
                      .buildWidget("label_content") ?? // todo(0.70.3): remove
                  Text(label),
            );
          }).toList(),
        );
      },
    );

    return ConstrainedControl(control: widget.control, child: rail);
  }
}
