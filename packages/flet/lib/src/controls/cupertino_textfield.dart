import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/form_field.dart';
import '../utils/gradient.dart';
import '../utils/shadows.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'textfield.dart';

class CupertinoTextFieldControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoTextFieldControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoTextFieldControl> createState() =>
      _CupertinoTextFieldControlState();
}

class _CupertinoTextFieldControlState extends State<CupertinoTextFieldControl> {
  String _value = "";
  bool _focused = false;
  bool _revealPassword = false;
  late TextEditingController _controller;
  late final FocusNode _focusNode;
  late final FocusNode _shiftEnterfocusNode;
  String? _lastFocusValue;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent evt) {
        if (!HardwareKeyboard.instance.isShiftPressed &&
            evt.logicalKey.keyLabel == 'Enter') {
          if (evt is KeyDownEvent) {
            widget.backend.triggerControlEvent(widget.control.id, "submit");
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
    widget.backend.triggerControlEvent(widget.control.id,
        _shiftEnterfocusNode.hasFocus ? "focus" : "blur", "");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoTextField build: ${widget.control.id}");

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    debugPrint("CupertinoTextField StoreConnector build: ${widget.control.id}");

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
    bool multiline = widget.control.attrBool("multiline", false)! || shiftEnter;
    int minLines = widget.control.attrInt("minLines", 1)!;
    int? maxLines = widget.control.attrInt("maxLines", multiline ? null : 1);

    bool readOnly = widget.control.attrBool("readOnly", false)!;
    bool password = widget.control.attrBool("password", false)!;
    bool onChange = widget.control.attrBool("onChange", false)!;

    var cursorColor = widget.control.attrColor("cursorColor", context);
    var selectionColor = widget.control.attrColor("selectionColor", context);

    int? maxLength = widget.control.attrInt("maxLength");

    var textSize = widget.control.attrDouble("textSize");

    var color = widget.control.attrColor("color", context);
    var focusedColor = widget.control.attrColor("focusedColor", context);

    TextStyle? textStyle =
        parseTextStyle(Theme.of(context), widget.control, "textStyle");
    if (textSize != null || color != null || focusedColor != null) {
      textStyle = (textStyle ?? const TextStyle()).copyWith(
          fontSize: textSize, color: _focused ? focusedColor ?? color : color);
    }

    TextCapitalization? textCapitalization = TextCapitalization.values
        .firstWhere(
            (a) =>
                a.name.toLowerCase() ==
                widget.control.attrString("capitalization", "")!.toLowerCase(),
            orElse: () => TextCapitalization.none);

    FilteringTextInputFormatter? inputFilter =
        parseInputFilter(widget.control, "inputFilter");

    List<TextInputFormatter>? inputFormatters = [];
    // add non-null input formatters
    if (inputFilter != null) {
      inputFormatters.add(inputFilter);
    }
    if (textCapitalization != TextCapitalization.none) {
      inputFormatters.add(TextCapitalizationFormatter(textCapitalization));
    }

    TextInputType keyboardType =
        parseTextInputType(widget.control.attrString("keyboardType", "")!);

    if (multiline) {
      keyboardType = TextInputType.multiline;
    }

    TextAlign textAlign = TextAlign.values.firstWhere(
      ((b) =>
          b.name == widget.control.attrString("textAlign", "")!.toLowerCase()),
      orElse: () => TextAlign.start,
    );

    double? textVerticalAlign = widget.control.attrDouble("textVerticalAlign");

    bool rtl = widget.control.attrBool("rtl", false)!;
    bool autocorrect = widget.control.attrBool("autocorrect", true)!;
    bool enableSuggestions =
        widget.control.attrBool("enableSuggestions", true)!;
    bool smartDashesType = widget.control.attrBool("smartDashesType", true)!;
    bool smartQuotesType = widget.control.attrBool("smartQuotesType", true)!;

    FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;

    var focusValue = widget.control.attrString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      focusNode.requestFocus();
    }

    BorderRadius? borderRadius =
        parseBorderRadius(widget.control, "borderRadius");

    BoxBorder? border;
    double borderWidth = widget.control.attrDouble("borderWidth") ?? 1.0;
    Color borderColor = widget.control.attrColor("borderColor", context) ??
        const Color(0xFF000000);

    try {
      border = parseBorder(Theme.of(context), widget.control, "border");
      // adaptive TextField is being created
    } catch (e) {
      FormFieldInputBorder inputBorder = FormFieldInputBorder.values.firstWhere(
        ((b) =>
            b.name == widget.control.attrString("border", "")!.toLowerCase()),
        orElse: () => FormFieldInputBorder.outline,
      );

      if (inputBorder == FormFieldInputBorder.outline) {
        border = Border.all(color: borderColor, width: borderWidth);
      } else if (inputBorder == FormFieldInputBorder.underline) {
        border =
            Border(bottom: BorderSide(color: borderColor, width: borderWidth));
        borderRadius = BorderRadius.zero;
      }
    }

    bool canRevealPassword =
        widget.control.attrBool("canRevealPassword", false)!;

    Widget? revealPasswordIcon;
    if (password && canRevealPassword) {
      revealPasswordIcon = GestureDetector(
          child: Icon(
            _revealPassword ? CupertinoIcons.eye_slash : CupertinoIcons.eye,
          ),
          onTap: () {
            setState(() {
              _revealPassword = !_revealPassword;
            });
          });
    }

    BoxDecoration? defaultDecoration = const CupertinoTextField().decoration;
    var gradient = parseGradient(Theme.of(context), widget.control, "gradient");
    var blendMode = BlendMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("blendMode", "")!.toLowerCase());

    var bgColor = widget.control.attrColor("bgColor", context);
    // for adaptive TextField use label for placeholder
    var placeholder = widget.control.attrString("placeholderText") ??
        widget.control.attrString("label");
    // for adaptive TextField use labelStyle for placeholderStyle
    var placeholderStyle =
        parseTextStyle(Theme.of(context), widget.control, "placeholderStyle") ??
            parseTextStyle(Theme.of(context), widget.control, "labelStyle");

    Widget textField = CupertinoTextField(
        style: textStyle,
        textAlignVertical: textVerticalAlign != null
            ? TextAlignVertical(y: textVerticalAlign)
            : null,
        placeholder: placeholder,
        placeholderStyle: placeholderStyle,
        autofocus: autofocus,
        enabled: !disabled,
        onSubmitted: !multiline
            ? (_) {
                widget.backend
                    .triggerControlEvent(widget.control.id, "submit", "");
              }
            : null,
        decoration: defaultDecoration?.copyWith(
            color: bgColor,
            gradient: gradient,
            backgroundBlendMode:
                bgColor != null || gradient != null ? blendMode : null,
            border: border,
            borderRadius: borderRadius,
            boxShadow:
                parseBoxShadow(Theme.of(context), widget.control, "shadow")),
        cursorHeight: widget.control.attrDouble("cursorHeight"),
        showCursor: widget.control.attrBool("showCursor"),
        cursorWidth: widget.control.attrDouble("cursorWidth") ?? 2.0,
        cursorRadius: parseRadius(widget.control, "cursorRadius") ??
            const Radius.circular(2.0),
        keyboardType: keyboardType,
        clearButtonSemanticLabel:
            widget.control.attrString("clearButtonSemanticsLabel"),
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
            ? createControl(widget.control, prefixControls.first.id, disabled,
                parentAdaptive: widget.parentAdaptive)
            : null,
        suffix: revealPasswordIcon ??
            (suffixControls.isNotEmpty
                ? createControl(
                    widget.control, suffixControls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : null),
        readOnly: readOnly,
        textDirection: rtl ? TextDirection.rtl : null,
        inputFormatters: inputFormatters.isNotEmpty ? inputFormatters : null,
        obscureText: password && !_revealPassword,
        controller: _controller,
        focusNode: focusNode,
        onChanged: (String value) {
          //debugPrint(value);
          _value = value;
          widget.backend
              .updateControlState(widget.control.id, {"value": value});
          if (onChange) {
            widget.backend
                .triggerControlEvent(widget.control.id, "change", value);
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
  }
}
