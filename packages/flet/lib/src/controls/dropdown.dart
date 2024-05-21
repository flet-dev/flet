import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_store_mixin.dart';

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
    debugPrint("Dropdown build: ${widget.control.id}");

    return withControls(widget.control.childIds, (context, itemsView) {
      debugPrint("DropdownFletControlState build: ${widget.control.id}");

      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      var textSize = widget.control.attrDouble("textSize");
      var alignment = parseAlignment(widget.control, "alignment");
      var iconCtrl =
          widget.children.where((c) => c.name == "icon" && c.isVisible);
      var hintCtrl =
          widget.children.where((c) => c.name == "hint" && c.isVisible);

      var color = widget.control.attrColor("color", context);
      var focusedColor = widget.control.attrColor("focusedColor", context);
      var bgcolor = widget.control.attrColor("bgcolor", context);
      var iconEnabledColor =
          widget.control.attrColor("iconEnabledColor", context);
      var iconDisabledColor =
          widget.control.attrColor("iconDisabledColor", context);

      TextStyle? textStyle =
          parseTextStyle(Theme.of(context), widget.control, "textStyle");
      if (textSize != null || color != null || focusedColor != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: (_focused ? focusedColor ?? color : color) ??
                Theme.of(context).colorScheme.onSurface);
      }

      var items = itemsView.controlViews
          .map((v) => v.control)
          .where((c) => c.name == null && c.isVisible)
          .map<DropdownMenuItem<String>>((Control itemCtrl) {
        Widget itemChild = Text(
          itemCtrl.attrs["text"] ?? itemCtrl.attrs["key"] ?? itemCtrl.id,
        );
        var align = parseAlignment(itemCtrl, "alignment");
        if (align != null) {
          itemChild = Container(alignment: align, child: itemChild);
        }
        return DropdownMenuItem<String>(
          enabled: !(disabled || itemCtrl.isDisabled),
          value: itemCtrl.attrs["key"] ?? itemCtrl.attrs["text"] ?? itemCtrl.id,
          alignment: align ?? AlignmentDirectional.centerStart,
          onTap: !(disabled || itemCtrl.isDisabled)
              ? () {
                  widget.backend.triggerControlEvent(itemCtrl.id, "click");
                }
              : null,
          child: itemChild,
        );
      }).toList();

      String? value = widget.control.attrString("value");
      if (_value != value) {
        _value = value;
      }

      if (items.where((item) => item.value == value).isEmpty) {
        _value = null;
      }

      var prefixControls = itemsView.controlViews
          .where((c) => c.control.name == "prefix" && c.control.isVisible);
      var suffixControls = itemsView.controlViews
          .where((c) => c.control.name == "suffix" && c.control.isVisible);

      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        _focusNode.requestFocus();
      }

      var borderRadius = parseBorderRadius(widget.control, "borderRadius");

      Widget dropDown = DropdownButtonFormField<String>(
        style: textStyle,
        autofocus: autofocus,
        focusNode: _focusNode,
        value: _value,
        dropdownColor: bgcolor,
        enableFeedback: widget.control.attrBool("enableFeedback"),
        elevation: widget.control.attrInt("elevation", 8)!,
        padding: parseEdgeInsets(widget.control, "padding"),
        itemHeight: widget.control.attrDouble("itemHeight"),
        menuMaxHeight: widget.control.attrDouble("maxMenuHeight"),
        iconEnabledColor: iconEnabledColor,
        iconDisabledColor: iconDisabledColor,
        iconSize: widget.control.attrDouble("iconSize", 24.0)!,
        borderRadius: borderRadius,
        alignment: alignment ?? AlignmentDirectional.centerStart,
        isExpanded: alignment != null,
        icon: iconCtrl.isNotEmpty
            ? createControl(widget.control, iconCtrl.first.id, disabled)
            : null,
        hint: iconCtrl.isNotEmpty
            ? createControl(widget.control, hintCtrl.first.id, disabled)
            : null,
        decoration: buildInputDecoration(
            context,
            widget.control,
            prefixControls.isNotEmpty ? prefixControls.first.control : null,
            suffixControls.isNotEmpty ? suffixControls.first.control : null,
            null,
            _focused,
            disabled,
            widget.parentAdaptive),
        onTap: !disabled
            ? () {
                widget.backend.triggerControlEvent(widget.control.id, "click");
              }
            : null,
        onChanged: disabled
            ? null
            : (String? value) {
                debugPrint("Dropdown selected value: $value");
                _value = value!;
                widget.backend
                    .updateControlState(widget.control.id, {"value": value});
                widget.backend
                    .triggerControlEvent(widget.control.id, "change", value);
              },
        items: items,
      );

      if (widget.control.attrInt("expand", 0)! > 0) {
        return constrainedControl(
            context, dropDown, widget.parent, widget.control);
      } else {
        return LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
            if (constraints.maxWidth == double.infinity &&
                widget.control.attrDouble("width") == null) {
              dropDown = ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 300),
                child: dropDown,
              );
            }

            return constrainedControl(
                context, dropDown, widget.parent, widget.control);
          },
        );
      }
    });
  }
}
