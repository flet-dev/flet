import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_store_mixin.dart';

class NavigationRailControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const NavigationRailControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<NavigationRailControl> createState() => _NavigationRailControlState();
}

class _NavigationRailControlState extends State<NavigationRailControl>
    with FletStoreMixin {
  int? _selectedIndex;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationRailControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex");

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    NavigationRailLabelType? labelType = NavigationRailLabelType.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control.attrString("labelType", "")!.toLowerCase(),
            orElse: () => NavigationRailLabelType.all);

    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var trailingCtrls =
        widget.children.where((c) => c.name == "trailing" && c.isVisible);

    var extended = widget.control.attrBool("extended", false)!;

    var rail = withControls(
        widget.children
            .where((c) => c.isVisible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          debugPrint(
              "NavigationRail constraints.maxWidth: ${constraints.maxWidth}");
          debugPrint(
              "NavigationRail constraints.maxHeight: ${constraints.maxHeight}");

          if (constraints.maxHeight == double.infinity &&
              widget.control.attrs["height"] == null) {
            return const ErrorControl("Error displaying NavigationRail",
                description:
                    "Control's height is unbounded. Either set \"expand\" property, set a fixed \"height\" or nest NavigationRail inside another control with a fixed height.");
          }

          return NavigationRail(
              labelType: extended ? NavigationRailLabelType.none : labelType,
              extended: extended,
              elevation: widget.control.attrDouble("elevation", 0),
              selectedLabelTextStyle: parseTextStyle(
                  Theme.of(context), widget.control, "selectedLabelTextStyle"),
              unselectedLabelTextStyle: parseTextStyle(Theme.of(context),
                  widget.control, "unselectedLabelTextStyle"),
              indicatorShape:
                  parseOutlinedBorder(widget.control, "indicatorShape"),
              minWidth: widget.control.attrDouble("minWidth"),
              minExtendedWidth: widget.control.attrDouble("minExtendedWidth"),
              groupAlignment: widget.control.attrDouble("groupAlignment"),
              backgroundColor: widget.control.attrColor("bgColor", context),
              indicatorColor:
                  widget.control.attrColor("indicatorColor", context),
              leading: leadingCtrls.isNotEmpty
                  ? createControl(
                      widget.control, leadingCtrls.first.id, disabled,
                      parentAdaptive: widget.parentAdaptive)
                  : null,
              trailing: trailingCtrls.isNotEmpty
                  ? createControl(
                      widget.control, trailingCtrls.first.id, disabled,
                      parentAdaptive: widget.parentAdaptive)
                  : null,
              selectedIndex: _selectedIndex,
              onDestinationSelected: _destinationChanged,
              destinations: viewModel.controlViews.map((destView) {
                var label = destView.control.attrString("label", "")!;
                var labelContentCtrls =
                    destView.children.where((c) => c.name == "label_content");

                var icon = parseIcon(destView.control.attrString("icon", "")!);
                var iconContentCtrls =
                    destView.children.where((c) => c.name == "icon_content");

                var selectedIcon =
                    parseIcon(destView.control.attrString("selectedIcon", "")!);
                var selectedIconContentCtrls = destView.children
                    .where((c) => c.name == "selected_icon_content");

                return NavigationRailDestination(
                    disabled: disabled || destView.control.isDisabled,
                    padding: parseEdgeInsets(destView.control, "padding"),
                    indicatorColor:
                        destView.control.attrColor("indicatorColor", context),
                    indicatorShape:
                        parseOutlinedBorder(destView.control, "indicatorShape"),
                    icon: iconContentCtrls.isNotEmpty
                        ? createControl(destView.control,
                            iconContentCtrls.first.id, disabled,
                            parentAdaptive: widget.parentAdaptive)
                        : Icon(icon),
                    selectedIcon: selectedIconContentCtrls.isNotEmpty
                        ? createControl(destView.control,
                            selectedIconContentCtrls.first.id, disabled,
                            parentAdaptive: widget.parentAdaptive)
                        : selectedIcon != null
                            ? Icon(selectedIcon)
                            : null,
                    label: labelContentCtrls.isNotEmpty
                        ? createControl(destView.control,
                            labelContentCtrls.first.id, disabled,
                            parentAdaptive: widget.parentAdaptive)
                        : Text(label));
              }).toList());
        },
      );
    });

    return constrainedControl(context, rail, widget.parent, widget.control);
  }
}
