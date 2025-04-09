import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/cupertino.dart';

import '../models/control.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class CupertinoPickerControl extends StatefulWidget {
  final Control control;

  const CupertinoPickerControl({super.key, required this.control});

  @override
  State<CupertinoPickerControl> createState() => _CupertinoPickerControlState();
}

class _CupertinoPickerControlState extends State<CupertinoPickerControl> {
  int _index = 0;
  int previousIndex = 0;
  bool isScrollUp = false;
  bool isScrollDown = true;
  FixedExtentScrollController scrollController = FixedExtentScrollController();

  @override
  void initState() {
    super.initState();
    scrollController = FixedExtentScrollController(
        initialItem: widget.control.getInt("selectedIndex", _index)!);
    scrollController.addListener(_manageScroll);
  }

  void _manageScroll() {
    // https://stackoverflow.com/a/75283541
    // Fixes https://github.com/flet-dev/flet/issues/3649
    if (previousIndex != scrollController.selectedItem) {
      isScrollDown = previousIndex < scrollController.selectedItem;
      isScrollUp = previousIndex > scrollController.selectedItem;

      var previousIndexTemp = previousIndex;
      previousIndex = scrollController.selectedItem;

      if (isScrollUp) {
        scrollController.jumpToItem(previousIndexTemp - 1);
      } else if (isScrollDown) {
        scrollController.jumpToItem(previousIndexTemp + 1);
      }
    }
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
        _index = index;
        widget.control.updateProperties({"selected_index": index});
        widget.control.triggerEvent("change", index);
      },
      children: widget.control.children("controls").map((c) {
        return Center(child: ControlWidget(control: c));
      }).toList(),
    );

    return ConstrainedControl(control: widget.control, child: picker);
  }
}
