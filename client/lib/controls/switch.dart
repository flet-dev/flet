import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

enum LabelPosition { right, left }

class SwitchControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const SwitchControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<SwitchControl> createState() => _SwitchControlState();
}

class _SwitchControlState extends State<SwitchControl> {
  bool _value = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SwitchControl build: ${widget.control.id}");

    String label = widget.control.attrString("label", "")!;
    LabelPosition labelPosition = LabelPosition.values.firstWhere(
        (p) =>
            p.name.toLowerCase() ==
            widget.control.attrString("labelPosition", "")!.toLowerCase(),
        orElse: () => LabelPosition.right);
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("Checkbox StoreConnector build: ${widget.control.id}");

          bool value = widget.control.attrBool("value", false)!;
          if (_value != value) {
            _value = value;
          }

          onChange(bool value) {
            var svalue = value.toString();
            debugPrint(svalue);
            setState(() {
              _value = value;
            });
            List<Map<String, String>> props = [
              {"i": widget.control.id, "value": svalue}
            ];
            dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            ws.updateControlProps(props: props);
            ws.pageEventFromWeb(
                eventTarget: widget.control.id,
                eventName: "change",
                eventData: svalue);
          }

          var swtch = Switch(
              value: _value,
              onChanged: !disabled
                  ? (bool value) {
                      onChange(value);
                    }
                  : null);

          Widget result = swtch;
          if (label != "") {
            var labelWidget = disabled
                ? Text(label,
                    style: TextStyle(color: Theme.of(context).disabledColor))
                : MouseRegion(
                    cursor: SystemMouseCursors.click, child: Text(label));
            result = GestureDetector(
                onTap: !disabled
                    ? () {
                        onChange(!_value);
                      }
                    : null,
                child: labelPosition == LabelPosition.right
                    ? Row(children: [swtch, labelWidget])
                    : Row(children: [labelWidget, swtch]));
          }

          return constrainedControl(result, widget.parent, widget.control);
        });
  }
}
