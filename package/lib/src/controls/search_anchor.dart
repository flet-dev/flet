import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/text.dart';
import 'create_control.dart';

class SearchAnchorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SearchAnchorControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<SearchAnchorControl> createState() => _SearchAnchorControlState();
}

class _SearchAnchorControlState extends State<SearchAnchorControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("SearchAnchor build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    SearchController controller = SearchController();

    debugPrint(widget.control.attrs.toString());

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("SearchAnchor StoreConnector build: ${widget.control.id}");

          var suggestionCtrls =
              widget.children.where((c) => c.name == "controls" && c.isVisible);
          var barLeadingCtrls = widget.children
              .where((c) => c.name == "barLeading" && c.isVisible);
          var barTrailingCtrls = widget.children
              .where((c) => c.name == "barTrailing" && c.isVisible);
          var viewLeadingCtrls = widget.children
              .where((c) => c.name == "viewLeading" && c.isVisible);
          var viewTrailingCtrls = widget.children
              .where((c) => c.name == "viewTrailing" && c.isVisible);

          var viewBgcolor = HexColor.fromString(
              Theme.of(context), widget.control.attrString("viewBgcolor", "")!);
          var dividerColor = HexColor.fromString(Theme.of(context),
              widget.control.attrString("dividerColor", "")!);

          TextStyle? viewHeaderTextStyle = parseTextStyle(
              Theme.of(context), widget.control, "viewHeaderTextStyle");
          TextStyle? viewHintTextStyle = parseTextStyle(
              Theme.of(context), widget.control, "viewHintTextStyle");

          /*var method = widget.control.attrString("method");

          if (method != null) {
            debugPrint("SearchAnchor JSON method: $method");

            var mj = json.decode(method);
            var name = mj["n"] as String;
            var params = Map<String, dynamic>.from(mj["p"] as Map);

            if (name == "dismiss") {
              WidgetsBinding.instance.addPostFrameCallback((_) {
                List<Map<String, String>> props = [
                  {"i": widget.control.id, "method": ""}
                ];
                widget.dispatch(UpdateControlPropsAction(
                    UpdateControlPropsPayload(props: props)));
                FletAppServices.of(context)
                    .server
                    .updateControlProps(props: props);
                if (controller.isOpen) {
                  var text = params["text"].toString();
                  debugPrint("SearchAnchor CLOSEVIEW: $text");
                  setState(() {
                    controller.closeView(text);
                  });
                }
              });
            }
          }*/

          Widget anchor = SearchAnchor.bar(
            // searchController: controller,
            barHintText: widget.control.attrString("barHintText"),
            barBackgroundColor: parseMaterialStateColor(
                Theme.of(context), widget.control, "barBgcolor"),
            barOverlayColor: parseMaterialStateColor(
                Theme.of(context), widget.control, "barOverlayColor"),
            viewSide:
                parseBorderSide(Theme.of(context), widget.control, "viewSide"),
            isFullScreen: widget.control.attrBool("fullScreen", false),
            viewBackgroundColor: viewBgcolor,
            dividerColor: dividerColor,
            viewHintText: widget.control.attrString("viewHintText"),
            viewElevation: widget.control.attrDouble("viewElevation"),
            viewHeaderHintStyle: viewHintTextStyle,
            viewHeaderTextStyle: viewHeaderTextStyle,
            viewShape: parseOutlinedBorder(widget.control, "viewShape"),
            barLeading: barLeadingCtrls.isNotEmpty
                ? createControl(
                    widget.parent, barLeadingCtrls.first.id, disabled)
                : null,
            barTrailing: barTrailingCtrls.isNotEmpty
                ? barTrailingCtrls.map((ctrl) {
                    return createControl(widget.parent, ctrl.id, disabled);
                  })
                : null,
            viewTrailing: viewTrailingCtrls.isNotEmpty
                ? viewTrailingCtrls.map((ctrl) {
                    return createControl(widget.parent, ctrl.id, disabled);
                  })
                : null,
            viewLeading: viewLeadingCtrls.isNotEmpty
                ? createControl(
                    widget.parent, viewLeadingCtrls.first.id, disabled)
                : null,
            suggestionsBuilder:
                (BuildContext context, SearchController controller) {
              return suggestionCtrls.map((ctrl) {
                return createControl(widget.parent, ctrl.id, disabled);
              });
            },
          );

          return constrainedControl(
              context, anchor, widget.parent, widget.control);
        });
  }
}
