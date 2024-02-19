import 'package:flutter/material.dart';

import 'package:flet/flet.dart';
import 'package:google_nav_bar/google_nav_bar.dart';

class GoogleNavigationBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const GoogleNavigationBarControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<GoogleNavigationBarControl> createState() =>
      _GoogleNavigationBarControlState();
}

class _GoogleNavigationBarControlState extends State<GoogleNavigationBarControl>
    with FletStoreMixin {
  int _selectedIndex = 0;

  void _onTabChange(int index) {
    _selectedIndex = index;
    debugPrint("Selected index: $_selectedIndex");
    widget.backend.updateControlState(
        widget.control.id, {"selectedindex": _selectedIndex.toString()});
    widget.backend.triggerControlEvent(
        widget.control.id, "change", _selectedIndex.toString());
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("GoogleNavigationBarControl build: ${widget.control.id}");

    var selectedIndex = widget.control.attrInt("selectedIndex", 0)!;

    if (_selectedIndex != selectedIndex) {
      _selectedIndex = selectedIndex;
    }

    var navBar = withControls(
        widget.children
            .where((c) => c.isVisible && c.name == null)
            .map((c) => c.id), (content, viewModel) {
      return Container(
          margin: const EdgeInsets.all(16),
          color: HexColor.fromString(Theme.of(context),
              widget.control.attrString("bgcolor", "transparent")!),
          child: GNav(
            tabs: viewModel.controlViews.map((destView) {
              var label = destView.control.attrString("label", "")!;
              var icon =
                  parseIcon(destView.control.attrString("icon", "home")!)!;
              return GButton(
                icon: icon,
                iconColor: HexColor.fromString(Theme.of(context),
                    widget.control.attrString("iconColor", "")!),
                iconActiveColor: HexColor.fromString(Theme.of(context),
                    widget.control.attrString("iconActiveColor", "")!),
                text: label,
              );
            }).toList(),
            selectedIndex: _selectedIndex,
            onTabChange: _onTabChange,
            color: HexColor.fromString(
                Theme.of(context), widget.control.attrString("color", "")!),
            gap: widget.control.attrDouble("gap", 8.0)!,
            tabBorder: parseBorder(Theme.of(context), widget.control, "border"),
            tabBorderRadius: widget.control.attrDouble("borderRadius", 100.0)!,
            tabBackgroundColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("bgActiveColor", "transparent")!)!,
            iconSize: widget.control.attrDouble("iconSize", 30.0)!,
            activeColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("activeColor", "")!),
            tabActiveBorder:
                parseBorder(Theme.of(context), widget.control, "activeBorder"),
            mainAxisAlignment: parseMainAxisAlignment(
                widget.control, "alignment", MainAxisAlignment.center),
          ));
    });

    return constrainedControl(context, navBar, widget.parent, widget.control);
  }
}
