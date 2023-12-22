import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_children_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/alignment.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'form_field.dart';

class DropdownControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final dynamic dispatch;

  const DropdownControl(
      {super.key,
      this.parent,
      required this.control,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<DropdownControl> createState() => _DropdownControlState();
}

class _DropdownControlState extends State<DropdownControl> {
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
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
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

    final server = FletAppServices.of(context).server;

    return StoreConnector<AppState, ControlChildrenViewModel>(
        distinct: true,
        ignoreChange: (state) {
          return state.controls[widget.control.id] == null;
        },
        converter: (store) => ControlChildrenViewModel.fromStore(
            store, widget.control.id,
            dispatch: store.dispatch),
        builder: (context, itemsView) {
          debugPrint("Dropdown StoreConnector build: ${widget.control.id}");

          bool autofocus = widget.control.attrBool("autofocus", false)!;
          bool disabled = widget.control.isDisabled || widget.parentDisabled;

          var textSize = widget.control.attrDouble("textSize");

          var color = HexColor.fromString(
              Theme.of(context), widget.control.attrString("color", "")!);
          var focusedColor = HexColor.fromString(Theme.of(context),
              widget.control.attrString("focusedColor", "")!);

          TextStyle? textStyle =
              parseTextStyle(Theme.of(context), widget.control, "textStyle");
          if (textSize != null || color != null || focusedColor != null) {
            textStyle = (textStyle ?? const TextStyle()).copyWith(
                fontSize: textSize,
                color: (_focused ? focusedColor ?? color : color) ??
                    Theme.of(context).colorScheme.onSurface);
          }

          var alignment = parseAlignment(widget.control, "alignment");

          var items = itemsView.children
              .where((c) => c.name == null && c.isVisible)
              .map<DropdownMenuItem<String>>((Control itemCtrl) {
            Widget itemChild = Text(
              itemCtrl.attrs["text"] ?? itemCtrl.attrs["key"] ?? itemCtrl.id,
            );

            if (alignment != null) {
              itemChild = Container(alignment: alignment, child: itemChild);
            }
            return DropdownMenuItem<String>(
              enabled: !(disabled || itemCtrl.isDisabled),
              value: itemCtrl.attrs["key"] ??
                  itemCtrl.attrs["text"] ??
                  itemCtrl.id,
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

          var prefixControls = itemsView.children
              .where((c) => c.name == "prefix" && c.isVisible);
          var suffixControls = itemsView.children
              .where((c) => c.name == "suffix" && c.isVisible);

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
            borderRadius: borderRadius,
            alignment: alignment ?? AlignmentDirectional.centerStart,
            isExpanded: alignment != null,
            decoration: buildInputDecoration(
                context,
                widget.control,
                prefixControls.isNotEmpty ? prefixControls.first : null,
                suffixControls.isNotEmpty ? suffixControls.first : null,
                null,
                _focused),
            onChanged: disabled
                ? null
                : (String? value) {
                    debugPrint("Dropdown selected value: $value");
                    setState(() {
                      _value = value!;
                    });
                    List<Map<String, String>> props = [
                      {"i": widget.control.id, "value": value!}
                    ];
                    widget.dispatch(UpdateControlPropsAction(
                        UpdateControlPropsPayload(props: props)));
                    server.updateControlProps(props: props);
                    server.sendPageEvent(
                        eventTarget: widget.control.id,
                        eventName: "change",
                        eventData: value);
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
