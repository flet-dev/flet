import 'package:flet_view/controls/create_control.dart';
import 'package:flutter/material.dart';
import 'package:flet_view/protocol/update_control_props_payload.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../web_socket_client.dart';

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

          bool disabled = widget.control.isDisabled || widget.parentDisabled;

          String? value = widget.control.attrs["value"];
          if (value == "") {
            value = null;
          }
          if (_value != value) {
            _value = value;
          }

          var dropDown = DropdownButton<String>(
            value: _value,
            // icon: const Icon(Icons.arrow_downward),
            // elevation: 16,
            // style: const TextStyle(color: Colors.deepPurple),
            // underline: Container(
            //   height: 1,
            //   color: Colors.deepPurpleAccent,
            // ),
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
            },
            items: itemsView.children
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

          return expandable(dropDown, widget.parent, widget.control);
        });
  }
}
