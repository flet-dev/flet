import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class CupertinoPickerControl extends StatefulWidget {
  final Control control;

  CupertinoPickerControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<CupertinoPickerControl> createState() => _CupertinoPickerControlState();
}

class _CupertinoPickerControlState extends State<CupertinoPickerControl> {
  FixedExtentScrollController scrollController = FixedExtentScrollController();

  @override
  void initState() {
    super.initState();
    scrollController = FixedExtentScrollController(
        initialItem: widget.control.getInt("selected_index", 0)!);
  }

  @override
  void dispose() {
    scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoPicker build: ${widget.control.id}");

    Widget picker = CupertinoPicker(
      scrollController: scrollController,
      backgroundColor: widget.control.getColor("bgcolor", context),
      diameterRatio: widget.control.getDouble("diameter_ratio", 1.07)!,
      magnification: widget.control.getDouble("magnification", 1.0)!,
      squeeze: widget.control.getDouble("squeeze", 1.45)!,
      offAxisFraction: widget.control.getDouble("off_axis_fraction", 0.0)!,
      itemExtent: widget.control.getDouble("item_extent", 32.0)!,
      useMagnifier: widget.control.getBool("use_magnifier", false)!,
      looping: widget.control.getBool("looping", false)!,
      selectionOverlay: widget.control.buildWidget("selection_overlay") ??
          CupertinoPickerDefaultSelectionOverlay(
            background: widget.control.getColor(
                "default_selection_overlay_bgcolor",
                context,
                CupertinoColors.tertiarySystemFill)!,
          ),
      onSelectedItemChanged: (int index) {
        widget.control.updateProperties({"selected_index": index});
        widget.control.triggerEvent("change", index);
      },
      children: widget.control.children("controls").map((c) {
        return Center(child: ControlWidget(control: c));
      }).toList(),
    );

    return LayoutControl(control: widget.control, child: picker);
  }
}
