import 'package:flet/src/controls/error.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class AppBarControl extends StatelessWidget implements PreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;
  final double height;

  const AppBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.height})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    var leadingCtrls =
        children.where((c) => c.name == "leading" && c.isVisible);
    var titleCtrls = children.where((c) => c.name == "title" && c.isVisible);
    var actionCtrls = children.where((c) => c.name == "action" && c.isVisible);

    var leadingWidth = control.attrDouble("leadingWidth");
    var elevation = control.attrDouble("elevation");
    var centerTitle = control.attrBool("centerTitle", false)!;
    var automaticallyImplyLeading =
        control.attrBool("automaticallyImplyLeading", true)!;
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    var bgcolor = HexColor.fromString(
        Theme.of(context), control.attrString("bgcolor", "")!);

    return AppBar(
      leading: leadingCtrls.isNotEmpty
          ? createControl(control, leadingCtrls.first.id, control.isDisabled)
          : null,
      leadingWidth: leadingWidth,
      automaticallyImplyLeading: automaticallyImplyLeading,
      title: titleCtrls.isNotEmpty
          ? createControl(control, titleCtrls.first.id, control.isDisabled)
          : null,
      centerTitle: centerTitle,
      toolbarHeight: preferredSize.height,
      foregroundColor: color,
      backgroundColor: bgcolor,
      elevation: elevation,
      actions: actionCtrls
          .map((c) => createControl(control, c.id, control.isDisabled))
          .toList(),
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(height);
}

class BottomAppBarControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const BottomAppBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<BottomAppBarControl> createState() => _BottomAppBarControlState();
}

class _BottomAppBarControlState extends State<BottomAppBarControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("BottomAppBarControl build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);

    var s = widget.control.attrString("shape");
    NotchedShape? shape;
    if (s == "circular") {
      shape = const CircularNotchedRectangle();
    } else if (s == "auto") {
      shape = const AutomaticNotchedShape(ContinuousRectangleBorder());
    }

    var elevation = widget.control.attrDouble("elevation", 0);
    if (elevation! < 0) {
      return const ErrorControl(
          "The Elevation of the BottomAppBar must be greater than or equal to 0 !");
    }

    var clipBehavior = Clip.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            widget.control.attrString("clipBehavior", "")!.toLowerCase(),
        orElse: () => Clip.none);
    var bottomAppBar = StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(
            store,
            widget.children
                .where((c) => c.isVisible && c.name == null)
                .map((c) => c.id)),
        builder: (content, viewModel) {
          return BottomAppBar(
            clipBehavior: clipBehavior,
            padding: parseEdgeInsets(widget.control, "padding"),
            height: widget.control.attrDouble("height"),
            elevation: elevation,
            shape: shape,
            shadowColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("shadowColor", "")!),
            surfaceTintColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("surfaceTintColor", "")!),
            color: HexColor.fromString(
                Theme.of(context), widget.control.attrString("bgColor", "")!),
            notchMargin: widget.control.attrDouble("notchMargin", 4.0)!,
            child: contentCtrls.isNotEmpty
                ? createControl(widget.control, contentCtrls.first.id, disabled)
                : null,
          );
        });

    return constrainedControl(
        context, bottomAppBar, widget.parent, widget.control);
  }
}
