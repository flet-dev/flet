import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/layout.dart';
import '../utils/menu.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'base_controls.dart';

class DropdownControl extends StatefulWidget {
  final Control control;

  DropdownControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

  @override
  State<DropdownControl> createState() => _DropdownControlState();
}

class _DropdownControlState extends State<DropdownControl> {
  late final FocusNode _focusNode;
  late final TextEditingController _controller;
  String? _value;
  bool _suppressTextChange = false;

  @override
  void initState() {
    super.initState();

    // initialize controller
    _value = widget.control.getString("value");
    final text = widget.control.getString("text") ?? _value ?? "";
    _controller = TextEditingController(text: text);
    _controller.addListener(_onTextChange);

    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  void _onTextChange() {
    if (_suppressTextChange) return;

    if (_controller.text != widget.control.getString("text")) {
      widget.control.updateProperties({"text": _controller.text});
      widget.control.triggerEvent("text_change", _controller.text);
    }
  }

  void _onFocusChange() {
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  /// Updates text without triggering a text change event.
  void _updateControllerText(String text) {
    _suppressTextChange = true;
    _controller.value = TextEditingValue(
      text: text,
      selection: TextSelection.collapsed(offset: text.length),
    );
    _suppressTextChange = false;
    widget.control.updateProperties({"text": text}, python: false);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _controller.dispose();
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Dropdown.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown Dropdown method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("DropdownMenu build: ${widget.control.id}");

    var theme = Theme.of(context);
    var editable = widget.control.getBool("editable", false)!;
    var autofocus = widget.control.getBool("autofocus", false)!;
    var textSize = widget.control.getDouble("text_size");
    var color = widget.control.getColor("color", context);

    var textAlign = widget.control.getTextAlign("text_align", TextAlign.start)!;

    var fillColor = widget.control.getColor("fill_color", context);
    var borderColor = widget.control.getColor("border_color", context);

    var borderRadius = widget.control.getBorderRadius("border_radius");
    var focusedBorderColor =
        widget.control.getColor("focused_border_color", context);
    var borderWidth = widget.control.getDouble("border_width");
    var focusedBorderWidth = widget.control.getDouble("focused_border_width");
    var menuWidth = widget.control.getDouble("menu_width");
    var bgColor = widget.control.getWidgetStateColor("bgcolor", theme);
    var elevation = widget.control.getWidgetStateDouble("elevation");

    var inputBorder = widget.control
        .getFormFieldInputBorder("border", FormFieldInputBorder.outline)!;

    InputBorder? border;

    if (inputBorder == FormFieldInputBorder.underline) {
      border = UnderlineInputBorder(
          borderSide: BorderSide(
              color: borderColor ?? const Color(0xFF000000),
              width: borderWidth ?? 1.0));
    } else if (inputBorder == FormFieldInputBorder.none) {
      border = InputBorder.none;
    } else if (inputBorder == FormFieldInputBorder.outline ||
        borderRadius != null ||
        borderColor != null ||
        borderWidth != null) {
      border = OutlineInputBorder(
          borderSide: BorderSide(
              color: borderColor ?? const Color(0xFF000000),
              width: borderWidth ?? 1.0));
      if (borderRadius != null) {
        border =
            (border as OutlineInputBorder).copyWith(borderRadius: borderRadius);
      }
      if (borderColor != null || borderWidth != null) {
        border = (border as OutlineInputBorder).copyWith(
            borderSide: borderWidth == 0
                ? BorderSide.none
                : BorderSide(
                    color: borderColor ??
                        theme.colorScheme.onSurface.withValues(alpha: 0.38),
                    width: borderWidth ?? 1.0));
      }
    }

    InputBorder? focusedBorder;
    if (borderColor != null ||
        borderWidth != null ||
        focusedBorderColor != null ||
        focusedBorderWidth != null) {
      focusedBorder = border?.copyWith(
          borderSide: borderWidth == 0
              ? BorderSide.none
              : BorderSide(
                  color: focusedBorderColor ??
                      borderColor ??
                      theme.colorScheme.primary,
                  width: focusedBorderWidth ?? borderWidth ?? 2.0));
    }

    InputDecorationTheme inputDecorationTheme = InputDecorationTheme(
      filled: widget.control.getBool("filled", false)!,
      fillColor: fillColor,
      hintStyle: widget.control.getTextStyle("hint_style", theme),
      errorStyle: widget.control.getTextStyle("error_style", theme),
      helperStyle: widget.control.getTextStyle("helper_style", theme),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      isDense: widget.control.getBool("dense", false)!,
      contentPadding: widget.control.getPadding("content_padding"),
    );

    TextStyle? textStyle = widget.control.getTextStyle("text_style", theme);
    if (textSize != null || color != null) {
      textStyle =
          (textStyle ?? theme.dropdownMenuTheme.textStyle ?? const TextStyle())
              .copyWith(
                  fontSize: textSize,
                  color: color ?? theme.colorScheme.onSurface);
    }

    MenuStyle? menuStyle = widget.control.getMenuStyle("menu_style", theme);
    if (bgColor != null || elevation != null || menuWidth != null) {
      menuStyle =
          (menuStyle ?? theme.dropdownMenuTheme.menuStyle ?? const MenuStyle())
              .copyWith(
                  backgroundColor: bgColor,
                  elevation: elevation,
                  fixedSize: WidgetStateProperty.all(
                      Size.fromWidth(menuWidth ?? double.infinity)));
    }

    if (textSize != null || color != null) {
      textStyle =
          (textStyle ?? theme.dropdownMenuTheme.textStyle ?? const TextStyle())
              .copyWith(
                  fontSize: textSize,
                  color: color ?? theme.colorScheme.onSurface);
    }

    // build dropdown items
    var options = widget.control
        .children("options")
        .map<DropdownMenuEntry<String>?>((Control itemCtrl) {
          bool itemDisabled = widget.control.disabled || itemCtrl.disabled;
          ButtonStyle? style = itemCtrl.getButtonStyle("style", theme);

          var optionKey = itemCtrl.getString("key");
          var optionText = itemCtrl.getString("text");

          var optionValue = optionKey ?? optionText;
          var optionLabel = optionText ?? optionKey;
          if (optionValue == null || optionLabel == null) {
            return null;
          }

          return DropdownMenuEntry<String>(
            enabled: !itemDisabled,
            value: optionValue,
            label: optionLabel,
            labelWidget: itemCtrl.buildWidget("content"),
            leadingIcon: itemCtrl.buildIconOrWidget("leading_icon"),
            trailingIcon: itemCtrl.buildIconOrWidget("trailing_icon"),
            style: style,
          );
        })
        .nonNulls
        .toList();

    var value = widget.control.getString("value");
    var selectedOption = options.firstWhereOrNull((o) => o.value == value);
    value = selectedOption?.value;

    // keep controller text in sync with backend-driven value changes
    if (_value != value) {
      if (value == null) {
        if (_value != null && _controller.text.isNotEmpty) {
          // clears dropdown field
          _updateControllerText("");
        }
      } else {
        final String entryLabel =
            selectedOption?.label ?? widget.control.getString("text") ?? value;
        if (_controller.text != entryLabel) {
          _updateControllerText(entryLabel);
        }
      }
      _value = value;
    }

    TextCapitalization textCapitalization = widget.control
        .getTextCapitalization("capitalization", TextCapitalization.none)!;
    FilteringTextInputFormatter? inputFilter =
        widget.control.getTextInputFormatter("input_filter");

    List<TextInputFormatter>? inputFormatters = [];
    if (inputFilter != null) {
      inputFormatters.add(inputFilter);
    }
    if (textCapitalization != TextCapitalization.none) {
      inputFormatters.add(TextCapitalizationFormatter(textCapitalization));
    }

    _focusNode.canRequestFocus = editable;

    int expand = widget.control.getExpand("expand", 0)!;
    EdgeInsets? expandedInsets = expand > 0 ? EdgeInsets.zero : null;

    Widget dropDown = DropdownMenu<String>(
      enabled: !widget.control.disabled,
      focusNode: _focusNode,
      controller: _controller,
      initialSelection: value,
      enableFilter: widget.control.getBool("enable_filter", false)!,
      enableSearch: widget.control.getBool("enable_search", true)!,
      menuHeight: widget.control.getDouble("menu_height"),
      label: widget.control.buildTextOrWidget("label",
          textStyle: widget.control.getTextStyle("label_style", theme)),
      leadingIcon: widget.control.buildIconOrWidget("leading_icon"),
      trailingIcon: widget.control.buildIconOrWidget("trailing_icon"),
      selectedTrailingIcon:
          widget.control.buildIconOrWidget("selected_trailing_icon"),
      textStyle: textStyle,
      textAlign: textAlign,
      width: widget.control.getDouble("width"),
      errorText: widget.control.getString("error_text"),
      hintText: widget.control.getString("hint_text"),
      helperText: widget.control.getString("helper_text"),
      menuStyle: menuStyle,
      expandedInsets: expandedInsets,
      inputDecorationTheme: inputDecorationTheme,
      inputFormatters: inputFormatters.isEmpty ? null : inputFormatters,
      onSelected: widget.control.disabled
          ? null
          : (String? selection) {
              _value = selection;
              widget.control.updateProperties({"value": selection});
              widget.control.triggerEvent("select", selection);
            },
      dropdownMenuEntries: options,
    );

    var didAutoFocus = false;
    if (!didAutoFocus && autofocus) {
      didAutoFocus = true;
      SchedulerBinding.instance.addPostFrameCallback((_) {
        FocusScope.of(context).autofocus(_focusNode);
      });
    }

    return LayoutControl(control: widget.control, child: dropDown);
  }
}
