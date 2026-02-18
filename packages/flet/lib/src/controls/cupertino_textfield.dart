import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/autofill.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/gradient.dart';
import '../utils/images.dart';
import '../utils/layout.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import '../utils/theme.dart';
import 'base_controls.dart';

class CupertinoTextFieldControl extends StatefulWidget {
  final Control control;

  CupertinoTextFieldControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

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
  String? _lastBlurValue;
  TextSelection? _selection;

  KeyEventResult _handleTextFieldKeyEvent(KeyEvent event,
      {required bool submitOnEnter}) {
    // ignore up/down arrow keys if flag is set
    if ((event is KeyDownEvent || event is KeyRepeatEvent) &&
        widget.control.getBool("ignore_up_down_keys", false)! &&
        (event.logicalKey == LogicalKeyboardKey.arrowUp ||
            event.logicalKey == LogicalKeyboardKey.arrowDown)) {
      return KeyEventResult.handled;
    }

    // submit on Enter if flag is set and shift is not pressed
    if (submitOnEnter &&
        event is KeyDownEvent &&
        !HardwareKeyboard.instance.isShiftPressed &&
        (event.logicalKey == LogicalKeyboardKey.enter ||
            event.logicalKey == LogicalKeyboardKey.numpadEnter)) {
      widget.control.triggerEvent("submit");
      return KeyEventResult.handled;
    }

    // let the system handle other key events
    return KeyEventResult.ignored;
  }

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _controller.addListener(_handleControllerChange);
    _shiftEnterfocusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent event) =>
          _handleTextFieldKeyEvent(event, submitOnEnter: true),
    );
    _shiftEnterfocusNode.addListener(_onShiftEnterFocusChange);
    _focusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent event) =>
          _handleTextFieldKeyEvent(event, submitOnEnter: false),
    );
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    _controller.removeListener(_handleControllerChange);
    _controller.dispose();
    _shiftEnterfocusNode.removeListener(_onShiftEnterFocusChange);
    _shiftEnterfocusNode.dispose();
    _focusNode.removeListener(_onFocusChange);
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _focusNode.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("CupertinoTextField.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown CupertinoTextField method: $name");
    }
  }

  void _onShiftEnterFocusChange() {
    setState(() {
      _focused = _shiftEnterfocusNode.hasFocus;
    });
    widget.control
        .triggerEvent(_shiftEnterfocusNode.hasFocus ? "focus" : "blur");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  void _handleControllerChange() {
    final selection = _controller.selection;
    if (_selection == selection) return;

    _selection = selection;

    if (!selection.isValid ||
        !widget.control.getBool("on_selection_change", false)!) {
      return;
    }

    widget.control.updateProperties({"selection": selection.toMap()});
    widget.control.triggerEvent("selection_change", {
      "selected_text":
          _controller.text.substring(selection.start, selection.end),
      "selection": selection.toMap()
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoTextField build: ${widget.control.id}");

    var autofocus = widget.control.getBool("autofocus", false)!;
    var value = widget.control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        // preserve cursor position at the end
        selection: TextSelection.collapsed(offset: value.length),
      );
      _selection = _controller.selection;
    }

    var shiftEnter = widget.control.getBool("shift_enter", false)!;
    var multiline = widget.control.getBool("multiline", false)! || shiftEnter;
    var minLines = widget.control.getInt("min_lines", 1)!;
    var maxLines = widget.control.getInt("max_lines", multiline ? null : 1);

    var readOnly = widget.control.getBool("read_only", false)!;
    var password = widget.control.getBool("password", false)!;
    var onChange = widget.control.getBool("on_change", false)!;

    var cursorColor = widget.control.getColor("cursor_color", context);
    var selectionColor = widget.control.getColor("selection_color", context);

    var maxLength = widget.control.getInt("max_length");

    var textSize = widget.control.getDouble("text_size");

    var color = widget.control.getColor("color", context);
    var focusedColor = widget.control.getColor("focused_color", context);

    var textStyle =
        widget.control.getTextStyle("text_style", Theme.of(context));
    if (textSize != null || color != null || focusedColor != null) {
      textStyle = (textStyle ?? const TextStyle()).copyWith(
          fontSize: textSize, color: _focused ? focusedColor ?? color : color);
    }

    List<TextInputFormatter> inputFormatters = [];
    var inputFilter = widget.control.getTextInputFormatter("input_filter");
    if (inputFilter != null) {
      inputFormatters.add(inputFilter);
    }
    var textCapitalization = widget.control
        .getTextCapitalization("capitalization", TextCapitalization.none)!;
    if (textCapitalization != TextCapitalization.none) {
      inputFormatters.add(TextCapitalizationFormatter(textCapitalization));
    }
    var textAlign = widget.control.getTextAlign("text_align", TextAlign.start)!;
    var textVerticalAlign = widget.control.getDouble("text_vertical_align");
    var rtl = widget.control.getBool("rtl", false)!;
    var autocorrect = widget.control.getBool("autocorrect", true)!;
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

    var selection = widget.control.getTextSelection("selection",
        minOffset: 0, maxOffset: _controller.text.length);
    if (selection != null && selection != _controller.selection) {
      _controller.selection = selection;
      _selection = selection;
    }

    var borderRadius = widget.control.getBorderRadius("border_radius");

    BoxBorder? border;
    var borderWidth = widget.control.getDouble("border_width", 1.0)!;
    var borderColor = widget.control.getColor("border_color", context) ??
        const Color(0xFF000000);

    try {
      border = widget.control.getBorder("border", Theme.of(context));
      // adaptive TextField is being created
    } catch (e) {
      FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
        widget.control.getString("border"),
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

    var canRevealPassword =
        widget.control.getBool("can_reveal_password", false)!;

    Widget? revealPasswordIcon;
    if (password && canRevealPassword) {
      revealPasswordIcon = Padding(
        padding: const EdgeInsets.only(right: 15.0),
        child: GestureDetector(
            child: Icon(_revealPassword
                ? CupertinoIcons.eye_slash
                : CupertinoIcons.eye),
            onTap: () {
              setState(() {
                _revealPassword = !_revealPassword;
              });
            }),
      );
    }
    var fitParentSize = widget.control.getBool("fit_parent_size", false)!;
    var defaultDecoration = const CupertinoTextField().decoration;
    var gradient = widget.control.getGradient("gradient", Theme.of(context));
    var blendMode = widget.control.getBlendMode("blend_mode");
    var bgcolor = widget.control.getColor("bgcolor", context);
    var label = widget.control.get("label");
    String? labelStr;
    if (label is String) {
      labelStr = widget.control.getString("label");
    }

    Widget textField = CupertinoTextField(
        style: textStyle,
        textAlignVertical: textVerticalAlign != null
            ? TextAlignVertical(y: textVerticalAlign)
            : null,
        placeholder: widget.control.getString("placeholder_text") ?? labelStr,
        placeholderStyle:
            widget.control.getTextStyle("placeholder_style", Theme.of(context)) ??
                widget.control.getTextStyle("label_style", Theme.of(context)),
        // label_style for adaptive TextField
        autofocus: autofocus,
        enabled: !widget.control.disabled,
        onSubmitted: !multiline
            ? (String value) {
                widget.control.triggerEvent("submit", value);
              }
            : null,
        decoration: defaultDecoration?.copyWith(
            color: bgcolor,
            gradient: gradient,
            image: widget.control.getDecorationImage("image", context),
            backgroundBlendMode:
                bgcolor != null || gradient != null ? blendMode : null,
            border: border,
            borderRadius: borderRadius,
            boxShadow:
                widget.control.getBoxShadows("shadow", Theme.of(context))),
        cursorHeight: widget.control.getDouble("cursor_height"),
        showCursor: widget.control.getBool("show_cursor"),
        cursorWidth: widget.control.getDouble("cursor_width", 2.0)!,
        cursorRadius: widget.control
            .getRadius("cursor_radius", const Radius.circular(2.0))!,
        keyboardType: multiline
            ? TextInputType.multiline
            : widget.control
                .getTextInputType("keyboard_type", TextInputType.text)!,
        clearButtonSemanticLabel:
            widget.control.getString("clear_button_semantics_label"),
        autocorrect: autocorrect,
        enableSuggestions: widget.control.getBool("enable_suggestions", true)!,
        smartDashesType: widget.control.getBool("smart_dashes_type", true)!
            ? SmartDashesType.enabled
            : SmartDashesType.disabled,
        smartQuotesType: widget.control.getBool("smart_quotes_type", true)!
            ? SmartQuotesType.enabled
            : SmartQuotesType.disabled,
        suffixMode: widget.control.getOverlayVisibilityMode(
            "suffix_visibility_mode", OverlayVisibilityMode.always)!,
        prefixMode: widget.control.getOverlayVisibilityMode(
            "prefix_visibility_mode", OverlayVisibilityMode.always)!,
        textAlign: textAlign,
        minLines: fitParentSize ? null : minLines,
        maxLines: fitParentSize ? null : maxLines,
        maxLength: maxLength,
        prefix: widget.control.buildTextOrWidget("prefix"),
        suffix:
            revealPasswordIcon ?? widget.control.buildTextOrWidget("suffix"),
        readOnly: readOnly,
        textDirection: rtl ? TextDirection.rtl : null,
        inputFormatters: inputFormatters.isNotEmpty ? inputFormatters : null,
        obscureText: password && !_revealPassword,
        padding:
            widget.control.getPadding("padding", const EdgeInsets.all(7.0))!,
        stylusHandwritingEnabled:
            widget.control.getBool("enable_stylus_handwriting", true)!,
        scrollPadding: widget.control
            .getPadding("scroll_padding", const EdgeInsets.all(20.0))!,
        obscuringCharacter:
            widget.control.getString("obscuring_character", '•')!,
        cursorOpacityAnimates:
            widget.control.getBool("animate_cursor_opacity", isIOSMobile())!,
        expands: fitParentSize,
        enableIMEPersonalizedLearning:
            widget.control.getBool("enable_ime_personalized_learning", true)!,
        clipBehavior:
            widget.control.getClipBehavior("clip_behavior", Clip.hardEdge)!,
        cursorColor: cursorColor,
        autofillHints: parseAutofillHints(widget.control.get("autofill_hints")),
        keyboardAppearance: widget.control.getBrightness("keyboard_brightness"),
        enableInteractiveSelection:
            widget.control.getBool("enable_interactive_selection"),
        clearButtonMode: widget.control.getOverlayVisibilityMode("clear_button_visibility_mode", OverlayVisibilityMode.never)!,
        strutStyle: widget.control.getStrutStyle("strut_style"),
        onTap: () => widget.control.triggerEvent("click"),
        controller: _controller,
        focusNode: focusNode,
        onTapOutside: widget.control.getBool("on_tap_outside", false)!
            ? (PointerDownEvent? event) {
                widget.control.triggerEvent("tap_outside");
              }
            : null,
        onChanged: (String value) {
          _value = value;
          widget.control.updateProperties({"value": value});
          if (onChange) {
            widget.control.triggerEvent("change", value);
          }
        });

    if (cursorColor != null || selectionColor != null) {
      textField = TextSelectionTheme(
          data: TextSelectionTheme.of(context).copyWith(
              cursorColor: cursorColor, selectionColor: selectionColor),
          child: textField);
    }

    if (widget.control.getExpand("expand", 0)! > 0) {
      return LayoutControl(control: widget.control, child: textField);
    } else {
      double? width = widget.control.getDouble("width");

      return LayoutControl(
        control: widget.control,
        child: width == null
            ? ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 300),
                child: textField)
            : textField,
      );
    }
  }
}
