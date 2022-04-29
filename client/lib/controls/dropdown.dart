import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../web_socket_client.dart';
import 'create_control.dart';
import 'form_field.dart';

class DropdownControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const DropdownControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<DropdownControl> createState() => _DropdownControlState();
}

class _DropdownControlState extends State<DropdownControl> {
  String? _value;
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
  Widget build(BuildContext context) {
    debugPrint("Dropdown build: ${widget.control.id}");

    return StoreConnector<AppState, ControlChildrenViewModel>(
        distinct: true,
        converter: (store) => ControlChildrenViewModel.fromStore(
            store, widget.control.id,
            dispatch: store.dispatch),
        builder: (context, itemsView) {
          debugPrint("Dropdown StoreConnector build: ${widget.control.id}");

          bool autofocus = widget.control.attrBool("autofocus", false)!;
          bool disabled = widget.control.isDisabled || widget.parentDisabled;

          String? value = widget.control.attrString("value");
          if (_value != value) {
            _value = value;
          }

          var prefixControls =
              itemsView.children.where((c) => c.name == "prefix");
          var suffixControls =
              itemsView.children.where((c) => c.name == "suffix");

          var dropDown = DropdownButtonFormField<String>(
            autofocus: autofocus,
            focusNode: _focusNode,
            value: _value,
            decoration: buildInputDecoration(
                widget.control,
                prefixControls.isNotEmpty ? prefixControls.first : null,
                suffixControls.isNotEmpty ? suffixControls.first : null,
                null),
            onChanged: (String? value) {
              debugPrint("Dropdown selected value: $value");
              setState(() {
                _value = value!;
              });
              List<Map<String, String>> props = [
                {"i": widget.control.id, "value": value!}
              ];
              itemsView.dispatch(UpdateControlPropsAction(
                  UpdateControlPropsPayload(props: props)));
              ws.updateControlProps(props: props);
              ws.pageEventFromWeb(
                  eventTarget: widget.control.id,
                  eventName: "change",
                  eventData: value);
            },
            items: itemsView.children
                .where((c) => c.name == null)
                .map<DropdownMenuItem<String>>((Control itemCtrl) {
              return DropdownMenuItem<String>(
                enabled: !(disabled || itemCtrl.isDisabled),
                value: itemCtrl.attrs["key"] ??
                    itemCtrl.attrs["text"] ??
                    itemCtrl.id,
                child: Text(itemCtrl.attrs["text"] ??
                    itemCtrl.attrs["key"] ??
                    itemCtrl.id),
              );
            }).toList(),
          );

          return constrainedControl(dropDown, widget.parent, widget.control);
        });
  }
}
