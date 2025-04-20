import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class TextFieldControl extends StatefulWidget {
  final Control control;

  const TextFieldControl({
    super.key,
    required this.control,
  });

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
  String? _lastFocusValue;
  String? _lastBlurValue;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent evt) {
        if (!HardwareKeyboard.instance.isShiftPressed &&
            evt.logicalKey.keyLabel == 'Enter') {
          if (evt is KeyDownEvent) {
            widget.control.triggerEvent("submit");
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
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _controller.dispose();
    _shiftEnterfocusNode.removeListener(_onShiftEnterFocusChange);
    _shiftEnterfocusNode.dispose();
    _focusNode.removeListener(_onFocusChange);
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("TextField.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown TextField method: $name");
    }
  }

  void _onShiftEnterFocusChange() {
    _focused = _shiftEnterfocusNode.hasFocus;
    widget.control
        .triggerEvent(_shiftEnterfocusNode.hasFocus ? "focus" : "blur");
  }

  void _onFocusChange() {
    _focused = _focusNode.hasFocus;
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("TextField build: ${widget.control.id}");

    bool autofocus = widget.control.getBool("autofocus", false)!;

    String value = widget.control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(
            offset: value.length), // preserve cursor position at the end
      );
    }

    var shiftEnter = widget.control.getBool("shift_enter", false)!;
    var multiline = widget.control.getBool("multiline", false)! || shiftEnter;
    var minLines = widget.control.getInt("min_lines", 1)!;
    var maxLines = widget.control.getInt("max_lines", multiline ? null : 1);

    var password = widget.control.getBool("password", false)!;
    var canRevealPassword =
        widget.control.getBool("can_reveal_password", false)!;
    var cursorColor = widget.control.getColor("cursor_color", context);
    var selectionColor = widget.control.getColor("selection_color", context);
    var textSize = widget.control.getDouble("text_size");
    var color = widget.control.getColor("color", context);
    var focusedColor = widget.control.getColor("focused_color", context);
    var textStyle = widget.control
        .getTextStyle("text_style", Theme.of(context), const TextStyle())!;
    if (textSize != null || color != null || focusedColor != null) {
      textStyle = textStyle.copyWith(
          fontSize: textSize, color: _focused ? focusedColor ?? color : color);
    }

    TextCapitalization textCapitalization = widget.control
        .getTextCapitalization("capitalization", TextCapitalization.none)!;

    FilteringTextInputFormatter? inputFilter =
        parseInputFilter(widget.control.get("input_filter"));

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

    var textVerticalAlign = widget.control.getDouble("text_vertical_align");

    FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;

    var focusValue = widget.control.getString("focus");
    var blurValue = widget.control.getString("blur");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      focusNode.requestFocus();
    }
    if (blurValue != null && blurValue != _lastBlurValue) {
      _lastBlurValue = blurValue;
      _focusNode.unfocus();
    }

    var fitParentSize = widget.control.getBool("fit_parent_size", false)!;

    var maxLength = widget.control.getInt("max_length");

    Widget textField = TextFormField(
        style: textStyle,
        autofocus: autofocus,
        enabled: !widget.control.disabled,
        onFieldSubmitted: !multiline
            ? (value) {
                widget.control.triggerEvent("submit", value);
              }
            : null,
        decoration: buildInputDecoration(
          context,
          widget.control,
          customSuffix: revealPasswordIcon,
          valueLength: _value.length,
          maxLength: maxLength,
          focused: _focused,
        ),
        showCursor: widget.control.getBool("show_cursor"),
        textAlignVertical: textVerticalAlign != null
            ? TextAlignVertical(y: textVerticalAlign)
            : null,
        cursorHeight: widget.control.getDouble("cursor_height"),
        cursorWidth: widget.control.getDouble("cursor_width", 2.0)!,
        cursorRadius: widget.control.getRadius("cursor_radius"),
        keyboardType: multiline
            ? TextInputType.multiline
            : widget.control
                .getTextInputType("keyboard_type", TextInputType.text)!,
        autocorrect: widget.control.getBool("autocorrect", true)!,
        enableSuggestions: widget.control.getBool("enable_suggestions", true)!,
        smartDashesType: widget.control.getBool("smart_dashes_type", true)!
            ? SmartDashesType.enabled
            : SmartDashesType.disabled,
        smartQuotesType: widget.control.getBool("smart_quotes_type", true)!
            ? SmartQuotesType.enabled
            : SmartQuotesType.disabled,
        textAlign: widget.control.getTextAlign("text_align", TextAlign.start)!,
        minLines: fitParentSize ? null : minLines,
        maxLines: fitParentSize ? null : maxLines,
        maxLength: maxLength,
        readOnly: widget.control.getBool("read_only", false)!,
        inputFormatters: inputFormatters.isNotEmpty ? inputFormatters : null,
        obscureText: password && !_revealPassword,
        controller: _controller,
        focusNode: focusNode,
        autofillHints: widget.control.getAutofillHints("autofill_hints"),
        expands: fitParentSize,
        enableInteractiveSelection:
            widget.control.getBool("enable_interactive_selection"),
        canRequestFocus: widget.control.getBool("can_request_focus", true)!,
        clipBehavior:
            widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
        cursorColor: cursorColor,
        ignorePointers: widget.control.getBool("ignore_pointers"),
        cursorErrorColor:
            widget.control.getColor("cursor_error_color", context),
        stylusHandwritingEnabled: widget.control
                .getBool("enable_stylus_handwriting") ??
            widget.control.getBool(
                "enable_scribble") ?? // todo(0.73.0): remove enable_scribble
            true,
        scrollPadding: widget.control
            .getPadding("scroll_padding", const EdgeInsets.all(20.0))!,
        keyboardAppearance: widget.control.getBrightness("keyboard_brightness"),
        enableIMEPersonalizedLearning:
            widget.control.getBool("enable_ime_personalized_learning", true)!,
        obscuringCharacter:
            widget.control.getString("obscuring_character", '•')!,
        mouseCursor: widget.control.getMouseCursor("mouse_cursor"),
        cursorOpacityAnimates: widget.control.getBool("animate_cursor_opacity",
            Theme.of(context).platform == TargetPlatform.iOS)!,
        onTapAlwaysCalled: widget.control.getBool("always_call_on_tap", false)!,
        strutStyle: widget.control.getStrutStyle("strut_style"),
        onTap: () {
          widget.control.triggerEvent("click");
        },
        onTapOutside: widget.control.getBool("on_tap_outside", false)!
            ? (PointerDownEvent? event) {
                widget.control.triggerEvent("tap_outside");
              }
            : null,
        onChanged: (String value) {
          _value = value;
          widget.control.updateProperties({"value": value});
          if (widget.control.getBool("on_change", false)!) {
            widget.control.triggerEvent("change", value);
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

    if (widget.control.get("expand") == true ||
        (widget.control.get("expand") is int &&
            widget.control.getInt("expand", 0)! > 0)) {
      return ConstrainedControl(
        control: widget.control,
        child: textField,
      );
    } else {
      return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          if (constraints.maxWidth == double.infinity &&
              widget.control.getDouble("width") == null) {
            textField = ConstrainedBox(
              constraints: const BoxConstraints.tightFor(width: 300),
              child: textField,
            );
          }

          return ConstrainedControl(control: widget.control, child: textField);
        },
      );
    }
    //});
  }
}
