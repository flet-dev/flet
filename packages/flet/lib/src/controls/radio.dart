import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/theme.dart';
import '../widgets/error.dart';
import '../widgets/radio_group_provider.dart';
import 'base_controls.dart';
import 'list_tile.dart';

class RadioControl extends StatefulWidget {
  final Control control;

  RadioControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<RadioControl> createState() => _RadioControlState();
}

class _RadioControlState extends State<RadioControl> {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    ListTileClicks.of(context)?.notifier.addListener(_toggleRadio);
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    ListTileClicks.of(context)?.notifier.removeListener(_toggleRadio);
    _focusNode.dispose();
    super.dispose();
  }

  void _toggleRadio() {
    var radioGroup = RadioGroupProvider.of(context);
    if (radioGroup != null) {
      String value = widget.control.getString("value", "")!;
      _onChange(radioGroup, value);
    }
  }

  void _onChange(Control radioGroup, String? value) {
    radioGroup.updateProperties({"value": value}, notify: true);
    radioGroup.triggerEvent("change", value);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Radio build: ${widget.control.id}");

    var label = widget.control.getString("label", "")!;
    var value = widget.control.getString("value", "")!;
    var labelPosition =
        widget.control.getLabelPosition("label_position", LabelPosition.right)!;
    var visualDensity = widget.control.getVisualDensity("visual_density");
    bool autofocus = widget.control.getBool("autofocus", false)!;

    var labelStyle =
        widget.control.getTextStyle("label_style", Theme.of(context));
    if (widget.control.disabled && labelStyle != null) {
      labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
    }

    debugPrint("Radio StoreConnector build: ${widget.control.id}");

    var radioGroup = RadioGroupProvider.of(context);

    if (radioGroup == null) {
      return const ErrorControl("Radio must be enclosed within RadioGroup");
    }

    String groupValue = radioGroup.getString("value", "")!;

    var radio = Radio<String>(
        autofocus: autofocus,
        focusNode: _focusNode,
        groupValue: groupValue,
        mouseCursor: parseMouseCursor(widget.control.getString("mouseCursor")),
        value: value,
        activeColor: widget.control.getColor("active_color", context),
        focusColor: widget.control.getColor("focus_color", context),
        hoverColor: widget.control.getColor("hover_color", context),
        splashRadius: widget.control.getDouble("splash_radius"),
        toggleable: widget.control.getBool("toggleable", false)!,
        fillColor:
            widget.control.getWidgetStateColor("fill_color", Theme.of(context)),
        overlayColor: widget.control
            .getWidgetStateColor("overlay_color", Theme.of(context)),
        visualDensity: visualDensity,
        onChanged: !widget.control.disabled
            ? (String? value) => _onChange(radioGroup, value)
            : null);

    Widget result = radio;
    if (label != "") {
      var labelWidget = widget.control.disabled
          ? Text(label, style: labelStyle)
          : MouseRegion(
              cursor: SystemMouseCursors.click,
              child: Text(label, style: labelStyle));
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !widget.control.disabled
                  ? () => _onChange(radioGroup, value)
                  : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [radio, labelWidget])
                  : Row(children: [labelWidget, radio])));
    }

    return LayoutControl(control: widget.control, child: result);
  }
}
