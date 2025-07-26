import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoSegmentedButtonControl extends StatefulWidget {
  final Control control;

  CupertinoSegmentedButtonControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoSegmentedButtonControl> createState() =>
      _CupertinoSegmentedButtonControlState();
}

class _CupertinoSegmentedButtonControlState
    extends State<CupertinoSegmentedButtonControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSegmentedButtonControl build: ${widget.control.id}");

    var controls = widget.control.buildWidgets("controls");
    var selectedIndex = widget.control.getInt("selected_index");

    if (controls.length < 2) {
      return const ErrorControl(
          "CupertinoSegmentedButton must have at minimum two visible controls");
    }

    var segmnetedButton = CupertinoSegmentedControl(
      groupValue: selectedIndex,
      borderColor: widget.control.getColor("border_color", context),
      selectedColor: widget.control.getColor("selected_color", context),
      unselectedColor: widget.control.getColor("unselected_color", context),
      pressedColor: widget.control.getColor("click_color", context),
      disabledColor: widget.control.getColor("disabled_color", context),
      disabledTextColor:
          widget.control.getColor("disabled_text_color", context),
      padding: widget.control.getPadding("padding"),
      children: controls.asMap().map((i, c) => MapEntry(i, c)),
      onValueChanged: (int index) {
        if (!widget.control.disabled) {
          widget.control.updateProperties({"selected_index": index});
          widget.control.triggerEvent("change", index);
          setState(() {
            selectedIndex = index;
          });
        }
      },
    );

    return ConstrainedControl(control: widget.control, child: segmnetedButton);
  }
}
