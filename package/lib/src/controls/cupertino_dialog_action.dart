import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/buttons.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
import 'create_control.dart';

class CupertinoDialogActionControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CupertinoDialogActionControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<CupertinoDialogActionControl> createState() =>
      _CupertinoDialogActionControlState();
}

class _CupertinoDialogActionControlState
    extends State<CupertinoDialogActionControl> {
  late final FocusNode _focusNode;
  String? _lastFocusValue;

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

  void _onFocusChange() {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${widget.control.id}");

    final server = FletAppServices.of(context).server;

    String text = widget.control.attrString("text", "")!;
    //IconData? icon = getMaterialIcon(widget.control.attrString("icon", "")!);
    // Color? iconColor = HexColor.fromString(
    //     Theme.of(context), widget.control.attrString("iconColor", "")!);
    var contentCtrls = widget.children.where((c) => c.name == "content");
    //bool onHover = widget.control.attrBool("onHover", false)!;
    //bool onLongPress = widget.control.attrBool("onLongPress", false)!;
    String url = widget.control.attrString("url", "")!;
    String? urlTarget = widget.control.attrString("urlTarget");
    //bool autofocus = widget.control.attrBool("autofocus", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("Button ${widget.control.id} clicked!");
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    // Function()? onLongPressHandler = onLongPress && !disabled
    //     ? () {
    //         debugPrint("Button ${widget.control.id} long pressed!");
    //         server.sendPageEvent(
    //             eventTarget: widget.control.id,
    //             eventName: "long_press",
    //             eventData: "");
    //       }
    //     : null;

    // Function(bool)? onHoverHandler = onHover && !disabled
    //     ? (state) {
    //         debugPrint("Button ${widget.control.id} hovered!");
    //         server.sendPageEvent(
    //             eventTarget: widget.control.id,
    //             eventName: "hover",
    //             eventData: state.toString());
    //       }
    //     : null;

    //TextButton? button;
    CupertinoDialogAction? button;

    // var theme = Theme.of(context);

    // var style = parseButtonStyle(Theme.of(context), widget.control, "style",
    //     defaultForegroundColor: theme.colorScheme.primary,
    //     defaultBackgroundColor: Colors.transparent,
    //     defaultOverlayColor: Colors.transparent,
    //     defaultShadowColor: Colors.transparent,
    //     defaultSurfaceTintColor: Colors.transparent,
    //     defaultElevation: 0,
    //     defaultPadding: const EdgeInsets.all(8),
    //     defaultBorderSide: BorderSide.none,
    //     defaultShape: theme.useMaterial3
    //         ? const StadiumBorder()
    //         : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

    // if (icon != null) {
    //   button = TextButton.icon(
    //       autofocus: autofocus,
    //       focusNode: _focusNode,
    //       onPressed: onPressed,
    //       onLongPress: onLongPressHandler,
    //       onHover: onHoverHandler,
    //       style: style,
    //       icon: Icon(
    //         icon,
    //         color: iconColor,
    //       ),
    //       label: Text(text));
    // } else
    if (contentCtrls.isNotEmpty) {
      // button = TextButton(
      //     autofocus: autofocus,
      //     focusNode: _focusNode,
      //     onPressed: onPressed,
      //     onLongPress: onLongPressHandler,
      //     onHover: onHoverHandler,
      //     style: style,
      //     child:
      //         createControl(widget.control, contentCtrls.first.id, disabled));
      button = CupertinoDialogAction(
          //autofocus: autofocus,
          //  focusNode: _focusNode,
          onPressed: onPressed,
          //     onLongPress: onLongPressHandler,
          //     onHover: onHoverHandler,
          //     style: style,
          child:
              createControl(widget.control, contentCtrls.first.id, disabled));
    } else {
      button = CupertinoDialogAction(
          //autofocus: autofocus,
          //focusNode: _focusNode,
          //style: style,
          onPressed: onPressed,
          //onLongPress: onLongPressHandler,
          //onHover: onHoverHandler,
          child: Text(text));
    }

    var focusValue = widget.control.attrString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return constrainedControl(context, button, widget.parent, widget.control);
  }
}
