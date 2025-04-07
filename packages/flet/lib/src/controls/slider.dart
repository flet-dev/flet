import 'package:flutter/material.dart';

import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import 'base_controls.dart';

class SliderControl extends StatefulWidget {
  final Control control;

  const SliderControl({
    super.key,
    required this.control,
  });

  @override
  State<SliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<SliderControl> {
  double _value = 0;
  final _debouncer = Debouncer(milliseconds: isDesktopPlatform() ? 10 : 100);
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _debouncer.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  void onChange(double value) {
    _value = value;
    var props = {"value": value};
    FletBackend.of(context)
        .updateControl(widget.control.id, props, python: false, notify: true);
    _debouncer.run(() {
      FletBackend.of(context)
          .updateControl(widget.control.id, props, notify: true);
      FletBackend.of(context).triggerControlEvent(widget.control, "change");
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliderControl build: ${widget.control.id}");
    // bool? adaptive =
    //     widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
    // if (adaptive == true &&
    //     (platform == TargetPlatform.iOS ||
    //         platform == TargetPlatform.macOS)) {
    //   return CupertinoSliderControl(
    //       control: widget.control,
    //       parentDisabled: widget.parentDisabled,
    //       backend: widget.backend);
    // }

    String? label = widget.control.getString("label");

    double min = widget.control.getDouble("min", 0)!;
    double max = widget.control.getDouble("max", 1)!;
    int round = widget.control.getInt("round", 0)!;

    double value = widget.control.getDouble("value", min)!;
    if (_value != value) {
      // verify limits
      if (value < min) {
        _value = min;
      } else if (value > max) {
        _value = max;
      } else {
        _value = value;
      }
    }

    var slider = Slider(
        autofocus: widget.control.getBool("autofocus", false)!,
        focusNode: _focusNode,
        value: _value,
        min: min,
        max: max,
        year2023: widget.control.getBool("year_2023"),
        divisions: widget.control.getInt("divisions"),
        label: label?.replaceAll("{value}", _value.toStringAsFixed(round)),
        activeColor: widget.control.getColor("active_color", context),
        inactiveColor: widget.control.getColor("inactive_color", context),
        overlayColor: parseWidgetStateColor(
            widget.control.get("overlay_color"), Theme.of(context)),
        allowedInteraction: widget.control.getSliderInteraction("interaction"),
        thumbColor: widget.control.getColor("thumb_color", context),
        padding: widget.control.getPadding("padding"),
        onChanged: !widget.control.disabled
            ? (double value) {
                onChange(value);
              }
            : null,
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        secondaryActiveColor:
            widget.control.getColor("secondary_active_color", context),
        secondaryTrackValue: widget.control.getDouble("secondary_track_value"),
        onChangeStart: !widget.control.disabled
            ? (double value) {
                FletBackend.of(context).triggerControlEvent(
                    widget.control, "change_start", value.toString());
              }
            : null,
        onChangeEnd: !widget.control.disabled
            ? (double value) {
                FletBackend.of(context).triggerControlEvent(
                    widget.control, "change_end", value.toString());
              }
            : null);

    return ConstrainedControl(control: widget.control, child: slider);
  }
}
