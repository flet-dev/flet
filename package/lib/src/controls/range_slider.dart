import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import '../utils/desktop.dart';
import 'create_control.dart';

class RangeSliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const RangeSliderControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<RangeSliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<RangeSliderControl> {
  Timer? _debounce;
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _debounce?.cancel();
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

  void onChange(double startValue, double endValue, Function dispatch) {
    var strStartValue = startValue.toString();
    var strEndValue = endValue.toString();
    debugPrint(strStartValue);

    if (_debounce?.isActive ?? false) _debounce!.cancel();
    List<Map<String, String>> props = [
      {
        "i": widget.control.id,
        "startvalue": strStartValue,
        "endvalue": strEndValue
      }
    ];
    dispatch(UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    _debounce = Timer(Duration(milliseconds: isDesktop() ? 10 : 100), () {
      final server = FletAppServices.of(context).server;
      server.updateControlProps(props: props);
      server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "change",
          eventData: strStartValue);
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("RangeSliderControl build: ${widget.control.id}");

    double startValue = widget.control.attrDouble("startvalue", 0)!;
    double endValue = widget.control.attrDouble("endvalue", 0)!;
    //String? label = widget.control.attrString("label");
    // String? startLabel = widget.control.attrString("startlabel");
    // String? endLabel = widget.control.attrString("endlabel");
    String? label = widget.control.attrString("label");
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    double min = widget.control.attrDouble("min", 0)!;
    double max = widget.control.attrDouble("max", 1)!;

    int? divisions = widget.control.attrInt("divisions");
    int round = widget.control.attrInt("round", 0)!;

    final server = FletAppServices.of(context).server;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint(
              "SliderControl StoreConnector build: ${widget.control.id}");

          var rangeSlider = RangeSlider(
            //autofocus: autofocus,
            //focusNode: _focusNode,
            values: RangeValues(startValue, endValue),
            labels: RangeLabels(
                (label ?? "")
                    .replaceAll("{value}", startValue.toStringAsFixed(round)),
                (label ?? "")
                    .replaceAll("{value}", endValue.toStringAsFixed(round))),
            min: min,
            max: max,
            divisions: divisions,
            //label:
            //    label?.replaceAll("{value}", _value.toStringAsFixed(round)),
            activeColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("activeColor", "")!),
            inactiveColor: HexColor.fromString(Theme.of(context),
                widget.control.attrString("inactiveColor", "")!),
            onChanged: !disabled
                ? (RangeValues newValues) {
                    onChange(newValues.start, newValues.end, dispatch);
                  }
                : null,
            // onChangeStart: !disabled
            //     ? (double value) {
            //         server.sendPageEvent(
            //             eventTarget: widget.control.id,
            //             eventName: "change_start",
            //             eventData: value.toString());
            //       }
            //     : null,
            // onChangeEnd: !disabled
            //     ? (double value) {
            //         server.sendPageEvent(
            //             eventTarget: widget.control.id,
            //             eventName: "change_end",
            //             eventData: value.toString());
            //       }
            //     : null);
          );

          return constrainedControl(
              context, rangeSlider, widget.parent, widget.control);
        });
  }
}
