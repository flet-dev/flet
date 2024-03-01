import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'error.dart';

const double _kItemExtent = 32.0;
const double _kDefaultDiameterRatio = 1.07;
const double _kSqueeze = 1.45;

class CupertinoPickerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  const CupertinoPickerControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentAdaptive,
      required this.parentDisabled,
      required this.nextChild,
      required this.backend});

  @override
  State<CupertinoPickerControl> createState() => _CupertinoPickerControlState();
}

class _CupertinoPickerControlState extends State<CupertinoPickerControl> {
  Widget _createPicker() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    List<Widget> ctrls = widget.children.where((c) => c.isVisible).map((c) {
      return Center(
          child: createControl(widget.control, c.id, disabled,
              parentAdaptive: widget.parentAdaptive));
    }).toList();

    double itemExtent = widget.control.attrDouble("itemExtent", _kItemExtent)!;
    int? selectedIndex = widget.control.attrInt("selectedIndex");
    double diameterRatio =
        widget.control.attrDouble("diameterRatio", _kDefaultDiameterRatio)!;
    double magnification = widget.control.attrDouble("magnification", 1.0)!;
    double squeeze = widget.control.attrDouble("squeeze", _kSqueeze)!;
    double offAxisFraction = widget.control.attrDouble("offAxisFraction", 0.0)!;
    bool useMagnifier = widget.control.attrBool("useMagnifier", false)!;
    bool looping = widget.control.attrBool("looping", false)!;
    Color? backgroundColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgColor", "")!);

    Widget picker = CupertinoPicker(
      backgroundColor: backgroundColor,
      diameterRatio: diameterRatio,
      magnification: magnification,
      squeeze: squeeze,
      offAxisFraction: offAxisFraction,
      itemExtent: itemExtent,
      useMagnifier: useMagnifier,
      looping: looping,
      onSelectedItemChanged: (int index) {
        widget.backend.updateControlState(
            widget.control.id, {"selectedIndex": index.toString()});
        widget.backend
            .triggerControlEvent(widget.control.id, "change", index.toString());
      },
      scrollController: selectedIndex != null
          ? FixedExtentScrollController(initialItem: selectedIndex)
          : null,
      children: ctrls,
    );

    return Container(
      height: 216,
      padding: const EdgeInsets.only(top: 6.0),
      // The Bottom margin is provided to align the popup above the system navigation bar.
      margin: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      // Provide a background color for the popup.
      color: CupertinoColors.systemBackground.resolveFrom(context),
      // Use a SafeArea widget to avoid system overlaps.
      child: SafeArea(
        top: false,
        child: picker,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoPicker build: ${widget.control.id}");

    bool lastOpen = widget.control.state["open"] ?? false;

    var open = widget.control.attrBool("open", false)!;
    var modal = widget.control.attrBool("modal", false)!;

    debugPrint("Current open state: $lastOpen");
    debugPrint("New open state: $open");

    if (open && (open != lastOpen)) {
      var dialog = _createPicker();
      if (dialog is ErrorControl) {
        return dialog;
      }

      // close previous dialog
      if (ModalRoute.of(context)?.isCurrent != true) {
        Navigator.of(context).pop();
      }

      widget.control.state["open"] = open;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        showCupertinoModalPopup(
            barrierDismissible: !modal,
            useRootNavigator: false,
            context: context,
            builder: (context) => _createPicker()).then((value) {
          lastOpen = widget.control.state["open"] ?? false;
          debugPrint("Picker should be dismissed ($hashCode): $lastOpen");
          bool shouldDismiss = lastOpen;
          widget.control.state["open"] = false;

          if (shouldDismiss) {
            widget.backend
                .updateControlState(widget.control.id, {"open": "false"});
            widget.backend
                .triggerControlEvent(widget.control.id, "dismiss", "");
          }
        });
      });
    } else if (open != lastOpen && lastOpen) {
      Navigator.of(context).pop();
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
