import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
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
  bool _focused = false;
  late TextEditingController _controller;
  late final FocusNode _focusNode;
  late final FocusNode _shiftEnterfocusNode;
  String _lastFocusedTimestamp = "";

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
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
    _shiftEnterfocusNode.addListener(_onShiftEnterFocusChange);
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _controller.dispose();
    _shiftEnterfocusNode.removeListener(_onShiftEnterFocusChange);
    _shiftEnterfocusNode.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onShiftEnterFocusChange() {
    setState(() {
      _focused = _shiftEnterfocusNode.hasFocus;
    });
    ws.pageEventFromWeb(
        eventTarget: widget.control.id,
        eventName: _shiftEnterfocusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    ws.pageEventFromWeb(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
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

          var prefixControls =
              widget.children.where((c) => c.name == "prefix" && c.isVisible);
          var suffixControls =
              widget.children.where((c) => c.name == "suffix" && c.isVisible);

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

          var cursorColor = HexColor.fromString(
              Theme.of(context), widget.control.attrString("cursorColor", "")!);
          var selectionColor = HexColor.fromString(Theme.of(context),
              widget.control.attrString("selectionColor", "")!);

          int? maxLength = widget.control.attrInt("maxLength");

          var textSize = widget.control.attrDouble("textSize");

          var color = HexColor.fromString(
              Theme.of(context), widget.control.attrString("color", "")!);
          var focusedColor = HexColor.fromString(Theme.of(context),
              widget.control.attrString("focusedColor", "")!);

          TextStyle? textStyle;
          if (textSize != null || color != null || focusedColor != null) {
            textStyle = TextStyle(
                fontSize: textSize,
                color: _focused ? focusedColor ?? color : color);
          }

          TextCapitalization? textCapitalization = TextCapitalization.values
              .firstWhere(
                  (a) =>
                      a.name.toLowerCase() ==
                      widget.control
                          .attrString("capitalization", "")!
                          .toLowerCase(),
                  orElse: () => TextCapitalization.none);

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

          FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;

          var focusValue = widget.control.attrString("focus");
          if (focusValue != null) {
            debugPrint("Focus JSON value: $focusValue");
            var jv = json.decode(focusValue);
            var focus = jv["d"] as bool;
            var ts = jv["ts"] as String;
            if (focus && ts != _lastFocusedTimestamp) {
              focusNode.requestFocus();
              _lastFocusedTimestamp = ts;
            }
          }

          Widget textField = TextFormField(
              style: textStyle,
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
                  context,
                  widget.control,
                  prefixControls.isNotEmpty ? prefixControls.first : null,
                  suffixControls.isNotEmpty ? suffixControls.first : null,
                  revealPasswordIcon,
                  _focused),
              keyboardType: keyboardType,
              textAlign: textAlign,
              minLines: minLines,
              maxLines: maxLines,
              maxLength: maxLength,
              readOnly: readOnly,
              inputFormatters: textCapitalization != TextCapitalization.none
                  ? [
                      TextCapitalizationFormatter(textCapitalization),
                    ]
                  : null,
              obscureText: password && !_revealPassword,
              controller: _controller,
              focusNode: focusNode,
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

          if (cursorColor != null || selectionColor != null) {
            textField = TextSelectionTheme(
                data: TextSelectionTheme.of(context).copyWith(
                    cursorColor: cursorColor, selectionColor: selectionColor),
                child: textField);
          }

          if (widget.control.attrInt("expand", 0)! > 0) {
            return constrainedControl(textField, widget.parent, widget.control);
          } else {
            return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
                if (constraints.maxWidth == double.infinity &&
                    widget.control.attrDouble("width") == null) {
                  textField = ConstrainedBox(
                    constraints: const BoxConstraints.tightFor(width: 300),
                    child: textField,
                  );
                }

                return constrainedControl(
                    textField, widget.parent, widget.control);
              },
            );
          }
        });
  }
}

class TextCapitalizationFormatter extends TextInputFormatter {
  final TextCapitalization capitalization;

  TextCapitalizationFormatter(this.capitalization);

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    String text = '';

    switch (capitalization) {
      case TextCapitalization.words:
        text = capitalizeFirstofEach(newValue.text);
        break;
      case TextCapitalization.sentences:
        List<String> sentences = newValue.text.split('.');
        for (int i = 0; i < sentences.length; i++) {
          sentences[i] = inCaps(sentences[i]);
          print(sentences[i]);
        }
        text = sentences.join('.');
        break;
      case TextCapitalization.characters:
        text = allInCaps(newValue.text);
        break;
      case TextCapitalization.none:
        text = newValue.text;
        break;
    }

    return TextEditingValue(
      text: text,
      selection: newValue.selection,
    );
  }

  /// 'Hello world'
  static String inCaps(String text) {
    if (text.isEmpty) {
      return text;
    }
    String result = '';
    for (int i = 0; i < text.length; i++) {
      if (text[i] != ' ') {
        result += '${text[i].toUpperCase()}${text.substring(i + 1)}';
        break;
      } else {
        result += text[i];
      }
    }
    return result;
  }

  /// 'HELLO WORLD'
  static String allInCaps(String text) => text.toUpperCase();

  /// 'Hello World'
  static String capitalizeFirstofEach(String text) => text
      .replaceAll(RegExp(' +'), ' ')
      .split(" ")
      .map((str) => inCaps(str))
      .join(" ");
}
