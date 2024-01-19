import 'package:collection/collection.dart';
import 'package:flet/src/flet_app_services.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/controls_view_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/colors.dart';
import 'app_bar.dart';
import 'create_control.dart';
import 'cupertino_app_bar.dart';
import 'error.dart';

class PageletControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final dynamic dispatch;

  const PageletControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.dispatch});

  @override
  State<PageletControl> createState() => _PageletControlState();
}

class _PageletControlState extends State<PageletControl> {
  bool _selected = false;

  late final FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onSelect(bool selected) {
    var strSelected = selected.toString();
    debugPrint(strSelected);
    setState(() {
      _selected = selected;
    });
    List<Map<String, String>> props = [
      {"i": widget.control.id, "selected": strSelected}
    ];
    widget.dispatch(
        UpdateControlPropsAction(UpdateControlPropsPayload(props: props)));
    final server = FletAppServices.of(context).server;
    server.updateControlProps(props: props);
    server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: "select",
        eventData: strSelected);
  }

  void _onFocusChange() {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Pagelet build: ${widget.control.id}");

    var appBarCtrls =
        widget.children.where((c) => c.name == "appbar" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var deleteIconCtrls =
        widget.children.where((c) => c.name == "deleteIcon" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Pagelet must have content specified.");
    }

    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var bgcolor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("bgcolor", "")!);
    var deleteIconColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("deleteIconColor", "")!);
    var disabledColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("disabledColor", "")!);

    final server = FletAppServices.of(context).server;
    bool onClick = widget.control.attrBool("onclick", false)!;
    bool onDelete = widget.control.attrBool("onDelete", false)!;
    bool onSelect = widget.control.attrBool("onSelect", false)!;

    if (onSelect && onClick) {
      return const ErrorControl(
          "Chip cannot have both on_select and on_click events specified.");
    }

    bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool selected = widget.control.attrBool("selected", false)!;
    if (_selected != selected) {
      _selected = selected;
    }
    bool showCheckmark = widget.control.attrBool("showCheckmark", true)!;
    String deleteButtonTooltipMessage =
        widget.control.attrString("deleteButtonTooltipMessage", "")!;

    var elevation = widget.control.attrDouble("elevation");

    // var appBarView = childrenViews.controlViews
    //     .firstWhereOrNull((v) => v.control.id == (appBar?.id ?? ""));
    // var cupertinoAppBarView = childrenViews.controlViews
    //     .firstWhereOrNull((v) => v.control.id == (cupertinoAppBar?.id ?? ""));

    Function()? onClickHandler = onClick && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} clicked!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    Function()? onDeleteHandler = onDelete && !disabled
        ? () {
            debugPrint("Chip ${widget.control.id} deleted!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "delete",
                eventData: "");
          }
        : null;

    List<String> childIds = [
      appBarCtrls.firstOrNull?.id,
      // drawer?.id,
      // endDrawer?.id
    ].whereNotNull().toList();

    return StoreConnector<AppState, ControlsViewModel>(
        distinct: true,
        converter: (store) => ControlsViewModel.fromStore(store, childIds),
        ignoreChange: (state) {
          //debugPrint("ignoreChange: $id");
          for (var id in childIds) {
            if (state.controls[id] == null) {
              return true;
            }
          }
          return false;
        },
        builder: (context, childrenViews) {
          var appBarView = childrenViews.controlViews.firstWhereOrNull(
              (v) => v.control.id == (appBarCtrls.firstOrNull?.id ?? ""));

          var bar = appBarView != null
              ? appBarView.control.type == "appbar"
                  ? AppBarControl(
                      parent: widget.control,
                      control: appBarView.control,
                      children: appBarView.children,
                      parentDisabled: widget.control.isDisabled,
                      height: appBarView.control
                          .attrDouble("toolbarHeight", kToolbarHeight)!)
                  : appBarView.control.type == "cupertinoappbar"
                      ? CupertinoAppBarControl(
                          parent: widget.control,
                          control: appBarView.control,
                          children: appBarView.children,
                          parentDisabled: widget.control.isDisabled,
                          bgcolor: HexColor.fromString(Theme.of(context),
                              appBarView.control.attrString("bgcolor", "")!),
                        ) as ObstructingPreferredSizeWidget
                      : null
              : null;
          return constrainedControl(
              context,
              Scaffold(
                // autofocus: autofocus,
                // focusNode: _focusNode,
                appBar: bar,
                // avatar: leadingCtrls.isNotEmpty
                //     ? createControl(widget.control, leadingCtrls.first.id, disabled)
                //     : null,
                backgroundColor: bgcolor,
                body: createControl(
                    widget.control, contentCtrls.first.id, disabled),
                // checkmarkColor: HexColor.fromString(
                //     Theme.of(context), widget.control.attrString("checkColor", "")!),
                // selected: _selected,
                // showCheckmark: showCheckmark,
                // deleteButtonTooltipMessage: deleteButtonTooltipMessage,
                // onPressed: onClickHandler,
                // onDeleted: onDeleteHandler,
                // onSelected: onSelect && !disabled
                //     ? (bool selected) {
                //         _onSelect(selected);
                //       }
                //     : null,
                // deleteIcon: deleteIconCtrls.isNotEmpty
                //     ? createControl(
                //         widget.control, deleteIconCtrls.first.id, disabled)
                //     : null,
                // deleteIconColor: deleteIconColor,
                // disabledColor: disabledColor,
                // elevation: elevation,
                // isEnabled: !disabled,
                // padding: parseEdgeInsets(widget.control, "padding"),
                // labelPadding: parseEdgeInsets(widget.control, "labelPadding"),
                // labelStyle:
                //     parseTextStyle(Theme.of(context), widget.control, "labelStyle"),
                // selectedColor: HexColor.fromString(Theme.of(context),
                //     widget.control.attrString("selectedColor", "")!),
                // selectedShadowColor: HexColor.fromString(Theme.of(context),
                //     widget.control.attrString("selectedShadowColor", "")!),
                // shadowColor: HexColor.fromString(
                //     Theme.of(context), widget.control.attrString("shadowColor", "")!),
                // shape: parseOutlinedBorder(widget.control, "shape"),
              ),
              widget.parent,
              widget.control);
        });
  }
}
