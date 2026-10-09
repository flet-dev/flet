import 'package:flutter/foundation.dart';
import 'package:material_ui/material_ui.dart';
import 'package:flutter/services.dart';
import 'package:pasteboard/pasteboard.dart';

import '../models/control.dart';
import '../utils/autofill.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/layout.dart';
import '../utils/misc.dart';
import '../utils/mouse.dart';
import '../utils/numbers.dart';
import '../utils/paste_files_web.dart'
    if (dart.library.io) '../utils/paste_files_non_web.dart';
import '../utils/platform.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import '../utils/theme.dart';
import 'base_controls.dart';

class TextFieldControl extends StatefulWidget {
  final Control control;

  TextFieldControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

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
  TextSelection? _selection;
  void Function()? _stopPasteListener;

  KeyEventResult _handleTextFieldKeyEvent(KeyEvent event,
      {required bool submitOnEnter}) {
    // ignore up/down arrow keys if flag is set
    if ((event is KeyDownEvent || event is KeyRepeatEvent) &&
        widget.control.getBool("ignore_up_down_keys", false)! &&
        (event.logicalKey == LogicalKeyboardKey.arrowUp ||
            event.logicalKey == LogicalKeyboardKey.arrowDown)) {
      return KeyEventResult.handled;
    }

    // Ctrl/Cmd+V: report a clipboard image to `on_paste_files` (native;
    // the web gets pasted files from the browser's paste event instead).
    // The key still pastes text as usual.
    if (!kIsWeb &&
        event is KeyDownEvent &&
        event.logicalKey == LogicalKeyboardKey.keyV &&
        (HardwareKeyboard.instance.isMetaPressed ||
            HardwareKeyboard.instance.isControlPressed) &&
        widget.control.hasEventHandler("paste_files")) {
      _pasteClipboardImage();
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
    _stopPasteListener?.call();
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

  void _sendPastedFiles(List<PastedFile> files) {
    if (files.isEmpty || !widget.control.hasEventHandler("paste_files")) {
      return;
    }
    widget.control.triggerEvent("paste_files", {
      "files": files
          .map((f) =>
              {"name": f.name, "mime_type": f.mimeType, "bytes": f.bytes})
          .toList()
    });
  }

  Future<void> _pasteClipboardImage() async {
    try {
      final image = await Pasteboard.image;
      if (image != null && image.isNotEmpty) {
        _sendPastedFiles(
            [(name: "image.png", mimeType: "image/png", bytes: image)]);
      }
    } catch (e) {
      debugPrint("TextField: can't read a clipboard image: $e");
    }
  }

  /// Web: listen to paste events only while focused and handled, so other
  /// fields (and the rest of the page) keep the browser's default paste.
  void _updatePasteListener(bool focused) {
    _stopPasteListener?.call();
    _stopPasteListener = null;
    if (kIsWeb && focused && widget.control.hasEventHandler("paste_files")) {
      _stopPasteListener = listenPastedFiles(_sendPastedFiles);
    }
  }

  void _onShiftEnterFocusChange() {
    _focused = _shiftEnterfocusNode.hasFocus;
    _updatePasteListener(_focused);
    widget.control
        .triggerEvent(_shiftEnterfocusNode.hasFocus ? "focus" : "blur");
  }

  void _onFocusChange() {
    _focused = _focusNode.hasFocus;
    _updatePasteListener(_focused);
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  void _handleControllerChange() {
    final selection = _controller.selection;
    if (_selection == selection) return;

    _selection = selection;

    if (!selection.isValid ||
        !widget.control.hasEventHandler("selection_change")) {
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
    debugPrint("TextField build: ${widget.control.id}");

    bool autofocus = widget.control.getBool("autofocus", false)!;

    String value = widget.control.getString("value", "")!;
    if (_value != value) {
      _value = value;
      _controller.value = TextEditingValue(
        text: value,
        // preserve cursor position at the end
        selection: TextSelection.collapsed(offset: value.length),
      );
      _selection = _controller.selection;
    }

    var selection = widget.control.getTextSelection("selection",
        minOffset: 0, maxOffset: _controller.text.length);
    if (selection != null && selection != _controller.selection) {
      _controller.selection = selection;
      _selection = selection;
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
    // `Theme.text_field_theme.text_style` under the field's own style.
    var themeTextStyle =
        Theme.of(context).extension<TextFieldTheme>()?.textStyle;
    if (themeTextStyle != null) {
      textStyle = themeTextStyle.merge(textStyle);
    }
    if (textSize != null || color != null || focusedColor != null) {
      textStyle = textStyle.copyWith(
          fontSize: textSize, color: _focused ? focusedColor ?? color : color);
    }

    TextCapitalization textCapitalization = widget.control
        .getTextCapitalization("capitalization", TextCapitalization.none)!;

    FilteringTextInputFormatter? inputFilter =
        widget.control.getTextInputFormatter("input_filter");

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
        stylusHandwritingEnabled:
            widget.control.getBool("enable_stylus_handwriting", true)!,
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
        onTapOutside: widget.control.hasEventHandler("tap_outside")
            ? (PointerDownEvent? event) {
                widget.control.triggerEvent("tap_outside");
              }
            : null,
        onChanged: (String value) {
          _value = value;
          widget.control.updateProperties({"value": value});
          if (widget.control.hasEventHandler("change")) {
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
