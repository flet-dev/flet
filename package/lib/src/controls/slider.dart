import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import 'create_control.dart';

class SliderControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const SliderControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<SliderControl> createState() => _SliderControlState();
}

class _SliderControlState extends State<SliderControl> {
  double _value = 0;
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
    FletAppServices.of(context).ws.pageEventFromWeb(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  void onChange(double value, Function dispatch) {
    var svalue = value.toString();
    debugPrint(svalue);
    setState(() {
      _value = value;
    });

    if (_debounce?.isActive ?? false) _debounce!.cancel();
    List<Map<String, String>> props = [
      {"i": widget.control.id, "value": svalue}
    ];
    dispatch(UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    _debounce = Timer(const Duration(milliseconds: 100), () {
      final ws = FletAppServices.of(context).ws;
      ws.updateControlProps(props: props);
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: "change",
          eventData: svalue);
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

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint(
              "SliderControl StoreConnector build: ${widget.control.id}");

          double value = widget.control.attrDouble("value", 0)!;
          if (_value != value) {
            _value = value;
          }

          var slider = Slider(
              autofocus: autofocus,
              focusNode: _focusNode,
              value: _value,
              min: min,
              max: max,
              divisions: divisions,
              label: label?.replaceAll("{value}", _value.toString()),
              onChanged: !disabled
                  ? (double value) {
                      onChange(value, dispatch);
                    }
                  : null);

          return constrainedControl(slider, widget.parent, widget.control);
        });
  }
}
