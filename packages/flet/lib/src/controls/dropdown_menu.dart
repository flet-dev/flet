import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../utils/buttons.dart';
import '../utils/edge_insets.dart';
import '../utils/icons.dart';
import '../utils/menu.dart';
import '../utils/text.dart';
import '../utils/textfield.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';
import 'textfield.dart';

class DropdownMenuControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const DropdownMenuControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<DropdownMenuControl> createState() => _DropdownMenuControlState();
}

class _DropdownMenuControlState extends State<DropdownMenuControl>
    with FletStoreMixin {
  String? _value;
  bool _focused = false;
  late final FocusNode _focusNode;
  String? _lastFocusValue;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
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

      var textSize = widget.control.attrDouble("textSize");
      var label = widget.control.attrString("label");
      var suffixCtrl =
          widget.children.where((c) => c.name == "suffix" && c.isVisible);
      var selectedSuffixCtrl = widget.children
          .where((c) => c.name == "selectedSuffix" && c.isVisible);
      var prefixCtrl =
          widget.children.where((c) => c.name == "prefix" && c.isVisible);
      var labelCtrl =
          widget.children.where((c) => c.name == "label" && c.isVisible);
      var selectedSuffixIcon = widget.control.attrString("selectedSuffixIcon");
      var prefixIcon = widget.control.attrString("prefixIcon");
      var suffixIcon = widget.control.attrString("suffixIcon");
      var color = widget.control.attrColor("color", context);
      var focusedColor = widget.control.attrColor("focusedColor", context);

      TextStyle? textStyle =
          parseTextStyle(Theme.of(context), widget.control, "textStyle");
      if (textSize != null || color != null || focusedColor != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: (_focused ? focusedColor ?? color : color) ??
                Theme.of(context).colorScheme.onSurface);
      }

      var items = itemsView.controlViews
          .where((c) =>
              c.control.name == null &&
              c.control.type == "dropdownmenuoption" &&
              c.control.isVisible)
          .map<DropdownMenuEntry<String>>((ControlViewModel itemCtrlView) {
        var itemCtrl = itemCtrlView.control;
        bool itemDisabled = disabled || itemCtrl.isDisabled;
        ButtonStyle? style =
            parseButtonStyle(Theme.of(context), itemCtrl, "style");

        var contentCtrls = itemCtrlView.children
            .where((c) => c.name == "content" && c.isVisible);

        var prefixIconCtrls = itemCtrlView.children
            .where((c) => c.name == "prefix" && c.isVisible);
        var suffixIconCtrls = itemCtrlView.children
            .where((c) => c.name == "suffix" && c.isVisible);

        return DropdownMenuEntry<String>(
          enabled: !itemDisabled,
          value: itemCtrl.attrs["key"] ?? itemCtrl.attrs["text"] ?? itemCtrl.id,
          label: itemCtrl.attrs["text"] ?? itemCtrl.attrs["key"] ?? itemCtrl.id,
          labelWidget: contentCtrls.isNotEmpty
              ? createControl(
                  itemCtrlView.control, contentCtrls.first.id, itemDisabled)
              : null,
          leadingIcon: prefixIconCtrls.isNotEmpty
              ? createControl(
                  itemCtrlView.control, prefixIconCtrls.first.id, itemDisabled)
              : itemCtrlView.control.attrString("prefixIcon") != null
                  ? Icon(
                      parseIcon(itemCtrlView.control.attrString("prefixIcon")))
                  : null,
          trailingIcon: suffixIconCtrls.isNotEmpty
              ? createControl(
                  itemCtrlView.control, suffixIconCtrls.first.id, itemDisabled)
              : itemCtrlView.control.attrString("suffixIcon") != null
                  ? Icon(
                      parseIcon(itemCtrlView.control.attrString("suffixIcon")))
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

      Widget dropDown = DropdownMenu<String>(
        enabled: !disabled,
        enableFilter: widget.control.attrBool("enableFilter", false)!,
        enableSearch: widget.control.attrBool("enableSearch", true)!,
        errorText: widget.control.attrString("errorText"),
        helperText: widget.control.attrString("helperText"),
        hintText: widget.control.attrString("hintText"),
        initialSelection: _value,
        requestFocusOnTap: widget.control.attrBool("requestFocusOnTap", true)!,
        menuHeight: widget.control.attrDouble("menuHeight"),
        width: widget.control.attrDouble("width"),
        textStyle: textStyle,
        inputFormatters: inputFormatters,
        expandedInsets: parseEdgeInsets(widget.control, "expandedInsets"),
        menuStyle: parseMenuStyle(Theme.of(context), widget.control, "style"),
        focusNode: _focusNode,
        label: labelCtrl.isNotEmpty
            ? createControl(widget.control, labelCtrl.first.id, disabled)
            : label != null
                ? Text(label,
                    style: parseTextStyle(
                        Theme.of(context), widget.control, "labelStyle"))
                : null,
        trailingIcon: suffixCtrl.isNotEmpty
            ? createControl(widget.control, suffixCtrl.first.id, disabled)
            : suffixIcon != null
                ? Icon(parseIcon(suffixIcon))
                : null,
        leadingIcon: prefixCtrl.isNotEmpty
            ? createControl(widget.control, prefixCtrl.first.id, disabled)
            : prefixIcon != null
                ? Icon(parseIcon(prefixIcon))
                : null,
        selectedTrailingIcon: selectedSuffixCtrl.isNotEmpty
            ? createControl(
                widget.control, selectedSuffixCtrl.first.id, disabled)
            : selectedSuffixIcon != null
                ? Icon(parseIcon(selectedSuffixIcon))
                : null,
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

      return constrainedControl(
          context, dropDown, widget.parent, widget.control);
    });
  }
}
