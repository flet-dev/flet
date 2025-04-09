import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../widgets/error.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'list_tile.dart';

class CupertinoRadioControl extends StatefulWidget {
  final Control control;

  const CupertinoRadioControl({super.key, required this.control});

  @override
  State<CupertinoRadioControl> createState() => _CupertinoRadioControlState();
}

class _CupertinoRadioControlState extends State<CupertinoRadioControl>
    with FletStoreMixin {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onChange(String ancestorId, String? value) {
    widget.control.updateProperties({"value": value});
    widget.control.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoRadio build: ${widget.control.id}");

    String label = widget.control.getString("label", "")!;
    String value = widget.control.getString("value", "")!;
    LabelPosition labelPosition = parseLabelPosition(
        widget.control.getString("label_position"), LabelPosition.right)!;
    bool autofocus = widget.control.getBool("autofocus", false)!;

    return withControlAncestor(widget.control.id, "radiogroup",
        (context, viewModel) {
      debugPrint("CupertinoRadio build: ${widget.control.id}");

      if (viewModel.ancestor == null) {
        return const ErrorControl(
            "CupertinoRadio control must be enclosed with RadioGroup.");
      }

      String groupValue = viewModel.ancestor!.getString("value", "")!;
      String ancestorId = viewModel.ancestor!.id;

      var cupertinoRadio = CupertinoRadio<String>(
          autofocus: autofocus,
          focusNode: _focusNode,
          groupValue: groupValue,
          value: value,
          useCheckmarkStyle:
              widget.control.getBool("use_checkmark_style", false)!,
          fillColor: widget.control.getColor("fill_color", context),
          focusColor: widget.control.getColor("focus_color", context),
          toggleable: widget.control.getBool("toggleable", false)!,
          mouseCursor:
              parseMouseCursor(widget.control.getString("mouse_cursor")),
          activeColor: widget.control.getColor(
              "active_color", context, Theme.of(context).colorScheme.primary)!,
          inactiveColor: widget.control.getColor("inactive_color", context),
          onChanged: !widget.control.disabled
              ? (String? value) => _onChange(ancestorId, value)
              : null);

      ListTileClicks.of(context)?.notifier.addListener(() {
        _onChange(ancestorId, value);
      });

      Widget result = cupertinoRadio;
      if (label != "") {
        var labelWidget = widget.control.disabled
            ? Text(label,
                style: TextStyle(color: Theme.of(context).disabledColor))
            : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
        result = MergeSemantics(
            child: GestureDetector(
                onTap: !widget.control.disabled
                    ? () {
                        _onChange(ancestorId, value);
                      }
                    : null,
                child: labelPosition == LabelPosition.right
                    ? Row(children: [cupertinoRadio, labelWidget])
                    : Row(children: [labelWidget, cupertinoRadio])));
      }

      return ConstrainedControl(control: widget.control, child: result);
    });
  }
}
