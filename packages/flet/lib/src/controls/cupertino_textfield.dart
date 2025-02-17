import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/autofill.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/others.dart';
import '../utils/overlay_style.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';
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

class _CupertinoTextFieldControlState extends State<CupertinoTextFieldControl>
    with FletStoreMixin {
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
    widget.backend.triggerControlEvent(widget.control.id, _shiftEnterfocusNode.hasFocus ? "focus" : "blur");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
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

    TextCapitalization textCapitalization = parseTextCapitalization(
        widget.control.attrString("textCapitalization"),
        TextCapitalization.none)!;

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

    TextAlign textAlign = parseTextAlign(
        widget.control.attrString("textAlign"), TextAlign.start)!;

    double? textVerticalAlign = widget.control.attrDouble("textVerticalAlign");

    bool rtl = widget.control.attrBool("rtl", false)!;
    bool autocorrect = widget.control.attrBool("autocorrect", true)!;
    ;

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
      FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
        widget.control.attrString("border"),
        FormFieldInputBorder.outline,
      )!;

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
      revealPasswordIcon = Padding(
        padding: const EdgeInsets.only(right: 15.0),
        child: GestureDetector(
            child: Icon(
              _revealPassword ? CupertinoIcons.eye_slash : CupertinoIcons.eye,
            ),
            onTap: () {
              setState(() {
                _revealPassword = !_revealPassword;
              });
            }),
      );
    }
    var fitParentSize = widget.control.attrBool("fitParentSize", false)!;
    BoxDecoration? defaultDecoration = const CupertinoTextField().decoration;
    var gradient = parseGradient(Theme.of(context), widget.control, "gradient");
    var blendMode = parseBlendMode(widget.control.attrString("blendMode"));

    var bgColor = widget.control.attrColor("bgColor", context);

    return withPageArgs((context, pageArgs) {
      Widget textField = CupertinoTextField(
          style: textStyle,
          textAlignVertical: textVerticalAlign != null
              ? TextAlignVertical(y: textVerticalAlign)
              : null,
          placeholder: widget.control.attrString("placeholderText") ??
              widget.control.attrString("label"),
          // use label for adaptive TextField
          placeholderStyle: parseTextStyle(Theme.of(context), widget.control, "placeholderStyle") ??
              parseTextStyle(Theme.of(context), widget.control, "labelStyle"),
          // labelStyle for adaptive TextField
          autofocus: autofocus,
          enabled: !disabled,
          onSubmitted: !multiline
              ? (String value) {
                  widget.backend
                      .triggerControlEvent(widget.control.id, "submit", value);
                }
              : null,
          decoration: defaultDecoration?.copyWith(
              color: bgColor,
              gradient: gradient,
              image: parseDecorationImage(
                  Theme.of(context), widget.control, "image", pageArgs),
              backgroundBlendMode:
                  bgColor != null || gradient != null ? blendMode : null,
              border: border,
              borderRadius: borderRadius,
              boxShadow:
                  parseBoxShadow(Theme.of(context), widget.control, "shadow")),
          cursorHeight: widget.control.attrDouble("cursorHeight"),
          showCursor: widget.control.attrBool("showCursor"),
          cursorWidth: widget.control.attrDouble("cursorWidth", 2.0)!,
          cursorRadius: parseRadius(
              widget.control, "cursorRadius", const Radius.circular(2.0))!,
          keyboardType: multiline
              ? TextInputType.multiline
              : parseTextInputType(widget.control.attrString("keyboardType"),
                  TextInputType.text)!,
          clearButtonSemanticLabel:
              widget.control.attrString("clearButtonSemanticsLabel"),
          autocorrect: autocorrect,
          enableSuggestions:
              widget.control.attrBool("enableSuggestions", true)!,
          smartDashesType: widget.control.attrBool("smartDashesType", true)!
              ? SmartDashesType.enabled
              : SmartDashesType.disabled,
          smartQuotesType: widget.control.attrBool("smartQuotesType", true)!
              ? SmartQuotesType.enabled
              : SmartQuotesType.disabled,
          suffixMode: parseVisibilityMode(
              widget.control.attrString("suffixVisibilityMode"),
              OverlayVisibilityMode.always)!,
          prefixMode: parseVisibilityMode(
              widget.control.attrString("prefixVisibilityMode"),
              OverlayVisibilityMode.always)!,
          textAlign: textAlign,
          minLines: fitParentSize ? null : minLines,
          maxLines: fitParentSize ? null : maxLines,
          maxLength: maxLength,
          prefix: prefixControls.isNotEmpty
              ? createControl(widget.control, prefixControls.first.id, disabled,
                  parentAdaptive: widget.parentAdaptive)
              : null,
          suffix: revealPasswordIcon ?? (suffixControls.isNotEmpty ? createControl(widget.control, suffixControls.first.id, disabled, parentAdaptive: widget.parentAdaptive) : null),
          readOnly: readOnly,
          textDirection: rtl ? TextDirection.rtl : null,
          inputFormatters: inputFormatters.isNotEmpty ? inputFormatters : null,
          obscureText: password && !_revealPassword,
          padding: parseEdgeInsets(widget.control, "padding", const EdgeInsets.all(7.0))!,
          scribbleEnabled: widget.control.attrBool("enableScribble", true)!,
          scrollPadding: parseEdgeInsets(widget.control, "scrollPadding", const EdgeInsets.all(20.0))!,
          obscuringCharacter: widget.control.attrString("obscuringCharacter", '•')!,
          cursorOpacityAnimates: widget.control.attrBool("animateCursorOpacity", Theme.of(context).platform == TargetPlatform.iOS)!,
          expands: fitParentSize,
          enableIMEPersonalizedLearning: widget.control.attrBool("enableIMEPersonalizedLearning", true)!,
          clipBehavior: parseClip(widget.control.attrString("clipBehavior"), Clip.hardEdge)!,
          cursorColor: cursorColor,
          autofillHints: parseAutofillHints(widget.control, "autofillHints"),
          keyboardAppearance: parseBrightness(widget.control.attrString("keyboardBrightness")),
          enableInteractiveSelection: widget.control.attrBool("enableInteractiveSelection"),
          clearButtonMode: parseVisibilityMode(widget.control.attrString("clearButtonVisibilityMode"), OverlayVisibilityMode.never)!,
          strutStyle: parseStrutStyle(widget.control, "strutStyle"),
          onTap: () {
            widget.backend.triggerControlEvent(widget.control.id, "click");
          },
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
    });
  }
}
