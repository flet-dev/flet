import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';

class NavigationDrawerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const NavigationDrawerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<NavigationDrawerControl> createState() =>
      _NavigationDrawerControlState();
}

class _NavigationDrawerControlState extends State<NavigationDrawerControl> {
  int _selectedIndex = 0;

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
    debugPrint("NavigationDrawerControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var navDrawer = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
          List<Widget> children = viewModel.controlViews.map((destView) {
            if (destView.control.type == "navigationdrawerdestination") {
              var icon =
                  getMaterialIcon(destView.control.attrString("icon", "")!);
              var iconContentCtrls =
                  destView.children.where((c) => c.name == "icon_content");
              var selectedIcon = getMaterialIcon(
                  destView.control.attrString("selectedIcon", "")!);
              var selectedIconContentCtrls = destView.children
                  .where((c) => c.name == "selected_icon_content");
              return NavigationDrawerDestination(
                // backgroundColor: HexColor.fromString(Theme.of(context),
                //     destView.control.attrString("bgColor", "")!),
                // flutter issue https://github.com/flutter/flutter/issues/138105
                icon: iconContentCtrls.isNotEmpty
                    ? createControl(
                        destView.control, iconContentCtrls.first.id, disabled)
                    : Icon(icon),
                label: Text(destView.control.attrString("label", "")!),
                selectedIcon: selectedIconContentCtrls.isNotEmpty
                    ? createControl(destView.control,
                        selectedIconContentCtrls.first.id, disabled)
                    : selectedIcon != null
                        ? Icon(selectedIcon)
                        : null,
              );
            } else {
              return createControl(
                  widget.control, destView.control.id, disabled);
            }
          }).toList();
          return NavigationDrawer(
            elevation: widget.control.attrDouble("elevation"),
            indicatorColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("indicatorColor", "")!),
            indicatorShape:
                parseOutlinedBorder(widget.control, "indicatorShape"),
            backgroundColor: HexColor.fromString(
                Theme.of(context), widget.control.attrString("bgColor", "")!),
            selectedIndex: _selectedIndex,
            shadowColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("shadowColor", "")!),
            surfaceTintColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("surfaceTintColor", "")!),
            tilePadding: parseEdgeInsets(widget.control, "tilePadding") ??
                const EdgeInsets.symmetric(horizontal: 12.0),
            onDestinationSelected: _destinationChanged,
            children: children,
          );
        });

    return navDrawer;
  }
}
