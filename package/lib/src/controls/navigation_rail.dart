import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'error.dart';

class NavigationRailControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const NavigationRailControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<NavigationRailControl> createState() => _NavigationRailControlState();
}

class _NavigationRailControlState extends State<NavigationRailControl> {
  int? _selectedIndex;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    List<Map<String, String>> props = [
      {"i": widget.control.id, "selectedindex": _selectedIndex.toString()}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: "change",
        eventData: _selectedIndex.toString());
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

    var rail = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
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
                  labelType:
                      extended ? NavigationRailLabelType.none : labelType,
                  extended: extended,
                  elevation: widget.control.attrDouble("elevation", 0),
                  indicatorShape: parseOutlinedBorder(widget.control, "indicatorShape"),
                  minWidth: widget.control.attrDouble("minWidth"),
                  minExtendedWidth:
                      widget.control.attrDouble("minExtendedWidth"),
                  groupAlignment: widget.control.attrDouble("groupAlignment"),
                  backgroundColor: HexColor.fromString(Theme.of(context),
                      widget.control.attrString("bgColor", "")!),
                  indicatorColor: HexColor.fromString(Theme.of(context),
                      widget.control.attrString("indicatorColor", "")!),
                  leading: leadingCtrls.isNotEmpty
                      ? createControl(
                          widget.control, leadingCtrls.first.id, disabled)
                      : null,
                  trailing: trailingCtrls.isNotEmpty
                      ? createControl(
                          widget.control, trailingCtrls.first.id, disabled)
                      : null,
                  selectedIndex: _selectedIndex,
                  onDestinationSelected: _destinationChanged,
                  destinations: viewModel.controlViews.map((destView) {
                    var label = destView.control.attrString("label", "")!;
                    var labelContentCtrls = destView.children
                        .where((c) => c.name == "label_content");

                    var icon = getMaterialIcon(
                        destView.control.attrString("icon", "")!);
                    var iconContentCtrls = destView.children
                        .where((c) => c.name == "icon_content");

                    var selectedIcon = getMaterialIcon(
                        destView.control.attrString("selectedIcon", "")!);
                    var selectedIconContentCtrls = destView.children
                        .where((c) => c.name == "selected_icon_content");

                    return NavigationRailDestination(
                        padding: parseEdgeInsets(destView.control, "padding"),
                        icon: iconContentCtrls.isNotEmpty
                            ? createControl(destView.control,
                                iconContentCtrls.first.id, disabled)
                            : Icon(icon),
                        selectedIcon: selectedIconContentCtrls.isNotEmpty
                            ? createControl(destView.control,
                                selectedIconContentCtrls.first.id, disabled)
                            : selectedIcon != null
                                ? Icon(selectedIcon)
                                : null,
                        label: labelContentCtrls.isNotEmpty
                            ? createControl(destView.control,
                                labelContentCtrls.first.id, disabled)
                            : Text(label));
                  }).toList());
            },
          );
        });

    return constrainedControl(context, rail, widget.parent, widget.control);
  }
}
