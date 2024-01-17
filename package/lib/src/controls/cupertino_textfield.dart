import 'package:collection/collection.dart';
import 'package:flet/src/controls/textfield.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/shadows.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'form_field.dart';

class CupertinoTextFieldControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CupertinoTextFieldControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<CupertinoTextFieldControl> createState() =>
      _CupertinoTextFieldControlState();
}

class _CupertinoTextFieldControlState extends State<CupertinoTextFieldControl> {
  String _value = "";
  bool _revealPassword = false;
  bool _focused = false;
  late TextEditingController _controller;
  late final FocusNode _focusNode;
  late final FocusNode _shiftEnterfocusNode;
  String? _lastFocusValue;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
      onKey: (FocusNode node, RawKeyEvent evt) {
        if (!evt.isShiftPressed && evt.logicalKey.keyLabel == 'Enter') {
          if (evt is RawKeyDownEvent) {
            FletAppServices.of(context).server.sendPageEvent(
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
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _shiftEnterfocusNode.hasFocus ? "focus" : "blur",
        eventData: "");
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
  Widget build(BuildContext context) {
    debugPrint("CupertinoTextField build: ${widget.control.id}");

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint(
              "CupertinoTextField StoreConnector build: ${widget.control.id}");

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

          TextStyle? textStyle =
              parseTextStyle(Theme.of(context), widget.control, "textStyle");
          if (textSize != null || color != null || focusedColor != null) {
            textStyle = (textStyle ?? const TextStyle()).copyWith(
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

          FilteringTextInputFormatter? inputFilter =
              parseInputFilter(widget.control, "inputFilter");

          List<TextInputFormatter>? inputFormatters = [];
          // add non-null input formatters
          if (inputFilter != null) {
            inputFormatters.add(inputFilter);
          }
          if (textCapitalization != TextCapitalization.none) {
            inputFormatters
                .add(TextCapitalizationFormatter(textCapitalization));
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

          bool autocorrect = widget.control.attrBool("autocorrect", true)!;
          bool enableSuggestions =
              widget.control.attrBool("enableSuggestions", true)!;
          bool smartDashesType =
              widget.control.attrBool("smartDashesType", true)!;
          bool smartQuotesType =
              widget.control.attrBool("smartQuotesType", true)!;

          FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;

          var focusValue = widget.control.attrString("focus");
          if (focusValue != null && focusValue != _lastFocusValue) {
            _lastFocusValue = focusValue;
            focusNode.requestFocus();
          }

          BoxDecoration? defaultDecoration =
              const CupertinoTextField().decoration;
          var gradient =
              parseGradient(Theme.of(context), widget.control, "gradient");
          var blendMode = BlendMode.values.firstWhereOrNull((e) =>
              e.name.toLowerCase() ==
              widget.control.attrString("blendMode", "")!.toLowerCase());

          var borderRadius = parseBorderRadius(widget.control, "borderRadius");
          var bgColor = HexColor.fromString(
              Theme.of(context), widget.control.attrString("bgColor", "")!);

          Widget textField = CupertinoTextField(
              style: textStyle,
              placeholder: widget.control.attrString("placeholderText"),
              placeholderStyle: parseTextStyle(
                  Theme.of(context), widget.control, "placeholderStyle"),
              autofocus: autofocus,
              enabled: !disabled,
              onSubmitted: !multiline
                  ? (_) {
                      FletAppServices.of(context).server.sendPageEvent(
                          eventTarget: widget.control.id,
                          eventName: "submit",
                          eventData: "");
                    }
                  : null,
              decoration: defaultDecoration?.copyWith(
                  color: bgColor,
                  gradient: gradient,
                  backgroundBlendMode:
                      bgColor != null || gradient != null ? blendMode : null,
                  border:
                      parseBorder(Theme.of(context), widget.control, "border"),
                  borderRadius: borderRadius,
                  boxShadow: parseBoxShadow(
                      Theme.of(context), widget.control, "shadow")),
              cursorHeight: widget.control.attrDouble("cursorHeight"),
              showCursor: widget.control.attrBool("showCursor"),
              cursorWidth: widget.control.attrDouble("cursorWidth") ?? 2.0,
              cursorRadius: parseRadius(widget.control, "cursorRadius") ??
                  const Radius.circular(2.0),
              keyboardType: keyboardType,
              autocorrect: autocorrect,
              enableSuggestions: enableSuggestions,
              smartDashesType: smartDashesType
                  ? SmartDashesType.enabled
                  : SmartDashesType.disabled,
              smartQuotesType: smartQuotesType
                  ? SmartQuotesType.enabled
                  : SmartQuotesType.disabled,
              suffixMode: parseVisibilityMode(
                  widget.control.attrString("suffixVisibilityMode", "")!),
              prefixMode: parseVisibilityMode(
                  widget.control.attrString("prefixVisibilityMode", "")!),
              textAlign: textAlign,
              minLines: minLines,
              maxLines: maxLines,
              maxLength: maxLength,
              prefix: prefixControls.isNotEmpty
                  ? createControl(
                      widget.control, prefixControls.first.id, disabled)
                  : null,
              suffix: suffixControls.isNotEmpty
                  ? createControl(
                      widget.control, suffixControls.first.id, disabled)
                  : null,
              readOnly: readOnly,
              inputFormatters:
                  inputFormatters.isNotEmpty ? inputFormatters : null,
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
                FletAppServices.of(context)
                    .server
                    .updateControlProps(props: props);
                if (onChange) {
                  FletAppServices.of(context).server.sendPageEvent(
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
            return constrainedControl(
                context, textField, widget.parent, widget.control);
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
                    context, textField, widget.parent, widget.control);
              },
            );
          }
        });
  }
}
