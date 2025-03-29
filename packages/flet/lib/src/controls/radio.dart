import 'package:flet/src/utils/theme.dart';
import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'cupertino_radio.dart';
import 'error.dart';
import 'flet_store_mixin.dart';
import 'list_tile.dart';

class RadioControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const RadioControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<RadioControl> createState() => _RadioControlState();
}

class _RadioControlState extends State<RadioControl> with FletStoreMixin {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
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
    widget.backend.updateControlState(ancestorId, {"value": svalue});
    widget.backend.triggerControlEvent(ancestorId, "change", svalue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Radio build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.getBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoRadioControl(
            control: widget.control,
            parentDisabled: widget.parentDisabled,
            backend: widget.backend);
      }

      String label = widget.control.getString("label", "")!;
      String value = widget.control.getString("value", "")!;
      LabelPosition labelPosition = parseLabelPosition(
          widget.control.getString("labelPosition"), LabelPosition.right)!;
      VisualDensity? visualDensity =
          parseVisualDensity(widget.control.getString("visualDensity"));
      bool autofocus = widget.control.getBool("autofocus", false)!;
      bool disabled = widget.control.disabled || widget.parentDisabled;

      TextStyle? labelStyle =
          parseTextStyle(Theme.of(context), widget.control, "labelStyle");
      if (disabled && labelStyle != null) {
        labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
      }

      return withControlAncestor(widget.control.id, "radiogroup",
          (context, viewModel) {
        debugPrint("Radio StoreConnector build: ${widget.control.id}");

        if (viewModel.ancestor == null) {
          return const ErrorControl("Radio must be enclosed within RadioGroup");
        }

        String groupValue = viewModel.ancestor!.getString("value", "")!;
        String ancestorId = viewModel.ancestor!.id;

        var radio = Radio<String>(
            autofocus: autofocus,
            focusNode: _focusNode,
            groupValue: groupValue,
            mouseCursor:
                parseMouseCursor(widget.control.getString("mouseCursor")),
            value: value,
            activeColor: widget.control.getColor("activeColor", context),
            focusColor: widget.control.getColor("focusColor", context),
            hoverColor: widget.control.getColor("hoverColor", context),
            splashRadius: widget.control.getDouble("splashRadius"),
            toggleable: widget.control.getBool("toggleable", false)!,
            fillColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "fillColor"),
            overlayColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "overlayColor"),
            visualDensity: visualDensity,
            onChanged: !disabled
                ? (String? value) {
                    _onChange(ancestorId, value);
                  }
                : null);

        ListTileClicks.of(context)?.notifier.addListener(() {
          _onChange(ancestorId, value);
        });

        Widget result = radio;
        if (label != "") {
          var labelWidget = disabled
              ? Text(label, style: labelStyle)
              : MouseRegion(
                  cursor: SystemMouseCursors.click,
                  child: Text(label, style: labelStyle));
          result = MergeSemantics(
              child: GestureDetector(
                  onTap: !disabled
                      ? () {
                          _onChange(ancestorId, value);
                        }
                      : null,
                  child: labelPosition == LabelPosition.right
                      ? Row(children: [radio, labelWidget])
                      : Row(children: [labelWidget, radio])));
        }

        return constrainedControl(
            context, result, widget.parent, widget.control);
      });
    });
  }
}
