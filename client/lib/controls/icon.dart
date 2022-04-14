import 'package:flet_view/controls/create_control.dart';
import 'package:flet_view/utils/colors.dart';
import 'package:flet_view/utils/icons.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';

class IconControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const IconControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Icon build: ${control.id}");

    var name = control.attrString("name", "")!;
    var size = control.attrDouble("size", null);
    var color = HexColor.fromString(context, control.attrString("color", "")!);

    return commonControl(
        Icon(
          getMaterialIcon(name),
          size: size,
          color: color,
        ),
        parent,
        control);
  }
}
