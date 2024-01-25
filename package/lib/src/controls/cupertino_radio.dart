import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'error.dart';
import 'flet_control_state.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class CupertinoRadioControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const CupertinoRadioControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled});

  @override
  State<CupertinoRadioControl> createState() => _CupertinoRadioControlState();
}

class _CupertinoRadioControlState extends State<CupertinoRadioControl>
    with FletControlState {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    sendControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onChange(String ancestorId, String? value) {
    var svalue = value ?? "";
    debugPrint(svalue);
    updateControlProps(ancestorId, {"value": svalue});
    sendControlEvent(ancestorId, "change", svalue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoRadio build: ${widget.control.id}");

    String label = widget.control.attrString("label", "")!;
    String value = widget.control.attrString("value", "")!;
    LabelPosition labelPosition = LabelPosition.values.firstWhere(
        (p) =>
            p.name.toLowerCase() ==
            widget.control.attrString("labelPosition", "")!.toLowerCase(),
        orElse: () => LabelPosition.right);
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return withControlAncestor(widget.control.id, "radiogroup",
        (context, viewModel) {
      debugPrint("CupertinoRadio build: ${widget.control.id}");

      if (viewModel.ancestor == null) {
        return const ErrorControl(
            "CupertinoRadio control must be enclosed with RadioGroup.");
      }

      String groupValue = viewModel.ancestor!.attrString("value", "")!;
      String ancestorId = viewModel.ancestor!.id;

      var cupertinoRadio = CupertinoRadio<String>(
          autofocus: autofocus,
          focusNode: _focusNode,
          groupValue: groupValue,
          value: value,
          useCheckmarkStyle:
              widget.control.attrBool("useCheckmarkStyle", false)!,
          fillColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("fillColor", "")!),
          activeColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("activeColor", "")!),
          inactiveColor: HexColor.fromString(Theme.of(context),
              widget.control.attrString("inactiveColor", "")!),
          onChanged: !disabled
              ? (String? value) {
                  _onChange(ancestorId, value);
                }
              : null);

      ListTileClicks.of(context)?.notifier.addListener(() {
        _onChange(ancestorId, value);
      });

      Widget result = cupertinoRadio;
      if (label != "") {
        var labelWidget = disabled
            ? Text(label,
                style: TextStyle(color: Theme.of(context).disabledColor))
            : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
        result = MergeSemantics(
            child: GestureDetector(
                onTap: !disabled
                    ? () {
                        _onChange(ancestorId, value);
                      }
                    : null,
                child: labelPosition == LabelPosition.right
                    ? Row(children: [cupertinoRadio, labelWidget])
                    : Row(children: [labelWidget, cupertinoRadio])));
      }

      return constrainedControl(context, result, widget.parent, widget.control);
    });
  }
}
