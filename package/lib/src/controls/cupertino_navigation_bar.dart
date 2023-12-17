import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
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

class CupertinoNavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const CupertinoNavigationBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<CupertinoNavigationBarControl> createState() =>
      _CupertinoNavigationBarControlState();
}

class _CupertinoNavigationBarControlState
    extends State<CupertinoNavigationBarControl> {
  int _selectedIndex = 0;

  void _onTap(int index) {
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
    debugPrint("CupertinoNavigationBarControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var navBar = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
          return CupertinoTabBar(
              backgroundColor: HexColor.fromString(
                  Theme.of(context), widget.control.attrString("bgColor", "")!),
              activeColor: HexColor.fromString(
                  Theme.of(context), widget.control.attrString("activeColor", "")!),
              inactiveColor: HexColor.fromString(Theme.of(context),
                  widget.control.attrString("inactiveColor", "")!)!,
              iconSize: widget.control.attrDouble("iconSize", 30.0)!,
              currentIndex: _selectedIndex,
              border: parseBorder(Theme.of(context), widget.control, "border"),
              onTap: _onTap,
              items: viewModel.controlViews.map((destView) {
                var label = destView.control.attrString("label", "")!;

                var icon =
                    getMaterialIcon(destView.control.attrString("icon", "")!);
                var iconContentCtrls =
                    destView.children.where((c) => c.name == "icon_content");

                var activeIcon = getMaterialIcon(
                    destView.control.attrString("selectedIcon", "")!);
                var selectedIconContentCtrls = destView.children
                    .where((c) => c.name == "selected_icon_content");

                return BottomNavigationBarItem(
                    tooltip: destView.control.attrString("tooltip", "")!,
                    icon: iconContentCtrls.isNotEmpty
                        ? createControl(destView.control,
                            iconContentCtrls.first.id, disabled)
                        : Icon(icon),
                    activeIcon: selectedIconContentCtrls.isNotEmpty
                        ? createControl(destView.control,
                            selectedIconContentCtrls.first.id, disabled)
                        : activeIcon != null
                            ? Icon(activeIcon)
                            : null,
                    label: label);
              }).toList());
        });

    return constrainedControl(context, navBar, widget.parent, widget.control);
  }
}
