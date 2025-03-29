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
    debugPrint("NavigationRail selectedIndex: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationRailControl build: ${widget.control.id}");

    bool disabled = widget.control.disabled || widget.parentDisabled;
    var selectedIndex = widget.control.getInt("selectedIndex");

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    NavigationRailLabelType? labelType = NavigationRailLabelType.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control.getString("labelType", "")!.toLowerCase(),
            orElse: () => NavigationRailLabelType.all);

    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.visible);
    var trailingCtrls =
        widget.children.where((c) => c.name == "trailing" && c.visible);

    var extended = widget.control.getBool("extended", false)!;

    var rail = withControls(
        widget.children
            .where((c) => c.visible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return LayoutBuilder(
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
                  Theme.of(context), widget.control, "selectedLabelTextStyle"),
              unselectedLabelTextStyle: parseTextStyle(Theme.of(context),
                  widget.control, "unselectedLabelTextStyle"),
              indicatorShape:
                  parseOutlinedBorder(widget.control, "indicatorShape"),
              minWidth: widget.control.getDouble("minWidth"),
              minExtendedWidth: widget.control.getDouble("minExtendedWidth"),
              groupAlignment: widget.control.getDouble("groupAlignment"),
              backgroundColor: widget.control.getColor("bgColor", context),
              indicatorColor:
                  widget.control.getColor("indicatorColor", context),
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
                var label = destView.control.getString("label", "")!;
                var labelContentCtrls = destView.children
                    .where((c) => c.name == "label_content" && c.visible);

                var iconStr = parseIcon(destView.control.getString("icon"));
                var iconCtrls = destView.children
                    .where((c) => c.name == "icon" && c.visible);
                // if no control provided in "icon" property, replace iconCtrls with control provided in icon_content, if any
                // the line below needs to be deleted after icon_content is deprecated
                iconCtrls = iconCtrls.isEmpty
                    ? destView.children
                        .where((c) => c.name == "icon_content" && c.visible)
                    : iconCtrls;

                var selectedIconStr =
                    parseIcon(destView.control.getString("selectedIcon"));
                var selectedIconCtrls = destView.children
                    .where((c) => c.name == "selected_icon" && c.visible);
                // if no control provided in "selected_icon" property, replace selectedIconCtrls with control provided in selected_icon_content, if any
                // the line below needs to be deleted after selected_icon_content is deprecated
                selectedIconCtrls = selectedIconCtrls.isEmpty
                    ? destView.children.where(
                        (c) => c.name == "selected_icon_content" && c.visible)
                    : selectedIconCtrls;

                return NavigationRailDestination(
                    disabled: disabled || destView.control.disabled,
                    padding: parseEdgeInsets(destView.control, "padding"),
                    indicatorColor:
                        destView.control.getColor("indicatorColor", context),
                    indicatorShape:
                        parseOutlinedBorder(destView.control, "indicatorShape"),
                    icon: iconCtrls.isNotEmpty
                        ? createControl(
                            destView.control, iconCtrls.first.id, disabled,
                            parentAdaptive: widget.parentAdaptive)
                        : Icon(iconStr),
                    selectedIcon: selectedIconCtrls.isNotEmpty
                        ? createControl(destView.control,
                            selectedIconCtrls.first.id, disabled,
                            parentAdaptive: widget.parentAdaptive)
                        : selectedIconStr != null
                            ? Icon(selectedIconStr)
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
