import 'dart:convert';

import 'package:flutter/material.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'create_control.dart';

class SearchAnchorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const SearchAnchorControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<SearchAnchorControl> createState() => _SearchAnchorControlState();
}

class _SearchAnchorControlState extends State<SearchAnchorControl> {
  late final SearchController _controller;
  bool _focused = false;
  late final FocusNode _focusNode;
  String? _lastFocusValue;
  String? _lastBlurValue;

  @override
  void initState() {
    super.initState();
    _controller = SearchController();
    _controller.addListener(_searchTextChanged);
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
    _controller.removeListener(_searchTextChanged);
    _controller.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _searchTextChanged() {
    debugPrint("_searchTextChanged: ${_controller.text}");
    _updateValue(_controller.text);
  }

  void _updateValue(String value) {
    debugPrint("SearchBar.changeValue: $value");
    widget.backend.updateControlState(widget.control.id, {"value": value});
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SearchAnchor build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var value = widget.control.attrString("value", "");
    if (value != null && value != _controller.text) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.text = value;
      });
    }

    bool onChange = widget.control.attrBool("onChange", false)!;
    bool onTap = widget.control.attrBool("onTap", false)!;
    bool onSubmit = widget.control.attrBool("onSubmit", false)!;

    var suggestionCtrls =
        widget.children.where((c) => c.name == "controls" && c.isVisible);
    var barLeadingCtrls =
        widget.children.where((c) => c.name == "barLeading" && c.isVisible);
    var barTrailingCtrls =
        widget.children.where((c) => c.name == "barTrailing" && c.isVisible);
    var viewLeadingCtrls =
        widget.children.where((c) => c.name == "viewLeading" && c.isVisible);
    var viewTrailingCtrls =
        widget.children.where((c) => c.name == "viewTrailing" && c.isVisible);

    var textCapitalization = parseTextCapitalization(
        widget.control.attrString("textCapitalization"));
    TextInputType keyboardType = parseTextInputType(
        widget.control.attrString("keyboardType"), TextInputType.text)!;

    var focusValue = widget.control.attrString("focus");
    var blurValue = widget.control.attrString("blur");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }
    if (blurValue != null && blurValue != _lastBlurValue) {
      _lastBlurValue = blurValue;
      _focusNode.unfocus();
    }

    var method = widget.control.attrString("method");

    if (method != null) {
      debugPrint("SearchAnchor JSON method: $method");

      void resetMethod() {
        widget.backend.updateControlState(widget.control.id, {"method": ""});
      }

      var mj = json.decode(method);
      var name = mj["n"] as String;
      var params = Map<String, dynamic>.from(mj["p"] as Map);

      if (name == "closeView") {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          resetMethod();
          if (_controller.isOpen) {
            var text = params["text"].toString();
            _updateValue(text);
            _controller.closeView(text);
          }
        });
      } else if (name == "openView") {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          resetMethod();
          if (!_controller.isOpen) {
            _controller.openView();
          }
        });
      }
    }

    Widget anchor = SearchAnchor(
        searchController: _controller,
        headerHintStyle: parseTextStyle(
            Theme.of(context), widget.control, "viewHintTextStyle"),
        headerTextStyle: parseTextStyle(
            Theme.of(context), widget.control, "viewHeaderTextStyle"),
        viewSide:
            parseBorderSide(Theme.of(context), widget.control, "viewSide"),
        isFullScreen: widget.control.attrBool("fullScreen", false),
        viewBackgroundColor: widget.control.attrColor("viewBgcolor", context),
        dividerColor: widget.control.attrColor("dividerColor", context),
        viewHintText: widget.control.attrString("viewHintText"),
        viewElevation: widget.control.attrDouble("viewElevation"),
        headerHeight: widget.control.attrDouble("viewHeaderHeight"),
        viewConstraints:
            parseBoxConstraints(widget.control, "viewSizeConstraints"),
        viewShape: parseOutlinedBorder(widget.control, "viewShape"),
        viewTrailing: viewTrailingCtrls.isNotEmpty
            ? viewTrailingCtrls.map((ctrl) {
                return createControl(widget.parent, ctrl.id, disabled,
                    parentAdaptive: widget.parentAdaptive);
              })
            : null,
        viewLeading: viewLeadingCtrls.isNotEmpty
            ? createControl(widget.parent, viewLeadingCtrls.first.id, disabled,
                parentAdaptive: widget.parentAdaptive)
            : null,
        viewOnSubmitted: onSubmit
            ? (String value) {
                debugPrint("SearchBar.onSubmit: $value");
                _updateValue(value);
                widget.backend
                    .triggerControlEvent(widget.control.id, "submit", value);
              }
            : null,
        viewOnChanged: onChange
            ? (String value) {
                debugPrint("SearchBar.onChange: $value");
                _updateValue(value);
                widget.backend
                    .triggerControlEvent(widget.control.id, "change", value);
              }
            : null,
        viewSurfaceTintColor:
            widget.control.attrColor("viewSurfaceTintColor", context),
        textCapitalization: textCapitalization,
        keyboardType: keyboardType,
        builder: (BuildContext context, SearchController controller) {
          return SearchBar(
            controller: controller,
            keyboardType: keyboardType,
            textCapitalization: textCapitalization,
            autoFocus: widget.control.attrBool("autoFocus", false)!,
            focusNode: _focusNode,
            hintText: widget.control.attrString("barHintText"),
            elevation: parseWidgetStateDouble(widget.control, "barElevation"),
            shape: parseWidgetStateOutlinedBorder(widget.control, "barShape"),
            padding: parseWidgetStateEdgeInsets(widget.control, "barPadding"),
            textStyle: parseWidgetStateTextStyle(
                Theme.of(context), widget.control, "barTextStyle"),
            hintStyle: parseWidgetStateTextStyle(
                Theme.of(context), widget.control, "barHintTextStyle"),
            shadowColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "barShadowColor"),
            surfaceTintColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "barSurfaceTintColor"),
            side: parseWidgetStateBorderSide(
                Theme.of(context), widget.control, "barBorderSide"),
            backgroundColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "barBgcolor"),
            overlayColor: parseWidgetStateColor(
                Theme.of(context), widget.control, "barOverlayColor"),
            scrollPadding: parseEdgeInsets(widget.control, "barScrollPadding",
                const EdgeInsets.all(20.0))!,
            leading: barLeadingCtrls.isNotEmpty
                ? createControl(
                    widget.parent, barLeadingCtrls.first.id, disabled,
                    parentAdaptive: widget.parentAdaptive)
                : null,
            trailing: barTrailingCtrls.isNotEmpty
                ? barTrailingCtrls.map((ctrl) {
                    return createControl(widget.parent, ctrl.id, disabled,
                        parentAdaptive: widget.parentAdaptive);
                  })
                : null,
            onTap: onTap
                ? () {
                    widget.backend
                        .triggerControlEvent(widget.control.id, "tap");
                  }
                : null,
            onTapOutside: widget.control.attrBool("onTapOutsideBar", false)!
                ? (PointerDownEvent? event) {
                    widget.backend.triggerControlEvent(
                        widget.control.id, "tapOutsideBar");
                  }
                : null,
            onSubmitted: onSubmit
                ? (String value) {
                    debugPrint("SearchBar.onSubmit: $value");
                    _updateValue(value);
                    widget.backend.triggerControlEvent(
                        widget.control.id, "submit", value);
                  }
                : null,
            onChanged: onChange
                ? (String value) {
                    debugPrint("SearchBar.onChange: $value");
                    _updateValue(value);
                    widget.backend.triggerControlEvent(
                        widget.control.id, "change", value);
                  }
                : null,
          );
        },
        suggestionsBuilder:
            (BuildContext context, SearchController controller) {
          return suggestionCtrls.map((ctrl) {
            return createControl(widget.parent, ctrl.id, disabled,
                parentAdaptive: widget.parentAdaptive);
          });
        });

    return constrainedControl(context, anchor, widget.parent, widget.control);
  }
}
