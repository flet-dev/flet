import 'package:flet_view/utils/icons.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

class NavigationRailControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const NavigationRailControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<NavigationRailControl> createState() => _NavigationRailControlState();
}

class _NavigationRailControlState extends State<NavigationRailControl> {
  int? _selectedIndex;
  dynamic _dispatch;

  @override
  void initState() {
    super.initState();
  }

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    List<Map<String, String>> props = [
      {"i": widget.control.id, "selectedindex": _selectedIndex.toString()}
    ];
    _dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    ws.updateControlProps(props: props);
    ws.pageEventFromWeb(
        eventTarget: widget.control.id,
        eventName: "change",
        eventData: _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("NavigationRailControl build: ${widget.control.id}");

    var selectedIndex = widget.control.attrInt("selectedIndex");

    debugPrint(selectedIndex.toString());

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    NavigationRailLabelType? labelType = NavigationRailLabelType.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control.attrString("labelType", "")!.toLowerCase(),
            orElse: () => NavigationRailLabelType.all);

    var leadingCtrls = widget.children.where((c) => c.name == "leading");
    var trailingCtrls = widget.children.where((c) => c.name == "trailing");

    var extended = widget.control.attrBool("extended", false)!;

    var rail = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
          _dispatch = viewModel.dispatch;

          return NavigationRail(
              labelType: extended ? NavigationRailLabelType.none : labelType,
              extended: extended,
              minWidth: widget.control.attrDouble("minWidth"),
              minExtendedWidth: widget.control.attrDouble("minExtendedWidth"),
              groupAlignment: widget.control.attrDouble("groupAlignment"),
              backgroundColor: HexColor.fromString(
                  Theme.of(context), widget.control.attrString("bgColor", "")!),
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
                var labelContentCtrls =
                    destView.children.where((c) => c.name == "label_content");

                var icon =
                    getMaterialIcon(destView.control.attrString("icon", "")!);
                var iconContentCtrls =
                    destView.children.where((c) => c.name == "icon_content");

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
        });

    return constrainedControl(rail, widget.parent, widget.control);
  }
}
