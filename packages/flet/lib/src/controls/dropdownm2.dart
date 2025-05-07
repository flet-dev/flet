import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class DropdownM2Control extends StatefulWidget {
  final Control control;

  DropdownM2Control({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<DropdownM2Control> createState() => _DropdownM2ControlState();
}

class _DropdownM2ControlState extends State<DropdownM2Control> {
  String? _value;
  bool _focused = false;
  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("DropdownM2.$name($args)");
    switch (name) {
      case "focus":
        _focusNode.requestFocus();
      default:
        throw Exception("Unknown DropdownM2 method: $name");
    }
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("DropdownM2 build: ${widget.control.id}");

    var textSize = widget.control.getDouble("text_size");
    var color = widget.control.getColor("color", context);
    var focusedColor = widget.control.getColor("focused_color", context);

    var textStyle = widget.control
        .getTextStyle("text_style", Theme.of(context), const TextStyle())!;
    if (textSize != null || color != null || focusedColor != null) {
      textStyle = textStyle.copyWith(
          fontSize: textSize,
          color: (_focused ? (focusedColor ?? color) : color) ??
              Theme.of(context).colorScheme.onSurface);
    }

    var items = widget.control
        .children("options")
        .map<DropdownMenuItem<String>>((Control item) {
      var textStyle = item.getTextStyle("text_style", Theme.of(context));
      if (item.disabled && textStyle != null) {
        textStyle = textStyle.apply(color: Theme.of(context).disabledColor);
      }
      var value =
          item.getString("key") ?? item.getString("text") ?? item.id.toString();
      var content =
          item.buildWidget("content") ?? Text(value, style: textStyle);
      var alignment = item.getAlignment("alignment");
      if (alignment != null) {
        content = Container(alignment: alignment, child: content);
      }
      return DropdownMenuItem<String>(
          enabled: !item.disabled,
          value: value,
          alignment: alignment ?? AlignmentDirectional.centerStart,
          onTap: !item.disabled ? () => item.triggerEvent("click") : null,
          child: content);
    }).toList();

    String? value = widget.control.getString("value");
    if (_value != value) {
      _value = value;
    }

    if (items.where((item) => item.value == value).isEmpty) {
      _value = null;
    }

    Widget dropDown = DropdownButtonFormField<String>(
      style: textStyle,
      autofocus: widget.control.getBool("autofocus", false)!,
      focusNode: _focusNode,
      value: _value,
      dropdownColor: widget.control.getColor("bgcolor", context),
      enableFeedback: widget.control.getBool("enable_feedback"),
      elevation: widget.control.getInt("elevation", 8)!,
      padding: widget.control.getPadding("padding"),
      itemHeight: widget.control.getDouble("item_height"),
      menuMaxHeight: widget.control.getDouble("max_menu_height"),
      iconEnabledColor:
          widget.control.getColor("select_icon_enabled_color", context),
      iconDisabledColor:
          widget.control.getColor("select_icon_disabled_color", context),
      iconSize: widget.control.getDouble("select_icon_size", 24.0)!,
      borderRadius: widget.control.getBorderRadius("border_radius"),
      alignment: widget.control.getAlignment("alignment") ??
          AlignmentDirectional.centerStart,
      isExpanded: widget.control.getBool("options_fill_horizontally", true)!,
      icon: widget.control.buildIconOrWidget("select_icon"),
      hint: widget.control.buildWidget("hint"),
      disabledHint: widget.control.buildWidget("disabled_hint"),
      decoration: buildInputDecoration(context, widget.control,
          customSuffix: null, focused: _focused),
      onTap: !widget.control.disabled
          ? () => widget.control.triggerEvent("click")
          : null,
      onChanged: widget.control.disabled
          ? null
          : (String? value) {
              _value = value!;
              widget.control.updateProperties({"value": value});
              widget.control.triggerEvent("change", value);
            },
      items: items,
    );

    if (widget.control.getInt("expand", 0)! > 0) {
      return ConstrainedControl(control: widget.control, child: dropDown);
    } else {
      return LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          if (constraints.maxWidth == double.infinity &&
              widget.control.getDouble("width") == null) {
            dropDown = ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 300),
                child: dropDown);
          }

          return ConstrainedControl(control: widget.control, child: dropDown);
        },
      );
    }
  }
}
