import 'package:flet/src/utils/platform.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/autofill.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/mouse.dart';
import '../utils/others.dart';
import '../utils/overlay_style.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'cupertino_textfield.dart';
import 'flet_store_mixin.dart';

class TextFieldControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const TextFieldControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<TextFieldControl> createState() => _TextFieldControlState();
}

class _TextFieldControlState extends State<TextFieldControl>
    with FletStoreMixin {
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
    widget.backend.triggerControlEvent(
        widget.control.id, _shiftEnterfocusNode.hasFocus ? "focus" : "blur");
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
    debugPrint("TextField build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoTextFieldControl(
            control: widget.control,
            children: widget.children,
            parent: widget.parent,
            parentDisabled: widget.parentDisabled,
            parentAdaptive: adaptive,
            backend: widget.backend);
      }

      debugPrint("TextField build: ${widget.control.id}");

      String value = widget.control.attrs["value"] ?? "";
      if (_value != value) {
        _value = value;
        _controller.value = TextEditingValue(
          text: value,
          selection: TextSelection.collapsed(
              offset: value.length), // preserve cursor position at the end
        );
      }

      var prefixControls =
          widget.children.where((c) => c.name == "prefix" && c.isVisible);
      var prefixIconControls =
          widget.children.where((c) => c.name == "prefix_icon" && c.isVisible);
      var suffixControls =
          widget.children.where((c) => c.name == "suffix" && c.isVisible);
      var suffixIconControls =
          widget.children.where((c) => c.name == "suffix_icon" && c.isVisible);
      var iconControls =
          widget.children.where((c) => c.name == "icon" && c.isVisible);
      var counterControls =
          widget.children.where((c) => c.name == "counter" && c.isVisible);
      var errorCtrl =
          widget.children.where((c) => c.name == "error" && c.isVisible);
      var helperCtrl =
          widget.children.where((c) => c.name == "helper" && c.isVisible);
      var labelCtrl =
          widget.children.where((c) => c.name == "label" && c.isVisible);

      bool shiftEnter = widget.control.attrBool("shiftEnter", false)!;
      bool multiline =
          widget.control.attrBool("multiline", false)! || shiftEnter;
      int minLines = widget.control.attrInt("minLines", 1)!;
      int? maxLines = widget.control.attrInt("maxLines", multiline ? null : 1);

      bool password = widget.control.attrBool("password", false)!;
      bool canRevealPassword =
          widget.control.attrBool("canRevealPassword", false)!;
      var cursorColor = widget.control.attrColor("cursorColor", context);
      var selectionColor = widget.control.attrColor("selectionColor", context);
      var textSize = widget.control.attrDouble("textSize");
      var color = widget.control.attrColor("color", context);
      var focusedColor = widget.control.attrColor("focusedColor", context);

      TextStyle? textStyle =
          parseTextStyle(Theme.of(context), widget.control, "textStyle");
      if (textSize != null || color != null || focusedColor != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: _focused ? focusedColor ?? color : color);
      }

      TextCapitalization textCapitalization = parseTextCapitalization(
          widget.control.attrString("capitalization"),
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

      double? textVerticalAlign =
          widget.control.attrDouble("textVerticalAlign");

      FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;

      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        focusNode.requestFocus();
      }
      var fitParentSize = widget.control.attrBool("fitParentSize", false)!;

      var maxLength = widget.control.attrInt("maxLength");

      Widget textField = TextFormField(
          style: textStyle,
          autofocus: autofocus,
          enabled: !disabled,
          onFieldSubmitted: !multiline
              ? (value) {
                  widget.backend
                      .triggerControlEvent(widget.control.id, "submit", value);
                }
              : null,
          decoration: buildInputDecoration(context, widget.control,
              prefix: prefixControls.isNotEmpty ? prefixControls.first : null,
              prefixIcon: prefixIconControls.isNotEmpty
                  ? prefixIconControls.first
                  : null,
              suffix: suffixControls.isNotEmpty ? suffixControls.first : null,
              suffixIcon: suffixIconControls.isNotEmpty
                  ? suffixIconControls.first
                  : null,
              icon: iconControls.isNotEmpty ? iconControls.first : null,
              counter:
                  counterControls.isNotEmpty ? counterControls.first : null,
              error: errorCtrl.isNotEmpty ? errorCtrl.first : null,
              helper: helperCtrl.isNotEmpty ? helperCtrl.first : null,
              label: labelCtrl.isNotEmpty ? labelCtrl.first : null,
              customSuffix: revealPasswordIcon,
              valueLength: _value.length,
              maxLength: maxLength,
              focused: _focused,
              disabled: disabled,
              adaptive: adaptive),
          showCursor: widget.control.attrBool("showCursor"),
          textAlignVertical: textVerticalAlign != null
              ? TextAlignVertical(y: textVerticalAlign)
              : null,
          cursorHeight: widget.control.attrDouble("cursorHeight"),
          cursorWidth: widget.control.attrDouble("cursorWidth", 2.0)!,
          cursorRadius: parseRadius(widget.control, "cursorRadius"),
          keyboardType: multiline
              ? TextInputType.multiline
              : parseTextInputType(widget.control.attrString("keyboardType"),
                  TextInputType.text)!,
          autocorrect: widget.control.attrBool("autocorrect", true)!,
          enableSuggestions:
              widget.control.attrBool("enableSuggestions", true)!,
          smartDashesType: widget.control.attrBool("smartDashesType", true)!
              ? SmartDashesType.enabled
              : SmartDashesType.disabled,
          smartQuotesType: widget.control.attrBool("smartQuotesType", true)!
              ? SmartQuotesType.enabled
              : SmartQuotesType.disabled,
          textAlign: parseTextAlign(
              widget.control.attrString("textAlign"), TextAlign.start)!,
          minLines: fitParentSize ? null : minLines,
          maxLines: fitParentSize ? null : maxLines,
          maxLength: maxLength,
          readOnly: widget.control.attrBool("readOnly", false)!,
          inputFormatters: inputFormatters.isNotEmpty ? inputFormatters : null,
          obscureText: password && !_revealPassword,
          controller: _controller,
          focusNode: focusNode,
          autofillHints: parseAutofillHints(widget.control, "autofillHints"),
          expands: fitParentSize,
          enableInteractiveSelection:
              widget.control.attrBool("enableInteractiveSelection"),
          canRequestFocus: widget.control.attrBool("canRequestFocus", true)!,
          clipBehavior: parseClip(
              widget.control.attrString("clipBehavior"), Clip.hardEdge)!,
          cursorColor: cursorColor,
          ignorePointers: widget.control.attrBool("ignorePointers"),
          cursorErrorColor:
              widget.control.attrColor("cursorErrorColor", context),
          scribbleEnabled: widget.control.attrBool("enableScribble", true)!,
          scrollPadding: parseEdgeInsets(
              widget.control, "scrollPadding", const EdgeInsets.all(20.0))!,
          keyboardAppearance:
              parseBrightness(widget.control.attrString("keyboardBrightness")),
          enableIMEPersonalizedLearning:
              widget.control.attrBool("enableIMEPersonalizedLearning", true)!,
          obscuringCharacter:
              widget.control.attrString("obscuringCharacter", '•')!,
          mouseCursor:
              parseMouseCursor(widget.control.attrString("mouseCursor")),
          cursorOpacityAnimates: widget.control.attrBool("animateCursorOpacity",
              Theme.of(context).platform == TargetPlatform.iOS)!,
          onTapAlwaysCalled:
              widget.control.attrBool("animateCursorOpacity", false)!,
          strutStyle: parseStrutStyle(widget.control, "strutStyle"),
          onTap: () {
            widget.backend.triggerControlEvent(widget.control.id, "click");
          },
          onChanged: (String value) {
            _value = value;
            widget.backend
                .updateControlState(widget.control.id, {"value": value});
            if (widget.control.attrBool("onChange", false)!) {
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

      // linux workaround for https://github.com/flet-dev/flet/issues/3934
      textField =
          isLinuxDesktop() ? ExcludeSemantics(child: textField) : textField;

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

class CustomNumberFormatter extends TextInputFormatter {
  final String pattern;

  CustomNumberFormatter(this.pattern);

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    final regExp = RegExp(pattern);
    if (regExp.hasMatch(newValue.text)) {
      return newValue;
    }
    // If newValue is invalid, keep the old value
    return oldValue;
  }
}
