import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_ancestor_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import 'create_control.dart';
import 'error.dart';
import 'list_tile.dart';

enum LabelPosition { right, left }

class CupertinoRadioControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const CupertinoRadioControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.dispatch})
      : super(key: key);

  @override
  State<CupertinoRadioControl> createState() => _CupertinoRadioControlState();
}

class _CupertinoRadioControlState extends State<CupertinoRadioControl> {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
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

  void _onChange(String ancestorId, String? value) {
    var svalue = value ?? "";
    debugPrint(svalue);
    List<Map<String, String>> props = [
      {"i": ancestorId, "value": svalue}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));

    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: ancestorId, eventName: "change", eventData: svalue);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoRadio build: ${widget.control.id}");

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
        ignoreChange: (state) {
          return state.controls[widget.control.id] == null;
        },
        converter: (store) => ControlAncestorViewModel.fromStore(
            store, widget.control.id, "radiogroup"),
        builder: (context, viewModel) {
          debugPrint(
              "CupertinoRadio StoreConnector build: ${widget.control.id}");

          if (viewModel.ancestor == null) {
            return const ErrorControl(
                "CupertinoRadio control must be enclosed with RadioGroup.");
          }

          String groupValue = viewModel.ancestor!.attrString("value", "")!;
          String ancestorId = viewModel.ancestor!.id;

          var cupertinoRadio = CupertinoRadio<String>(
              autofocus: autofocus,
              focusNode: _focusNode,
              groupValue: groupValue,
              value: value,
              useCheckmarkStyle:
                  widget.control.attrBool("useCheckmarkStyle", false)!,
              fillColor: HexColor.fromString(Theme.of(context),
                  widget.control.attrString("fillColor", "")!),
              activeColor: HexColor.fromString(Theme.of(context),
                  widget.control.attrString("activeColor", "")!),
              inactiveColor: HexColor.fromString(Theme.of(context),
                  widget.control.attrString("inactiveColor", "")!),
              onChanged: !disabled
                  ? (String? value) {
                      _onChange(ancestorId, value);
                    }
                  : null);

          ListTileClicks.of(context)?.notifier.addListener(() {
            _onChange(ancestorId, value);
          });

          Widget result = cupertinoRadio;
          if (label != "") {
            var labelWidget = disabled
                ? Text(label,
                    style: TextStyle(color: Theme.of(context).disabledColor))
                : MouseRegion(
                    cursor: SystemMouseCursors.click, child: Text(label));
            result = MergeSemantics(
                child: GestureDetector(
                    onTap: !disabled
                        ? () {
                            _onChange(ancestorId, value);
                          }
                        : null,
                    child: labelPosition == LabelPosition.right
                        ? Row(children: [cupertinoRadio, labelWidget])
                        : Row(children: [labelWidget, cupertinoRadio])));
          }

          return constrainedControl(
              context, result, widget.parent, widget.control);
        });
  }
}
