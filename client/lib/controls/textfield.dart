import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../web_socket_client.dart';
import 'create_control.dart';
import 'form_field.dart';

class TextFieldControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const TextFieldControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<TextFieldControl> createState() => _TextFieldControlState();
}

class _TextFieldControlState extends State<TextFieldControl> {
  String _value = "";
  bool _revealPassword = false;
  late TextEditingController _controller;
  late final FocusNode _focusNode = FocusNode();

  late final _shiftEnterfocusNode = FocusNode(
    onKey: (FocusNode node, RawKeyEvent evt) {
      if (!evt.isShiftPressed && evt.logicalKey.keyLabel == 'Enter') {
        if (evt is RawKeyDownEvent) {
          ws.pageEventFromWeb(
              eventTarget: widget.control.id,
              eventName: "submit",
              eventData: "");
        }
        return KeyEventResult.handled;
      } else {
        return KeyEventResult.ignored;
      }
    },
  );

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _shiftEnterfocusNode.addListener(() {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: _shiftEnterfocusNode.hasFocus ? "focus" : "blur",
          eventData: "");
    });
    _focusNode.addListener(() {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: _focusNode.hasFocus ? "focus" : "blur",
          eventData: "");
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TextField build: ${widget.control.id}");

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("TextField StoreConnector build: ${widget.control.id}");

          String value = widget.control.attrs["value"] ?? "";
          if (_value != value) {
            _value = value;
            _controller.text = value;
          }

          var prefixControls = widget.children.where((c) => c.name == "prefix");
          var suffixControls = widget.children.where((c) => c.name == "suffix");

          bool shiftEnter = widget.control.attrBool("shiftEnter", false)!;
          bool multiline =
              widget.control.attrBool("multiline", false)! || shiftEnter;
          int minLines = widget.control.attrInt("minLines", 1)!;
          int? maxLines =
              widget.control.attrInt("maxLines", multiline ? null : 1);

          bool readOnly = widget.control.attrBool("readOnly", false)!;
          bool password = widget.control.attrBool("password", false)!;
          bool canRevealPassword =
              widget.control.attrBool("canRevealPassword", false)!;
          bool onChange = widget.control.attrBool("onChange", false)!;

          Widget? revealPasswordIcon;
          if (password && canRevealPassword) {
            revealPasswordIcon = GestureDetector(
                child: Icon(
                  _revealPassword ? Icons.visibility_off : Icons.visibility,
                ),
                onTap: () {
                  setState(() {
                    _revealPassword = !_revealPassword;
                  });
                });
          }

          TextInputType keyboardType = parseTextInputType(
              widget.control.attrString("keyboardType", "")!);

          if (multiline) {
            keyboardType = TextInputType.multiline;
          }

          TextAlign textAlign = TextAlign.values.firstWhere(
            ((b) =>
                b.name ==
                widget.control.attrString("textAlign", "")!.toLowerCase()),
            orElse: () => TextAlign.start,
          );

          var textField = TextFormField(
              autofocus: autofocus,
              enabled: !disabled,
              onFieldSubmitted: !multiline
                  ? (_) {
                      ws.pageEventFromWeb(
                          eventTarget: widget.control.id,
                          eventName: "submit",
                          eventData: "");
                    }
                  : null,
              decoration: buildInputDecoration(
                  widget.control,
                  prefixControls.isNotEmpty ? prefixControls.first : null,
                  suffixControls.isNotEmpty ? suffixControls.first : null,
                  revealPasswordIcon),
              keyboardType: keyboardType,
              textAlign: textAlign,
              minLines: minLines,
              maxLines: maxLines,
              readOnly: readOnly,
              obscureText: password && !_revealPassword,
              controller: _controller,
              focusNode: shiftEnter ? _shiftEnterfocusNode : _focusNode,
              onChanged: (String value) {
                //debugPrint(value);
                setState(() {
                  _value = value;
                });
                List<Map<String, String>> props = [
                  {"i": widget.control.id, "value": value}
                ];
                dispatch(UpdateControlPropsAction(
                    UpdateControlPropsPayload(props: props)));
                ws.updateControlProps(props: props);
                if (onChange) {
                  ws.pageEventFromWeb(
                      eventTarget: widget.control.id,
                      eventName: "change",
                      eventData: value);
                }
              });

          return constrainedControl(textField, widget.parent, widget.control);
        });
  }
}
