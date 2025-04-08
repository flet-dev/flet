import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/form_field.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class SearchBarControl extends StatefulWidget {
  final Control control;

  const SearchBarControl({super.key, required this.control});

  @override
  State<SearchBarControl> createState() => _SearchBarControlState();
}

class _SearchBarControlState extends State<SearchBarControl> {
  late final SearchController _controller;
  bool _focused = false;
  TextCapitalization _textCapitalization = TextCapitalization.none;
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
    widget.control.triggerEvent(_focusNode.hasFocus ? "focus" : "blur");
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
    _textCapitalization = parseTextCapitalization(
        widget.control.getString("capitalization"), TextCapitalization.none)!;
    _updateValue(_controller.text);
  }

  void _updateValue(String value) {
    value = applyCapitalization(value);
    if (_controller.value.text != value) {
      _controller.value = TextEditingValue(
        text: value,
        selection: TextSelection.collapsed(offset: value.length),
      );
    }

    widget.control.updateProperties({"value": value});
  }

  String applyCapitalization(String text) {
    switch (_textCapitalization) {
      /// Capitalizes the first character of each word.
      case TextCapitalization.words:
        return text
            .split(RegExp(r'\s+'))
            .map((word) => word.isNotEmpty
                ? word[0].toUpperCase() + word.substring(1).toLowerCase()
                : word)
            .join(' ');

      /// Capitalizes the first character of each sentence.
      case TextCapitalization.sentences:
        return text
            .split('. ')
            .map((sentence) => sentence.isNotEmpty
                ? sentence.trimLeft()[0].toUpperCase() +
                    sentence.substring(1).toLowerCase()
                : sentence)
            .join('. ');

      /// Capitalizes all characters.
      case TextCapitalization.characters:
        return text.toUpperCase();

      /// No change.
      case TextCapitalization.none:
        return text;
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SearchAnchor build: ${widget.control.id}");

    var value = widget.control.getString("value", "");
    if (value != null && value != _controller.text) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _controller.text = value;
      });
    }

    bool onChange = widget.control.getBool("on_change", false)!;
    bool onTap = widget.control.getBool("on_tap", false)!;
    bool onSubmit = widget.control.getBool("on_submit", false)!;
    TextInputType keyboardType =
        widget.control.getTextInputType("keyboard_type", TextInputType.text)!;

    var focusValue = widget.control.getString("focus");
    var blurValue = widget.control.getString("blur");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }
    if (blurValue != null && blurValue != _lastBlurValue) {
      _lastBlurValue = blurValue;
      _focusNode.unfocus();
    }

    // TODO: implement these methods
    // var method = widget.control.getString("method");
    //
    // if (method != null) {
    //   void resetMethod() {
    //     widget.control.updateProperties({"method": ""}, context);
    //   }
    //
    //   var mj = json.decode(method);
    //   var name = mj["n"] as String;
    //   var params = Map<String, dynamic>.from(mj["p"] as Map);
    //
    //   if (name == "closeView") {
    //     WidgetsBinding.instance.addPostFrameCallback((_) {
    //       resetMethod();
    //       if (_controller.isOpen) {
    //         var text = params["text"].toString();
    //         _updateValue(text);
    //         _controller.closeView(text);
    //       }
    //     });
    //   } else if (name == "openView") {
    //     WidgetsBinding.instance.addPostFrameCallback((_) {
    //       resetMethod();
    //       if (!_controller.isOpen) {
    //         _controller.openView();
    //       }
    //     });
    //   }
    // }

    Widget anchor = SearchAnchor(
        searchController: _controller,
        headerHintStyle: widget.control
            .getTextStyle("view_hint_text_style", Theme.of(context)),
        headerTextStyle: widget.control
            .getTextStyle("view_header_text_style", Theme.of(context)),
        viewSide: widget.control.getBorderSide("view_side", Theme.of(context)),
        isFullScreen: widget.control.getBool("full_screen", false),
        viewBackgroundColor: widget.control.getColor("view_bgcolor", context),
        dividerColor: widget.control.getColor("divider_color", context),
        viewHintText: widget.control.getString("view_hint_text"),
        viewElevation: widget.control.getDouble("view_elevation"),
        headerHeight: widget.control.getDouble("view_header_height"),
        viewConstraints:
            widget.control.getBoxConstraints("view_size_constraints"),
        viewShape: widget.control.getShape("view_shape"),
        viewTrailing: widget.control.buildWidgets("view_trailing"),
        viewLeading: widget.control.buildWidget("view_leading"),
        viewOnSubmitted: onSubmit
            ? (String value) {
                _updateValue(value);
                widget.control.triggerEvent("submit", value);
              }
            : null,
        viewOnChanged: onChange
            ? (String value) {
                _updateValue(value);
                widget.control.triggerEvent("change", value);
              }
            : null,
        viewSurfaceTintColor:
            widget.control.getColor("view_surface_tint_color", context),
        textCapitalization: _textCapitalization,
        keyboardType: keyboardType,
        builder: (BuildContext context, SearchController controller) {
          return SearchBar(
            controller: controller,
            keyboardType: keyboardType,
            textCapitalization: _textCapitalization,
            autoFocus: widget.control.getBool("autofocus", false)!,
            focusNode: _focusNode,
            hintText: widget.control.getString("bar_hint_text"),
            elevation: widget.control.getWidgetStateDouble("bar_elevation"),
            shape: widget.control.getWidgetStateOutlinedBorder("bar_shape"),
            padding: widget.control.getWidgetStatePadding("bar_padding"),
            textStyle: widget.control
                .getWidgetStateTextStyle("bar_text_style", Theme.of(context)),
            hintStyle: widget.control.getWidgetStateTextStyle(
                "bar_hint_text_style", Theme.of(context)),
            shadowColor: widget.control
                .getWidgetStateColor("bar_shadow_color", Theme.of(context)),
            surfaceTintColor: widget.control.getWidgetStateColor(
                "bar_surface_tint_color", Theme.of(context)),
            side: widget.control
                .getWidgetStateBorderSide("bar_border_side", Theme.of(context)),
            backgroundColor: widget.control
                .getWidgetStateColor("bar_bgcolor", Theme.of(context)),
            overlayColor: widget.control
                .getWidgetStateColor("bar_overlay_color", Theme.of(context)),
            scrollPadding: widget.control
                .getPadding("bar_scroll_padding", const EdgeInsets.all(20.0))!,
            leading: widget.control.buildWidget("bar_leading"),
            trailing: widget.control.buildWidgets("bar_trailing"),
            onTap: onTap
                ? () {
                    widget.control.triggerEvent("tap");
                  }
                : null,
            onTapOutside: widget.control.getBool("on_tap_outside_bar", false)!
                ? (PointerDownEvent? event) {
                    widget.control.triggerEvent("tap_outside_bar");
                  }
                : null,
            onSubmitted: onSubmit
                ? (String value) {
                    _updateValue(value);
                    widget.control.triggerEvent("submit");
                  }
                : null,
            onChanged: onChange
                ? (String value) {
                    _updateValue(value);
                    widget.control.triggerEvent("change");
                  }
                : null,
          );
        },
        suggestionsBuilder:
            (BuildContext context, SearchController controller) {
          return widget.control.buildWidgets("controls");
        });

    return ConstrainedControl(control: widget.control, child: anchor);
  }
}
