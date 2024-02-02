import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';
import 'create_control.dart';
import 'cupertino_slider.dart';
import 'flet_control_stateful_mixin.dart';
import 'flet_store_mixin.dart';

class SliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const SliderControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  State<SliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<SliderControl>
    with FletControlStatefulMixin, FletStoreMixin {
  double _value = 0;
  final _debouncer = Debouncer(milliseconds: isDesktop() ? 10 : 100);
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
    sendControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  void onChange(double value) {
    var svalue = value.toString();
    debugPrint(svalue);
    _value = value;
    var props = {"value": svalue};
    updateControlProps(widget.control.id, props, clientOnly: true);
    _debouncer.run(() {
      updateControlProps(widget.control.id, props);
      sendControlEvent(widget.control.id, "change", '');
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliderControl build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoSliderControl(
            control: widget.control, parentDisabled: widget.parentDisabled);
      }

      String? label = widget.control.attrString("label");
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      double min = widget.control.attrDouble("min", 0)!;
      double max = widget.control.attrDouble("max", 1)!;
      int? divisions = widget.control.attrInt("divisions");
      int round = widget.control.attrInt("round", 0)!;

      debugPrint("SliderControl build: ${widget.control.id}");

      double value = widget.control.attrDouble("value", 0)!;
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
          autofocus: autofocus,
          focusNode: _focusNode,
          value: _value,
          min: min,
          max: max,
          divisions: divisions,
          label: label?.replaceAll("{value}", _value.toStringAsFixed(round)),
          activeColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("activeColor", "")!),
          inactiveColor: HexColor.fromString(Theme.of(context),
              widget.control.attrString("inactiveColor", "")!),
          thumbColor: HexColor.fromString(
              Theme.of(context), widget.control.attrString("thumbColor", "")!),
          onChanged: !disabled
              ? (double value) {
                  onChange(value);
                }
              : null,
          onChangeStart: !disabled
              ? (double value) {
                  sendControlEvent(
                      widget.control.id, "change_start", value.toString());
                }
              : null,
          onChangeEnd: !disabled
              ? (double value) {
                  sendControlEvent(
                      widget.control.id, "change_end", value.toString());
                }
              : null);

      return constrainedControl(context, slider, widget.parent, widget.control);
    });
  }
}
