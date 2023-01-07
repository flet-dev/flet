import 'package:collection/collection.dart';
import 'package:flet/src/controls/error.dart';
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

class NavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const NavigationBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<NavigationBarControl> createState() => _NavigationBarControlState();
}

class _NavigationBarControlState extends State<NavigationBarControl> {
  int _selectedIndex = 0;
  dynamic _dispatch;

  void _destinationChanged(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    List<Map<String, String>> props = [
      {"i": widget.control.id, "selectedindex": _selectedIndex.toString()}
    ];
    _dispatch(
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
    debugPrint("NavigationBarControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    NavigationDestinationLabelBehavior? labelBehavior =
        NavigationDestinationLabelBehavior.values.firstWhereOrNull((a) =>
            a.name.toLowerCase() ==
            widget.control.attrString("labelBehavior", "")!.toLowerCase());

    var navBar = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
          _dispatch = viewModel.dispatch;

          return NavigationBar(
              labelBehavior: labelBehavior,
              height: widget.control.attrDouble("height"),
              elevation: widget.control.attrDouble("elevation"),
              backgroundColor: HexColor.fromString(
                  Theme.of(context), widget.control.attrString("bgColor", "")!),
              selectedIndex: _selectedIndex,
              onDestinationSelected: _destinationChanged,
              destinations: viewModel.controlViews.map((destView) {
                var label = destView.control.attrString("label", "")!;

                var icon =
                    getMaterialIcon(destView.control.attrString("icon", "")!);
                var iconContentCtrls =
                    destView.children.where((c) => c.name == "icon_content");

                var selectedIcon = getMaterialIcon(
                    destView.control.attrString("selectedIcon", "")!);
                var selectedIconContentCtrls = destView.children
                    .where((c) => c.name == "selected_icon_content");

                return NavigationDestination(
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
                    label: label);
              }).toList());
        });

    return constrainedControl(context, navBar, widget.parent, widget.control);
  }
}
