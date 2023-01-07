import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';

class HapticFeedbackControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const HapticFeedbackControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<HapticFeedbackControl> createState() => _HapticFeedbackControlState();
}

class _HapticFeedbackControlState extends State<HapticFeedbackControl> {
  String? _method;

  @override
  Widget build(BuildContext context) {
    debugPrint("HapticFeedback build: ${widget.control.id}");

    () async {
      var method = widget.control.attrString("method");
      if (method != null && method != _method) {
        _method = method;
        debugPrint("HapticFeedback JSON value: $_method");

        List<Map<String, String>> props = [
          {"i": widget.control.id, "method": ""}
        ];
        FletAppServices.of(context).store.dispatch(
            UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
        FletAppServices.of(context).server.updateControlProps(props: props);

        var mj = json.decode(method);
        var name = mj["n"] as String;

        switch (name) {
          case "heavy_impact":
            HapticFeedback.heavyImpact();
            break;
          case "light_impact":
            HapticFeedback.lightImpact();
            break;
          case "medium_impact":
            HapticFeedback.mediumImpact();
            break;
          case "vibrate":
            HapticFeedback.vibrate();
            break;
        }
      }
    }();

    return const SizedBox.shrink();
  }
}
