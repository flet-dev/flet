import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';
import '../utils/alignment.dart';
import 'create_control.dart';
import 'scrollable_control.dart';

class AppBarControl extends StatelessWidget implements PreferredSizeWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final List<Control> children;

  AppBar? _appBar;

  AppBarControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("AppBar build: ${control.id}");

    // final spacing = control.attrDouble("spacing", 10)!;
    // final mainAlignment =
    //     parseMainAxisAlignment(control, "alignment", MainAxisAlignment.start);
    // bool tight = control.attrBool("tight", false)!;
    // bool wrap = control.attrBool("wrap", false)!;
    // ScrollMode scrollMode = ScrollMode.values.firstWhere(
    //     (m) =>
    //         m.name.toLowerCase() ==
    //         control.attrString("scroll", "")!.toLowerCase(),
    //     orElse: () => ScrollMode.none);
    // bool disabled = control.isDisabled || parentDisabled;

    // List<Widget> controls = [];

    // bool firstControl = true;
    // for (var ctrl in children.where((c) => c.isVisible)) {
    //   // spacer between displayed controls
    //   if (!wrap &&
    //       spacing > 0 &&
    //       !firstControl &&
    //       mainAlignment != MainAxisAlignment.spaceAround &&
    //       mainAlignment != MainAxisAlignment.spaceBetween &&
    //       mainAlignment != MainAxisAlignment.spaceEvenly) {
    //     controls.add(SizedBox(width: spacing));
    //   }
    //   firstControl = false;

    //   // displayed control
    //   controls.add(createControl(control, ctrl.id, disabled));
    // }

    _appBar = AppBar(
      title: Text("Hello!"),
    );
    return _appBar!;
  }

  @override
  Size get preferredSize => _appBar!.preferredSize;
}
