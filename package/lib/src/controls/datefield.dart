import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:intl/intl.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import 'create_control.dart';

class DateFieldControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const DateFieldControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<DateFieldControl> createState() => _DateFieldControlState();
}

class _DateFieldControlState extends State<DateFieldControl> {
  DateTime? _value;

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
    debugPrint("DateField build: ${widget.control.id}");

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    DateTime? firstDate = widget.control.attrDateTime("firstDate");
    DateTime? lastDate = widget.control.attrDateTime("firstDate");
    bool onChange = widget.control.attrBool("onChange", false)!;

    // TODO: later
    // ButtonStyle? buttonStyle = parseButtonStyle(Theme.of(context), widget.control, "buttonStyle");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("DateField StoreConnector build: ${widget.control.id}");

          void onChanged(DateTime? dateValue) {
            DateTime? value = dateValue;
            debugPrint(value.toString());
            setState(() {
              _value = value;
            });
            String stringValue = value?.toIso8601String() ?? "null";
            List<Map<String, String>> props = [
              {"i": widget.control.id, "value": stringValue}
            ];
            dispatch(UpdateControlPropsAction(
                UpdateControlPropsPayload(props: props)));
            FletAppServices.of(context).server.updateControlProps(props: props);
            if (onChange) {
              FletAppServices.of(context).server.sendPageEvent(
                  eventTarget: widget.control.id,
                  eventName: "change",
                  eventData: stringValue);
            }
            FletAppServices.of(context).server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "submit",
                eventData: "");
          }

          DateTime? value = widget.control.attrDateTime("value");
          if (_value != value) {
            _value = value;
          }

          Future<void> selectDateDialog() async {
            final DateTime? pickedDate = await showDatePicker(
                context: context,
                initialDate: _value ?? DateTime.now(),
                firstDate: firstDate ?? DateTime(1900),
                lastDate: lastDate ?? DateTime(2050));
            if (!disabled && pickedDate != null && pickedDate != value) {
              onChanged(pickedDate);
            }
          }

          String buttonText;

          if (value == null) {
            buttonText = "";
          } else {
            buttonText = DateFormat.yMMMd().format(value);
          }

          Widget button = ElevatedButton(
            onPressed: selectDateDialog,
            autofocus: autofocus,
            child: Text(buttonText),
          );

          if (widget.control.attrInt("expand", 0)! > 0) {
            return constrainedControl(
                context, button, widget.parent, widget.control);
          } else {
            return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
                if (constraints.maxWidth == double.infinity &&
                    widget.control.attrDouble("width") == null) {
                  button = ConstrainedBox(
                    constraints: const BoxConstraints.tightFor(width: 300),
                    child: button,
                  );
                }

                return constrainedControl(
                    context, button, widget.parent, widget.control);
              },
            );
          }
        });
  }
}
