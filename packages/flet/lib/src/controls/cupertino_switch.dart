import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_backend.dart';
//import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
//import '../utils/others.dart';
import 'base_controls.dart';
//import 'create_control.dart';
//import 'flet_store_mixin.dart';
import 'list_tile.dart';

class CupertinoSwitchControl extends StatefulWidget {
  //final Control? parent;
  final Control control;
  //final bool parentDisabled;
  //final FletControlBackend backend;

  const CupertinoSwitchControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.parentDisabled,
    //required this.backend,
  });

  @override
  State<CupertinoSwitchControl> createState() => _CupertinoSwitchControlState();
}

class _CupertinoSwitchControlState extends State<CupertinoSwitchControl> {
  bool _value = false;
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onChange(bool value) {
    _value = value;
    var props = {"value": value};
    FletBackend.of(context)
        .updateControl(widget.control.id, props, notify: true);
    FletBackend.of(context).triggerControlEvent(widget.control, "change");
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSwitchControl build: ${widget.control.id}");
    //bool disabled = widget.control.isDisabled || widget.parentDisabled;

    String label = widget.control.getString("label", "")!;
    //var label = widget.control.get("label");
    LabelPosition labelPosition =
        widget.control.getLabelPosition("label_position", LabelPosition.right)!;
    // LabelPosition labelPosition = parseLabelPosition(
    //     widget.control.attrString("labelPosition"), LabelPosition.right)!;
    bool autofocus = widget.control.getBool("autofocus", false)!;

    bool value = widget.control.getBool("value", false)!;
    if (_value != value) {
      _value = value;
    }

    ThemeData theme = Theme.of(context);
    // var materialThumbColor =
    //     parseWidgetStateColor(Theme.of(context), widget.control, "thumbColor");
    var materialThumbColor =
        widget.control.getWidgetStateColor("thumb_color", theme);

    // var materialTrackColor =
    //     parseWidgetStateColor(Theme.of(context), widget.control, "trackColor");
    var materialTrackColor =
        widget.control.getWidgetStateColor("track_color", theme);
    var activeThumbImage = widget.control.getString("active_thumb_image");
    var inactiveThumbImage = widget.control.getString("inactive_thumb_image");

    //return withPageArgs((context, pageArgs) {
    var swtch = CupertinoSwitch(
        autofocus: autofocus,
        focusNode: _focusNode,
        activeTrackColor:
            widget.control.getColor("active_track_color", context) ??
                widget.control.getColor("active_color", context),
        // TODO: deprecated in v0.26.0, remove in v0.29.0
        thumbColor: materialThumbColor?.resolve({}),
        inactiveTrackColor: materialTrackColor?.resolve({}),
        focusColor: widget.control.getColor("focusColor", context),
        // inactiveTrackColor:
        //     widget.control.attrColor("inactiveTrackColor", context),
        inactiveThumbColor:
            widget.control.getColor("inactive_thumb_color", context),
        trackOutlineColor:
            widget.control.getWidgetStateColor("track_outline_color", theme),
        trackOutlineWidth:
            widget.control.getWidgetStateDouble("track_outline_width"),
        thumbIcon: widget.control.getWidgetStateIcon("thumb_Icon", theme),
        inactiveThumbImage: getImageProvider(context, inactiveThumbImage, null),
        activeThumbImage: getImageProvider(context, activeThumbImage, null),
        onActiveThumbImageError: activeThumbImage == null
            ? null
            : (Object exception, StackTrace? stackTrace) {
                FletBackend.of(context).triggerControlEvent(
                    widget.control, "image_error", exception.toString());
              },
        onInactiveThumbImageError: inactiveThumbImage == null
            ? null
            : (Object exception, StackTrace? stackTrace) {
                FletBackend.of(context).triggerControlEvent(
                    widget.control, "image_error", exception.toString());
              },
        value: _value,
        offLabelColor: widget.control.getColor("off_label_color", context),
        onLabelColor: widget.control.getColor("on_label_color", context),
        onChanged: !widget.control.disabled
            ? (bool value) {
                _onChange(value);
              }
            : null);

    ListTileClicks.of(context)?.notifier.addListener(() {
      _onChange(!_value);
    });

    Widget result = swtch;
    if (label != "") {
      var labelWidget = widget.control.disabled
          ? Text(label,
              style: TextStyle(color: Theme.of(context).disabledColor))
          : MouseRegion(cursor: SystemMouseCursors.click, child: Text(label));
      result = MergeSemantics(
          child: GestureDetector(
              onTap: !widget.control.disabled
                  ? () {
                      _onChange(!_value);
                    }
                  : null,
              child: labelPosition == LabelPosition.right
                  ? Row(children: [swtch, labelWidget])
                  : Row(children: [labelWidget, swtch])));
    }

    return ConstrainedControl(control: widget.control, child: result);
    //});
  }
}
