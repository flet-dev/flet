import 'package:flet_view/controls/error.dart';
import 'package:flet_view/models/control_ancestor_view_model.dart';
import 'package:flet_view/models/control_type.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

enum LabelPosition { right, left }

class RadioControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const RadioControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<RadioControl> createState() => _RadioControlState();
}

class _RadioControlState extends State<RadioControl> {
  final FocusNode _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: _focusNode.hasFocus ? "focus" : "blur",
          eventData: "");
    });
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Radio build: ${widget.control.id}");

    String label = widget.control.attrString("label", "")!;
    String value = widget.control.attrString("value", "")!;
    LabelPosition labelPosition = LabelPosition.values.firstWhere(
        (p) =>
            p.name.toLowerCase() ==
            widget.control.attrString("labelPosition", "")!.toLowerCase(),
        orElse: () => LabelPosition.right);
    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return StoreConnector<AppState, ControlAncestorViewModel>(
        distinct: true,
        converter: (store) => ControlAncestorViewModel.fromStore(
            store, widget.control.id, ControlType.radioGroup),
        builder: (context, viewModel) {
          debugPrint("Radio StoreConnector build: ${widget.control.id}");

          if (viewModel.ancestor == null) {
            return const ErrorControl(
                "Radio control must be enclosed with RadioGroup.");
          }

          String groupValue = viewModel.ancestor!.attrString("value", "")!;

          onChange(String? value) {
            var svalue = value != null ? value.toString() : "";
            debugPrint(svalue);
            List<Map<String, String>> props = [
              {"i": viewModel.ancestor!.id, "value": svalue}
            ];
            viewModel.dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            ws.updateControlProps(props: props);
            ws.pageEventFromWeb(
                eventTarget: viewModel.ancestor!.id,
                eventName: "change",
                eventData: svalue);
          }

          var radio = Radio<String>(
              autofocus: autofocus,
              focusNode: _focusNode,
              groupValue: groupValue,
              value: value,
              onChanged: !disabled
                  ? (String? value) {
                      onChange(value);
                    }
                  : null);

          Widget result = radio;
          if (label != "") {
            var labelWidget = disabled
                ? Text(label,
                    style: TextStyle(color: Theme.of(context).disabledColor))
                : MouseRegion(
                    cursor: SystemMouseCursors.click, child: Text(label));
            result = GestureDetector(
                onTap: !disabled
                    ? () {
                        onChange(value);
                      }
                    : null,
                child: labelPosition == LabelPosition.right
                    ? Row(children: [radio, labelWidget])
                    : Row(children: [labelWidget, radio]));
          }

          return constrainedControl(result, widget.parent, widget.control);
        });
  }
}
