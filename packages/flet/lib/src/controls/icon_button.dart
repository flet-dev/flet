import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

//import '../flet_control_backend.dart';
import '../utils/launch_url.dart';
import '../widgets/error.dart';
import 'base_controls.dart';
//import 'create_control.dart';
import 'cupertino_button.dart';
//import 'error.dart';
//import 'flet_store_mixin.dart';

class IconButtonControl extends StatefulWidget {
  //final Control? parent;
  final Control control;
  //final List<Control> children;
  //final bool parentDisabled;
  //final bool? parentAdaptive;
  //final FletControlBackend backend;

  const IconButtonControl({
    super.key,
    //this.parent,
    required this.control,
    //required this.children,
    //required this.parentDisabled,
    //required this.parentAdaptive,
    //required this.backend,
  });

  @override
  State<IconButtonControl> createState() => _IconButtonControlState();
}

class _IconButtonControlState extends State<IconButtonControl>
    with FletStoreMixin {
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
    FletBackend.of(context).triggerControlEvent(
        widget.control, _focusNode.hasFocus ? "focus" : "blur");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("IconButton build: ${widget.control.id}");

    return withPagePlatform((context, platform) {
      bool? adaptive =
          widget.control.adaptive ?? widget.control.parent?.adaptive;
      if (adaptive == true &&
          (platform == TargetPlatform.iOS ||
              platform == TargetPlatform.macOS)) {
        return CupertinoButtonControl(
          control: widget.control,
          //parentDisabled: widget.parentDisabled,
          //parentAdaptive: adaptive,
          //children: widget.children,
          //backend: widget.backend,
        );
      }

      // IconData? icon = parseIcon(widget.control.getString("icon"));
      // IconData? selectedIcon =
      //     parseIcon(widget.control.getString("selectedIcon"));
      Color? iconColor = widget.control.getColor("iconColor", context);
      Color? highlightColor =
          widget.control.getColor("highlightColor", context);
      Color? selectedIconColor =
          widget.control.getColor("selectedIconColor", context);
      Color? bgColor = widget.control.getColor("bgColor", context);
      Color? disabledColor = widget.control.getColor("disabledColor", context);
      Color? hoverColor = widget.control.getColor("hoverColor", context);
      Color? splashColor = widget.control.getColor("splashColor", context);
      Color? focusColor = widget.control.getColor("focusColor", context);
      double? iconSize = widget.control.getDouble("iconSize");
      double? splashRadius = widget.control.getDouble("splashRadius");
      var padding = parseEdgeInsets(widget.control, "padding");
      var alignment = parseAlignment(widget.control, "alignment");
      var sizeConstraints =
          parseBoxConstraints(widget.control, "sizeConstraints");
      // var contentCtrls =
      //     widget.children.where((c) => c.name == "content" && c.visible);
      bool autofocus = widget.control.getBool("autofocus", false)!;
      bool enableFeedback = widget.control.getBool("enableFeedback", true)!;
      bool selected = widget.control.getBool("selected", false)!;
      String url = widget.control.getString("url", "")!;
      String? urlTarget = widget.control.getString("urlTarget");
      bool disabled =
          widget.control.disabled || widget.control.parent!.disabled;
      var mouseCursor =
          parseMouseCursor(widget.control.getString("mouseCursor"));
      var visualDensity =
          parseVisualDensity(widget.control.getString("visualDensity"));

      Function()? onPressed = disabled
          ? null
          : () {
              debugPrint("Button ${widget.control.id} clicked!");
              if (url != "") {
                openWebBrowser(url, webWindowName: urlTarget);
              }
              FletBackend.of(context)
                  .triggerControlEvent(widget.control, "click");
            };

      Widget? button;

      var theme = Theme.of(context);

      var style = parseButtonStyle(Theme.of(context), widget.control, "style",
          defaultForegroundColor: theme.colorScheme.primary,
          defaultBackgroundColor: Colors.transparent,
          defaultOverlayColor: Colors.transparent,
          defaultShadowColor: Colors.transparent,
          defaultSurfaceTintColor: Colors.transparent,
          defaultElevation: 0,
          defaultPadding: const EdgeInsets.all(8),
          defaultBorderSide: BorderSide.none,
          defaultShape: theme.useMaterial3
              ? const StadiumBorder()
              : RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)));

      if (icon != null) {
        button = IconButton(
            autofocus: autofocus,
            focusNode: _focusNode,
            highlightColor: highlightColor,
            disabledColor: disabledColor,
            hoverColor: hoverColor,
            enableFeedback: enableFeedback,
            padding: padding,
            alignment: alignment,
            focusColor: focusColor,
            splashColor: splashColor,
            splashRadius: splashRadius,
            icon: Icon(
              icon,
              color: iconColor,
            ),
            iconSize: iconSize,
            mouseCursor: mouseCursor,
            visualDensity: visualDensity,
            style: style,
            isSelected: selected,
            constraints: sizeConstraints,
            selectedIcon: selectedIcon != null
                ? Icon(selectedIcon, color: selectedIconColor)
                : null,
            onPressed: onPressed);
        // } else if (contentCtrls.isNotEmpty) {
        //   button = IconButton(
        //       autofocus: autofocus,
        //       focusNode: _focusNode,
        //       highlightColor: highlightColor,
        //       disabledColor: highlightColor,
        //       hoverColor: highlightColor,
        //       enableFeedback: enableFeedback,
        //       padding: padding,
        //       alignment: alignment,
        //       focusColor: focusColor,
        //       splashColor: splashColor,
        //       splashRadius: splashRadius,
        //       onPressed: onPressed,
        //       iconSize: iconSize,
        //       mouseCursor: mouseCursor,
        //       visualDensity: visualDensity,
        //       style: style,
        //       isSelected: selected,
        //       constraints: sizeConstraints,
        //       selectedIcon: selectedIcon != null
        //           ? Icon(selectedIcon, color: selectedIconColor)
        //           : null,
        //       icon: createControl(widget.control, contentCtrls.first.id, disabled,
        //           parentAdaptive: widget.parentAdaptive));
      } else {
        return const ErrorControl(
            "IconButton must have either icon or a visible content specified.");
      }

      if (bgColor != null) {
        button = Container(
          decoration:
              ShapeDecoration(color: bgColor, shape: const CircleBorder()),
          child: button,
        );
      }

      var focusValue = widget.control.getString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        _focusNode.requestFocus();
      }

      return ConstrainedControl(control: widget.control, child: button);
    });
  }
}
