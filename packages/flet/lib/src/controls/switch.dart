import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../widgets/flet_store_mixin.dart';
import 'base_controls.dart';
import 'control_widget.dart';
import 'list_tile.dart';

class SwitchControl extends StatefulWidget {
  //final Control? parent;
  final Control control;
  //final bool parentDisabled;
  //final bool? parentAdaptive;
  //final List<Control> children;
  //final FletControlBackend backend;

  const SwitchControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.parentDisabled,
    //required this.parentAdaptive,
    //required this.children,
    //required this.backend,
  });

  @override
  State<SwitchControl> createState() => _SwitchControlState();
}

class _SwitchControlState extends State<SwitchControl> with FletStoreMixin {
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
    // var svalue = value.toString();
    // debugPrint(svalue);
    _value = value;
    var props = {"value": value};
    FletBackend.of(context)
        .updateControl(widget.control.id, props, python: false, notify: true);
    FletBackend.of(context).triggerControlEvent(widget.control, "change");
  }

  // void _onFocusChange() {
  //   FletBackend.of(context).triggerControlEvent(
  //       widget.control,
  //       _focusNode.hasFocus ? "focus" : "blur",
  //       _focusNode.hasPrimaryFocus.toString());
  // }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SwitchControl build: ${widget.control.id}");

    // return withPagePlatform((context, platform) {
    //   bool? adaptive =
    //       widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    //   if (adaptive == true &&
    //       (platform == TargetPlatform.iOS ||
    //           platform == TargetPlatform.macOS)) {
    //     return CupertinoSwitchControl(
    //         control: widget.control,
    //         parentDisabled: widget.parentDisabled,
    //         backend: widget.backend);
    //   }

    //var label = widget.children.firstWhereOrNull((c) => c.isVisible);
    var label = widget.control.get("label");
    // String labelStr =
    //     label is String ? widget.control.getString("label", "")! : "";
    LabelPosition labelPosition =
        widget.control.getLabelPosition("label_position", LabelPosition.right)!;
    double? width = widget.control.getDouble("width");
    double? height = widget.control.getDouble("height");
    bool autofocus = widget.control.getBool("autofocus", false)!;

    TextStyle? labelStyle =
        widget.control.getTextStyle("label_style", Theme.of(context));
    if (widget.control.disabled && labelStyle != null) {
      labelStyle = labelStyle.apply(color: Theme.of(context).disabledColor);
    }

    bool value = widget.control.getBool("value", false)!;
    if (_value != value) {
      _value = value;
    }

    var s = Switch(
        autofocus: autofocus,
        focusNode: _focusNode,
        activeColor: widget.control.getColor("active_color", context),
        activeTrackColor:
            widget.control.getColor("active_track_color", context),
        inactiveThumbColor:
            widget.control.getColor("inactive_thumb_color", context),
        inactiveTrackColor:
            widget.control.getColor("inactive_track_color", context),
        thumbColor: widget.control
            .getWidgetStateColor("thumb_color", Theme.of(context)),
        thumbIcon:
            widget.control.getWidgetStateIcon("thumb_icon", Theme.of(context)),
        trackColor: widget.control
            .getWidgetStateColor("track_color", Theme.of(context)),
        focusColor: widget.control.getColor("focus_color", context),
        value: _value,
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        splashRadius: widget.control.getDouble("splash_radius"),
        hoverColor: widget.control.getColor("hover_color", context),
        overlayColor: widget.control
            .getWidgetStateColor("overlay_color", Theme.of(context)),
        trackOutlineColor: widget.control
            .getWidgetStateColor("track_outline_color", Theme.of(context)),
        trackOutlineWidth:
            widget.control.getWidgetStateDouble("track_outline_width"),
        onChanged: !widget.control.disabled
            ? (bool value) {
                _onChange(value);
              }
            : null);

    ListTileClicks.of(context)?.notifier.addListener(() {
      _onChange(!_value);
    });

    Widget result = s;
    //Widget? labelWidget;
    // if (label != null || (labelStr != "")) {
    //   Widget? labelWidget;
    //   if (label != null) {
    //     //labelWidget = createControl(widget.control, label.id, disabled);
    //     labelWidget = ControlWidget(control: label);
    //   } else {
    //     labelWidget = widget.control.disabled
    //         ? Text(labelStr, style: labelStyle)
    //         : MouseRegion(
    //             cursor: SystemMouseCursors.click,
    //             child: Text(labelStr, style: labelStyle));
    //   }
    if (label is Control || (label is String)) {
      Widget? labelWidget;
      if (label is Control) {
        //labelWidget = createControl(widget.control, label.id, disabled);
        labelWidget = ControlWidget(control: label);
      } else {
        labelWidget = widget.control.disabled
            ? Text(label, style: labelStyle)
            : MouseRegion(
                cursor: SystemMouseCursors.click,
                child: Text(label, style: labelStyle));
      }

      result = MergeSemantics(
        child: GestureDetector(
          onTap: !widget.control.disabled
              ? () {
                  _onChange(!_value);
                }
              : null,
          child: labelPosition == LabelPosition.right
              ? Row(
                  // mainAxisSize: MainAxisSize.min,
                  children: [result, labelWidget],
                )
              : Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [labelWidget, result],
                ),
        ),
      );
    }
    if (width != null || height != null) {
      result = SizedBox(
        width: width,
        height: height,
        child: FittedBox(
          fit: BoxFit.fill,
          child: result,
        ),
      );
    }

    return ConstrainedControl(control: widget.control, child: result);
    //  });
  }
}
