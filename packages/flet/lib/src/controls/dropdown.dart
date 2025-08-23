import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

class DropdownControl extends StatefulWidget {
  final Control control;

  DropdownControl({Key? key, required this.control})
      : super(key: key ?? ValueKey("control_${control.id}"));

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
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
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
    var color = widget.control.getColor("color", context);

    TextAlign textAlign =
        widget.control.getTextAlign("text_align", TextAlign.start)!;

    var fillColor = widget.control.getColor("fill_color", context);
    var borderColor = widget.control.getColor("border_color", context);

    var borderRadius = widget.control.getBorderRadius("border_radius");
    var focusedBorderColor =
        widget.control.getColor("focused_border_color", context);
    var borderWidth = widget.control.getDouble("border_width");
    var focusedBorderWidth = widget.control.getDouble("focused_border_width");
    var menuWidth = widget.control.getDouble("menu_width", double.infinity)!;

    FormFieldInputBorder inputBorder = widget.control
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
      textStyle = (textStyle ?? const TextStyle()).copyWith(
          fontSize: textSize, color: color ?? theme.colorScheme.onSurface);
    }

    var items = widget.control
        .children("options")
        .map<DropdownMenuEntry<String>>((Control itemCtrl) {
      bool itemDisabled = widget.control.disabled || itemCtrl.disabled;
      ButtonStyle? style = itemCtrl.getButtonStyle("style", theme);

      return DropdownMenuEntry<String>(
        enabled: !itemDisabled,
        value: itemCtrl.getString("key") ??
            itemCtrl.getString("text") ??
            itemCtrl.id.toString(),
        label: itemCtrl.getString("text") ??
            itemCtrl.getString("key") ??
            itemCtrl.id.toString(),
        labelWidget: itemCtrl.buildWidget("content"),
        leadingIcon: itemCtrl.buildIconOrWidget("leading_icon"),
        trailingIcon: itemCtrl.buildIconOrWidget("trailing_icon"),
        style: style,
      );
    }).toList();

    String? value = widget.control.getString("value");
    if (items.where((item) => item.value == value).isEmpty) {
      value = null;
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

    Widget dropDown = DropdownMenu<String>(
      enabled: !widget.control.disabled,
      focusNode: _focusNode,
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
      menuStyle: MenuStyle(
        backgroundColor: widget.control.getWidgetStateColor("bgcolor", theme),
        elevation: widget.control.getWidgetStateDouble("elevation"),
        fixedSize: WidgetStateProperty.all(Size.fromWidth(menuWidth)),
      ),
      inputDecorationTheme: inputDecorationTheme,
      onSelected: widget.control.disabled
          ? null
          : (String? value) {
              widget.control.updateProperties({"value": value});
              widget.control.triggerEvent("change", value);
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

    return LayoutControl(control: widget.control, child: dropDown);
  }
}
