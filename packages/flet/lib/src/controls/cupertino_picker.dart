import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';

const double _kItemExtent = 32.0;
const double _kDefaultDiameterRatio = 1.07;
const double _kSqueeze = 1.45;

class CupertinoPickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoPickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.backend});

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
        initialItem: widget.control.attrInt("selectedIndex", _index)!);
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

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    List<Widget> ctrls = widget.children.where((c) => c.isVisible).map((c) {
      return Center(
          child: createControl(widget.control, c.id, disabled,
              parentAdaptive: widget.parentAdaptive));
    }).toList();

    double itemExtent = widget.control.attrDouble("itemExtent", _kItemExtent)!;
    double diameterRatio =
        widget.control.attrDouble("diameterRatio", _kDefaultDiameterRatio)!;
    double magnification = widget.control.attrDouble("magnification", 1.0)!;
    double squeeze = widget.control.attrDouble("squeeze", _kSqueeze)!;
    double offAxisFraction = widget.control.attrDouble("offAxisFraction", 0.0)!;
    bool useMagnifier = widget.control.attrBool("useMagnifier", false)!;
    bool looping = widget.control.attrBool("looping", false)!;
    Color? backgroundColor = widget.control.attrColor("bgColor", context);

    Widget picker = CupertinoPicker(
      scrollController: scrollController,
      backgroundColor: backgroundColor,
      diameterRatio: diameterRatio,
      magnification: magnification,
      squeeze: squeeze,
      offAxisFraction: offAxisFraction,
      itemExtent: itemExtent,
      useMagnifier: useMagnifier,
      looping: looping,
      onSelectedItemChanged: (int index) {
        _index = index;
        widget.backend.updateControlState(
            widget.control.id, {"selectedIndex": index.toString()});
        widget.backend
            .triggerControlEvent(widget.control.id, "change", index.toString());
      },
      children: ctrls,
    );

    return constrainedControl(context, picker, widget.parent, widget.control);
  }
}
