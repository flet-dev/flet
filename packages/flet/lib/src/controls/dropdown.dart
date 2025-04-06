import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

import '../extensions/control.dart';
import '../flet_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'base_controls.dart';
import 'control_widget.dart';

class DropdownControl extends StatefulWidget {
  final Control control;

  const DropdownControl({
    super.key,
    required this.control,
  });

  @override
  State<DropdownControl> createState() => _DropdownControlState();
}

class _DropdownControlState extends State<DropdownControl> {
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  void _onFocusChange() {
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
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
    bool editable = widget.control.getBool("editable", false)!;
    bool autofocus = widget.control.getBool("autofocus", false)!;
    var textSize = widget.control.getDouble("text_size");
    var label = widget.control.get("label");
    var trailingIcon = widget.control.get("trailing_icon");
    var leadingIcon = widget.control.get("leading_icon");
    var selectIcon = widget.control.get("select_icon");
    var selectedTrailingIcon = widget.control.get("selected_trailing_icon");
    var prefixIcon = widget.control.get("prefix_icon");
    var color = widget.control.getColor("color", context);

    TextAlign textAlign = parseTextAlign(
        widget.control.getString("text_align"), TextAlign.start)!;

    var fillColor = widget.control.getColor("fill_color", context);
    var borderColor = widget.control.getColor("border_color", context);

    var borderRadius = parseBorderRadius(widget.control.get("border_radius"));
    var focusedBorderColor =
        widget.control.getColor("focused_border_color", context);
    var borderWidth = widget.control.getDouble("border_width");
    var focusedBorderWidth = widget.control.getDouble("focused_border_width");
    var menuWidth = widget.control.getDouble("menu_width", double.infinity)!;

    FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
      widget.control.getString("border"),
      FormFieldInputBorder.outline,
    )!;

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
                        theme.colorScheme.onSurface.withOpacity(0.38),
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
      hintStyle: parseTextStyle(widget.control.get("hint_style"), theme),
      errorStyle: parseTextStyle(widget.control.get("error_style"), theme),
      helperStyle: parseTextStyle(widget.control.get("helper_style"), theme),
      border: border,
      enabledBorder: border,
      focusedBorder: focusedBorder,
      isDense: widget.control.getBool("dense", false)!,
      contentPadding: parseEdgeInsets(widget.control.get("content_padding")),
    );

    TextStyle? textStyle =
        parseTextStyle(widget.control.get("text_style"), theme);
    if (textSize != null || color != null) {
      textStyle = (textStyle ?? const TextStyle()).copyWith(
          fontSize: textSize, color: color ?? theme.colorScheme.onSurface);
    }

    var items = widget.control
        .children("options")
        .map<DropdownMenuEntry<String>>((Control itemCtrl) {
      bool itemDisabled = widget.control.disabled || itemCtrl.disabled;
      ButtonStyle? style = parseButtonStyle(itemCtrl.get("style"), theme);

      var contentCtrl = itemCtrl.child("content");
      var leadingIcon = itemCtrl.get("leading_icon");
      var trailingIcon = itemCtrl.get("trailing_icon");

      return DropdownMenuEntry<String>(
        enabled: !itemDisabled,
        value: itemCtrl.getString("key") ??
            itemCtrl.getString("text") ??
            itemCtrl.id.toString(),
        label: itemCtrl.getString("text") ??
            itemCtrl.getString("key") ??
            itemCtrl.id.toString(),
        labelWidget:
            contentCtrl is Control ? ControlWidget(control: contentCtrl) : null,
        leadingIcon: leadingIcon is Control
            ? ControlWidget(control: leadingIcon)
            : leadingIcon is String
                ? Icon(parseIcon(leadingIcon))
                : null,
        trailingIcon: trailingIcon is Control
            ? ControlWidget(control: trailingIcon)
            : trailingIcon is String
                ? Icon(parseIcon(trailingIcon))
                : null,
        style: style,
      );
    }).toList();

    String? value = widget.control.getString("value");
    if (items.where((item) => item.value == value).isEmpty) {
      value = null;
    }

    TextCapitalization textCapitalization = parseTextCapitalization(
        widget.control.getString("capitalization"), TextCapitalization.none)!;

    FilteringTextInputFormatter? inputFilter =
        parseInputFilter(widget.control.get("input_filter"));

    List<TextInputFormatter>? inputFormatters = [];
    if (inputFilter != null) {
      inputFormatters.add(inputFilter);
    }
    if (textCapitalization != TextCapitalization.none) {
      inputFormatters.add(TextCapitalizationFormatter(textCapitalization));
    }

    _focusNode.canRequestFocus = editable;

    Widget dropDown = DropdownMenu<String>(
      enabled: !widget.control.disabled,
      focusNode: _focusNode,
      initialSelection: value,
      enableFilter: widget.control.getBool("enable_filter", false)!,
      enableSearch: widget.control.getBool("enable_search", true)!,
      menuHeight: widget.control.getDouble("menu_height"),
      label: label is Control
          ? ControlWidget(control: label)
          : label is String
              ? Text(label,
                  style:
                      parseTextStyle(widget.control.get("label_style"), theme))
              : null,
      leadingIcon: leadingIcon is Control
          ? ControlWidget(control: leadingIcon)
          : leadingIcon is String
              ? Icon(parseIcon(leadingIcon))
              : prefixIcon is Control
                  ? ControlWidget(control: prefixIcon)
                  : prefixIcon is String
                      ? Icon(parseIcon(prefixIcon))
                      : null,
      trailingIcon: trailingIcon is Control
          ? ControlWidget(control: trailingIcon)
          : trailingIcon is String
              ? Icon(parseIcon(trailingIcon))
              : selectIcon is Control
                  ? ControlWidget(control: selectIcon)
                  : selectIcon is String
                      ? Icon(parseIcon(selectIcon))
                      : null,
      selectedTrailingIcon: selectedTrailingIcon is Control
          ? ControlWidget(control: selectedTrailingIcon)
          : selectedTrailingIcon is String
              ? Icon(parseIcon(selectedTrailingIcon))
              : null,
      textStyle: textStyle,
      textAlign: textAlign,
      width: widget.control.getDouble("width"),
      errorText: widget.control.getString("error_text"),
      hintText: widget.control.getString("hint_text"),
      helperText: widget.control.getString("helper_text"),
      menuStyle: MenuStyle(
        backgroundColor:
            parseWidgetStateColor(widget.control.get("bgcolor"), theme),
        elevation: parseWidgetStateDouble(widget.control.get("elevation")),
        fixedSize: WidgetStateProperty.all(Size.fromWidth(menuWidth)),
      ),
      inputDecorationTheme: inputDecorationTheme,
      onSelected: widget.control.disabled
          ? null
          : (String? value) {
              FletBackend.of(context)
                  .updateControl(widget.control.id, {"value": value});
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "change", value);
            },
      dropdownMenuEntries: items,
    );

    var didAutoFocus = false;

    if (!didAutoFocus && autofocus) {
      didAutoFocus = true;
      SchedulerBinding.instance.addPostFrameCallback((_) {
        FocusScope.of(context).autofocus(_focusNode);
      });
    }

    return ConstrainedControl(control: widget.control, child: dropDown);
  }
}
