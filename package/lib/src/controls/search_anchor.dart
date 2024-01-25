import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_control_state.dart';

class SearchAnchorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SearchAnchorControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  State<SearchAnchorControl> createState() => _SearchAnchorControlState();
}

class _SearchAnchorControlState extends FletControlState<SearchAnchorControl> {
  late final SearchController _controller;

  @override
  void initState() {
    super.initState();
    _controller = SearchController();
    _controller.addListener(_searchTextChanged);
  }

  @override
  void dispose() {
    _controller.removeListener(_searchTextChanged);
    _controller.dispose();
    super.dispose();
  }

  void _searchTextChanged() {
    debugPrint("_searchTextChanged: ${_controller.text}");
    _updateValue(_controller.text);
  }

  void _updateValue(String value) {
    debugPrint("SearchBar.changeValue: $value");
    updateControlProps(widget.control.id, {"value": value});
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("SearchAnchor build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    debugPrint(widget.control.attrs.toString());

    debugPrint("SearchAnchor build: ${widget.control.id}");

    var value = widget.control.attrString("value");
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

    var viewBgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("viewBgcolor", "")!);
    var dividerColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("dividerColor", "")!);

    TextStyle? viewHeaderTextStyle = parseTextStyle(
        Theme.of(context), widget.control, "viewHeaderTextStyle");
    TextStyle? viewHintTextStyle =
        parseTextStyle(Theme.of(context), widget.control, "viewHintTextStyle");

    var method = widget.control.attrString("method");

    if (method != null) {
      debugPrint("SearchAnchor JSON method: $method");

      void resetMethod() {
        updateControlProps(widget.control.id, {"method": ""});
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
        headerHintStyle: viewHintTextStyle,
        headerTextStyle: viewHeaderTextStyle,
        viewSide:
            parseBorderSide(Theme.of(context), widget.control, "viewSide"),
        isFullScreen: widget.control.attrBool("fullScreen", false),
        viewBackgroundColor: viewBgcolor,
        dividerColor: dividerColor,
        viewHintText: widget.control.attrString("viewHintText"),
        viewElevation: widget.control.attrDouble("viewElevation"),
        viewShape: parseOutlinedBorder(widget.control, "viewShape"),
        viewTrailing: viewTrailingCtrls.isNotEmpty
            ? viewTrailingCtrls.map((ctrl) {
                return createControl(widget.parent, ctrl.id, disabled);
              })
            : null,
        viewLeading: viewLeadingCtrls.isNotEmpty
            ? createControl(widget.parent, viewLeadingCtrls.first.id, disabled)
            : null,
        builder: (BuildContext context, SearchController controller) {
          return SearchBar(
            controller: controller,
            hintText: widget.control.attrString("barHintText"),
            backgroundColor: parseMaterialStateColor(
                Theme.of(context), widget.control, "barBgcolor"),
            overlayColor: parseMaterialStateColor(
                Theme.of(context), widget.control, "barOverlayColor"),
            leading: barLeadingCtrls.isNotEmpty
                ? createControl(
                    widget.parent, barLeadingCtrls.first.id, disabled)
                : null,
            trailing: barTrailingCtrls.isNotEmpty
                ? barTrailingCtrls.map((ctrl) {
                    return createControl(widget.parent, ctrl.id, disabled);
                  })
                : null,
            onTap: () {
              if (onTap) {
                sendControlEvent(widget.control.id, "tap", "");
              }
              controller.openView();
            },
            onSubmitted: onSubmit
                ? (String value) {
                    debugPrint("SearchBar.onSubmit: $value");
                    _updateValue(value);
                    sendControlEvent(widget.control.id, "submit", value);
                  }
                : null,
            onChanged: onChange
                ? (String value) {
                    debugPrint("SearchBar.onChange: $value");
                    _updateValue(value);
                    sendControlEvent(widget.control.id, "change", value);
                  }
                : null,
          );
        },
        suggestionsBuilder:
            (BuildContext context, SearchController controller) {
          return suggestionCtrls.map((ctrl) {
            return createControl(widget.parent, ctrl.id, disabled);
          });
        });

    return constrainedControl(context, anchor, widget.parent, widget.control);
  }
}
