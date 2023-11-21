import 'package:flutter/material.dart';
import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import '../utils/debouncer.dart';
import 'create_control.dart';

class SliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const SliderControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<SliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<SliderControl> {
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
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  void onChange(double value) {
    var svalue = value.toString();
    debugPrint(svalue);
    setState(() {
      _value = value;
    });

    List<Map<String, String>> props = [
      {"i": widget.control.id, "value": svalue}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    _debouncer.run(() {
      final server = FletAppServices.of(context).server;
      server.updateControlProps(props: props);
      server.sendPageEvent(
          eventTarget: widget.control.id, eventName: "change", eventData: '');
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SliderControl build: ${widget.control.id}");

    String? label = widget.control.attrString("label");
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    double min = widget.control.attrDouble("min", 0)!;
    double max = widget.control.attrDouble("max", 1)!;
    int? divisions = widget.control.attrInt("divisions");
    int round = widget.control.attrInt("round", 0)!;

    final server = FletAppServices.of(context).server;

    debugPrint("SliderControl StoreConnector build: ${widget.control.id}");

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
        inactiveColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("inactiveColor", "")!),
        thumbColor: HexColor.fromString(
            Theme.of(context), widget.control.attrString("thumbColor", "")!),
        onChanged: !disabled
            ? (double value) {
                onChange(value);
              }
            : null,
        onChangeStart: !disabled
            ? (double value) {
                server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "change_start",
                    eventData: value.toString());
              }
            : null,
        onChangeEnd: !disabled
            ? (double value) {
                server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "change_end",
                    eventData: value.toString());
              }
            : null);

    return constrainedControl(context, slider, widget.parent, widget.control);
  }
}
