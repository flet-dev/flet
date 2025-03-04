import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/icons.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';
import 'textfield.dart';

class DropdownControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DropdownControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<DropdownControl> createState() => _DropdownControlState();
}

class _DropdownControlState extends State<DropdownControl> with FletStoreMixin {
  String? _value;
  late final FocusNode _focusNode;
  String? _lastFocusValue;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("DropdownMenu build: ${widget.control.id}");
    return withControls(widget.control.childIds, (context, itemsView) {
      debugPrint("DropdownMenuFletControlState build: ${widget.control.id}");

      bool disabled = widget.control.isDisabled || widget.parentDisabled;
      bool editable = widget.control.attrBool("editable", false)!;
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      var textSize = widget.control.attrDouble("textSize");
      var label = widget.control.attrString("label");
      var trailingIconCtrl = widget.children
          .where((c) => c.name == "trailing_icon" && c.isVisible);
      var trailingIconStr =
          parseIcon(widget.control.attrString("trailingIcon"));

      var leadingIconCtrl =
          widget.children.where((c) => c.name == "leading_icon" && c.isVisible);
      var leadingIconStr = parseIcon(widget.control.attrString("leadingIcon"));

      var selectIconCtrl =
          widget.children.where((c) => c.name == "select_icon" && c.isVisible);
      var selectIconStr = parseIcon(widget.control.attrString("selectIcon"));

      var selectedTrailingIconCtrl = widget.children
          .where((c) => c.name == "selected_trailing_icon" && c.isVisible);
      var selectedTrailingIconStr =
          parseIcon(widget.control.attrString("selectedTrailingIcon"));
      var prefixIconCtrl =
          widget.children.where((c) => c.name == "prefix_icon" && c.isVisible);
      var prefixIconStr = parseIcon(widget.control.attrString("prefixIcon"));
      var labelCtrl =
          widget.children.where((c) => c.name == "label" && c.isVisible);
      var color = widget.control.attrColor("color", context);

      TextAlign textAlign = parseTextAlign(
          widget.control.attrString("textAlign"), TextAlign.start)!;

      var fillColor = widget.control.attrColor("fillColor", context);
      var borderColor = widget.control.attrColor("borderColor", context);

      var borderRadius = parseBorderRadius(widget.control, "borderRadius");
      var focusedBorderColor =
          widget.control.attrColor("focusedBorderColor", context);
      var borderWidth = widget.control.attrDouble("borderWidth");
      var focusedBorderWidth = widget.control.attrDouble("focusedBorderWidth");
      var menuWidth = widget.control.attrDouble("menuWidth") ?? double.infinity;

      FormFieldInputBorder inputBorder = parseFormFieldInputBorder(
        widget.control.attrString("border"),
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
          border = (border as OutlineInputBorder)
              .copyWith(borderRadius: borderRadius);
        }
        if (borderColor != null || borderWidth != null) {
          border = (border as OutlineInputBorder).copyWith(
              borderSide: borderWidth == 0
                  ? BorderSide.none
                  : BorderSide(
                      color: borderColor ??
                          Theme.of(context)
                              .colorScheme
                              .onSurface
                              .withOpacity(0.38),
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
                        Theme.of(context).colorScheme.primary,
                    width: focusedBorderWidth ?? borderWidth ?? 2.0));
      }

      InputDecorationTheme inputDecorationTheme = InputDecorationTheme(
        filled: widget.control.attrBool("filled", false)!,
        fillColor: fillColor,
        hintStyle:
            parseTextStyle(Theme.of(context), widget.control, "hintStyle"),
        errorStyle:
            parseTextStyle(Theme.of(context), widget.control, "errorStyle"),
        helperStyle:
            parseTextStyle(Theme.of(context), widget.control, "helperStyle"),
        border: border,
        enabledBorder: border,
        focusedBorder: focusedBorder,
        isDense: widget.control.attrBool("dense") ?? false,
        contentPadding: parseEdgeInsets(widget.control, "contentPadding"),
      );

      TextStyle? textStyle =
          parseTextStyle(Theme.of(context), widget.control, "textStyle");
      if (textSize != null || color != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: color ?? Theme.of(context).colorScheme.onSurface);
      }

      var items = itemsView.controlViews
          .where((c) =>
              c.control.name == null &&
              c.control.type == "dropdownoption" &&
              c.control.isVisible)
          .map<DropdownMenuEntry<String>>((ControlViewModel itemCtrlView) {
        var itemCtrl = itemCtrlView.control;
        bool itemDisabled = disabled || itemCtrl.isDisabled;
        ButtonStyle? style =
            parseButtonStyle(Theme.of(context), itemCtrl, "style");

        var contentCtrls = itemCtrlView.children
            .where((c) => c.name == "content" && c.isVisible);
        var leadingIconCtrls = itemCtrlView.children
            .where((c) => c.name == "leadingIcon" && c.isVisible);
        var trailingIconCtrls = itemCtrlView.children
            .where((c) => c.name == "trailingIcon" && c.isVisible);

        return DropdownMenuEntry<String>(
          enabled: !itemDisabled,
          value: itemCtrl.attrs["key"] ?? itemCtrl.attrs["text"] ?? itemCtrl.id,
          label: itemCtrl.attrs["text"] ?? itemCtrl.attrs["key"] ?? itemCtrl.id,
          labelWidget: contentCtrls.isNotEmpty
              ? createControl(
                  itemCtrlView.control, contentCtrls.first.id, itemDisabled)
              : null,
          leadingIcon: leadingIconCtrls.isNotEmpty
              ? createControl(
                  itemCtrlView.control, leadingIconCtrls.first.id, itemDisabled)
              : itemCtrlView.control.attrString("leadingIcon") != null
                  ? Icon(
                      parseIcon(itemCtrlView.control.attrString("leadingIcon")))
                  : null,
          trailingIcon: trailingIconCtrls.isNotEmpty
              ? createControl(itemCtrlView.control, trailingIconCtrls.first.id,
                  itemDisabled)
              : itemCtrlView.control.attrString("trailingIcon") != null
                  ? Icon(parseIcon(
                      itemCtrlView.control.attrString("trailingIcon")))
                  : null,
          style: style,
        );
      }).toList();

      String? value = widget.control.attrString("value");
      if (_value != value) {
        _value = value;
      }

      if (items.where((item) => item.value == value).isEmpty) {
        _value = null;
      }

      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        _focusNode.requestFocus();
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

      _focusNode.canRequestFocus = editable;

      Widget dropDown = DropdownMenu<String>(
        enabled: !disabled,
        focusNode: _focusNode,
        initialSelection: _value,
        //controller: controller,
        //requestFocusOnTap: editable,
        enableFilter: widget.control.attrBool("enableFilter", false)!,
        enableSearch: widget.control.attrBool("enableSearch", true)!,
        menuHeight: widget.control.attrDouble("menuHeight"),
        label: labelCtrl.isNotEmpty
            ? createControl(widget.control, labelCtrl.first.id, disabled)
            : label != null
                ? Text(label,
                    style: parseTextStyle(
                        Theme.of(context), widget.control, "labelStyle"))
                : null,
        leadingIcon: leadingIconCtrl.isNotEmpty
            ? createControl(widget.control, leadingIconCtrl.first.id, disabled)
            : leadingIconStr != null
                ? Icon(leadingIconStr)
                : prefixIconCtrl.isNotEmpty
                    ? createControl(
                        widget.control, prefixIconCtrl.first.id, disabled)
                    : prefixIconStr != null
                        ? Icon(prefixIconStr)
                        : null,
        trailingIcon: trailingIconCtrl.isNotEmpty
            ? createControl(widget.control, trailingIconCtrl.first.id, disabled)
            : trailingIconStr != null
                ? Icon(trailingIconStr)
                : selectIconCtrl.isNotEmpty
                    ? createControl(
                        widget.control, selectIconCtrl.first.id, disabled)
                    : selectIconStr != null
                        ? Icon(selectIconStr)
                        : null,
        selectedTrailingIcon: selectedTrailingIconCtrl.isNotEmpty
            ? createControl(
                widget.control, selectedTrailingIconCtrl.first.id, disabled)
            : selectedTrailingIconStr != null
                ? Icon(selectedTrailingIconStr)
                : null,
        textStyle: textStyle,
        textAlign: textAlign,
        width: widget.control.attrDouble("width"),
        errorText: widget.control.attrString("errorText"),
        hintText: widget.control.attrString("hintText"),
        helperText: widget.control.attrString("helperText"),
        //inputFormatters: inputFormatters,
        //expandedInsets: parseEdgeInsets(widget.control, "expandedInsets"),
        menuStyle: MenuStyle(
          backgroundColor: parseWidgetStateColor(
              Theme.of(context), widget.control, "bgcolor"),
          elevation: parseWidgetStateDouble(widget.control, "elevation"),
          fixedSize: WidgetStateProperty.all(Size.fromWidth(menuWidth)),
        ),

        inputDecorationTheme: inputDecorationTheme,
        onSelected: disabled
            ? null
            : (String? value) {
                debugPrint("DropdownMenu selected value: $value");
                _value = value!;
                widget.backend
                    .updateControlState(widget.control.id, {"value": value});
                widget.backend
                    .triggerControlEvent(widget.control.id, "change", value);
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

      return constrainedControl(
          context, dropDown, widget.parent, widget.control);
    });
  }
}
