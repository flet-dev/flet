import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import 'create_control.dart';

class AutocompleteControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const AutocompleteControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<AutocompleteControl> createState() => _AutocompleteControlState();
}

class _AutocompleteControlState extends State<AutocompleteControl> {
  String? _value;
  bool _focused = false; // to use later,
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Autocomplete build: ${widget.control.id}");

    final server = FletAppServices.of(context).server;

    return StoreConnector<AppState, ControlChildrenViewModel>(
        distinct: true,
        converter: (store) => ControlChildrenViewModel.fromStore(
            store, widget.control.id,
            dispatch: store.dispatch),
        builder: (context, itemsView) {
          debugPrint("Autocomplete StoreConnector build: ${widget.control.id}");

          Iterable<String> items = itemsView.children
              .where((c) => c.name == null)
              .map<String>((Control itemCtrl) {
            return itemCtrl.attrs["text"] ?? itemCtrl.attrs["key"] ?? "";
          });

          void onChanged(String? value) {
            debugPrint("Autocomplete text changed: $value");
            setState(() {
              _value = value!;
            });
            List<Map<String, String>> props = [
              {"i": widget.control.id, "value": value!}
            ];
            itemsView.dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            server.updateControlProps(props: props);
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "change",
                eventData: value);
          }

          void onSubmit(String? value) {
            debugPrint("Autocomplete selected value: $value");
            setState(() {
              _value = value!;
            });
            List<Map<String, String>> props = [
              {"i": widget.control.id, "value": value!}
            ];
            itemsView.dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            server.updateControlProps(props: props);
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "submit",
                eventData: value);
          }

          Iterable<String> getItems(TextEditingValue value) {
            if (value.text != _value) {
              onChanged(value.text);
            }
            return items;
          }

          String? value = widget.control.attrString("value");
          if (_value != value) {
            _value = value;
          }

          var focusValue = widget.control.attrString("focus");
          if (focusValue != null) {
            debugPrint("Focus JSON value: $focusValue");
            var jv = json.decode(focusValue);
            var focus = jv["d"] as bool;
            if (focus) {
              _focusNode.requestFocus();
            }
          }

          Widget autocomplete = Autocomplete<String>(
            optionsBuilder: getItems,
            onSelected: onSubmit,
          );

          if (widget.control.attrInt("expand", 0)! > 0) {
            return constrainedControl(
                context, autocomplete, widget.parent, widget.control);
          } else {
            return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
                if (constraints.maxWidth == double.infinity &&
                    widget.control.attrDouble("width") == null) {
                  autocomplete = ConstrainedBox(
                    constraints: const BoxConstraints.tightFor(width: 300),
                    child: autocomplete,
                  );
                }

                return constrainedControl(
                    context, autocomplete, widget.parent, widget.control);
              },
            );
          }
        });
  }
}
