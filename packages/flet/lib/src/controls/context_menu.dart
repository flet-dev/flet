import 'dart:async';

import 'package:collection/collection.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/popup_menu.dart';
import '../utils/transforms.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ContextMenuControl extends StatefulWidget {
  final Control control;

  const ContextMenuControl({super.key, required this.control});

  @override
  State<ContextMenuControl> createState() => _ContextMenuControlState();
}

class _ContextMenuControlState extends State<ContextMenuControl> {
  ContextMenuTrigger _primaryTrigger = ContextMenuTrigger.disabled;
  ContextMenuTrigger _secondaryTrigger = ContextMenuTrigger.down;
  ContextMenuTrigger _tertiaryTrigger = ContextMenuTrigger.down;

  Future<String?>? _pendingMenu;

  @override
  void initState() {
    super.initState();
    // Allow backend code to invoke methods on this control instance.
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ContextMenu build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("ContextMenu.content must be visible");
    }

    _primaryTrigger = parseContextMenuTrigger(
        widget.control.getString("primary_trigger"),
        ContextMenuTrigger.disabled)!;
    _secondaryTrigger = parseContextMenuTrigger(
        widget.control.getString("secondary_trigger"),
        ContextMenuTrigger.down)!;
    _tertiaryTrigger = parseContextMenuTrigger(
        widget.control.getString("tertiary_trigger"), ContextMenuTrigger.down)!;

    Widget result = GestureDetector(
      behavior: HitTestBehavior.deferToChild,
      onLongPressStart: _primaryTrigger == ContextMenuTrigger.longPress
          ? (LongPressStartDetails details) => _handleLongPress(
                _MouseButton.primary,
                details.globalPosition,
                details.localPosition,
              )
          : null,
      onSecondaryLongPressStart:
          _secondaryTrigger == ContextMenuTrigger.longPress
              ? (LongPressStartDetails details) => _handleLongPress(
                    _MouseButton.secondary,
                    details.globalPosition,
                    details.localPosition,
                  )
              : null,
      onTertiaryLongPressStart: _tertiaryTrigger == ContextMenuTrigger.longPress
          ? (LongPressStartDetails details) => _handleLongPress(
                _MouseButton.tertiary,
                details.globalPosition,
                details.localPosition,
              )
          : null,
      child: Listener(
        behavior: HitTestBehavior.translucent,
        onPointerDown: _handlePointerDown,
        child: content,
      ),
    );

    return LayoutControl(control: widget.control, child: result);
  }

  /// Handles pointer down events to determine if a context menu should be shown.
  /// Only responds to mouse events and triggers the menu if the configured trigger is `down`.
  void _handlePointerDown(PointerDownEvent event) {
    if (event.kind != PointerDeviceKind.mouse) return;

    final button = _mouseButtonFromEvent(event.buttons);
    if (button == null) return;

    final trigger = _getTriggerFromButton(button);
    if (trigger != ContextMenuTrigger.down) return;

    _showMenu(
      button: button,
      globalPosition: event.position,
      localPosition: event.localPosition,
    );
  }

  void _handleLongPress(
      _MouseButton button, Offset globalPosition, Offset localPosition) {
    final trigger = _getTriggerFromButton(button);
    if (trigger != ContextMenuTrigger.longPress) return;

    _showMenu(
      button: button,
      globalPosition: globalPosition,
      localPosition: localPosition,
    );
  }

  ContextMenuTrigger? _getTriggerFromButton(_MouseButton? button) {
    switch (button) {
      case _MouseButton.primary:
        return _primaryTrigger;
      case _MouseButton.secondary:
        return _secondaryTrigger;
      case _MouseButton.tertiary:
        return _tertiaryTrigger;
      default:
        return null;
    }
  }

  /// Returns the corresponding [_MouseButton] based on the
  /// given button bitmask, and `null` if no recognized button is pressed.
  _MouseButton? _mouseButtonFromEvent(int buttons) {
    if ((buttons & kPrimaryButton) != 0) {
      return _MouseButton.primary;
    } else if ((buttons & kSecondaryMouseButton) != 0) {
      return _MouseButton.secondary;
    } else if ((buttons & kTertiaryButton) != 0) {
      return _MouseButton.tertiary;
    }
    return null;
  }

  /// Picks popup menu items configured for the provided button, falling back
  /// to the shared `items` collection when a button-specific list is empty.
  List<Control> _getPopupItemsFromButton(_MouseButton? button) {
    switch (button) {
      case _MouseButton.primary:
        return widget.control.children("primary_items");
      case _MouseButton.secondary:
        return widget.control.children("secondary_items");
      case _MouseButton.tertiary:
        return widget.control.children("tertiary_items");
      default:
        return widget.control.children("items");
    }
  }

  /// Serialises menu event data to a compact payload sent to Python handlers.
  Map<String, dynamic> _eventPayload(
      _MouseButton? button, Offset globalPosition, Offset? localPosition,
      {int? itemId, int? itemIndex, int? itemCount}) {
    return {
      "b": button?.name,
      "tr": _getTriggerFromButton(button)?.name,
      "id": itemId,
      "idx": itemIndex,
      "ic": itemCount,
      "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      "l": localPosition != null
          ? {"x": localPosition.dx, "y": localPosition.dy}
          : null,
    };
  }

  /// Opens the context menu for a specific button at the requested position.
  Future<void> _showMenu(
      {required Offset globalPosition,
      Offset? localPosition,
      _MouseButton? button}) async {
    // If a menu is already open, close it and wait for it to finish.
    if (_pendingMenu != null) {
      Navigator.of(context).pop();
      await _pendingMenu;
      if (!mounted) return;
    }

    // Get the overlay state and its render box for positioning the menu.
    final overlayState = Overlay.of(context, rootOverlay: true);
    final overlayRenderBox =
        overlayState.context.findRenderObject() as RenderBox?;
    if (overlayRenderBox == null || !overlayRenderBox.hasSize) return;

    // Calculate the position for the popup menu relative to the overlay.
    final overlayOffset = overlayRenderBox.globalToLocal(globalPosition);
    final position = RelativeRect.fromLTRB(
      overlayOffset.dx,
      overlayOffset.dy,
      overlayRenderBox.size.width - overlayOffset.dx,
      overlayRenderBox.size.height - overlayOffset.dy,
    );

    // Build popup menu entries.
    final popupItems = _getPopupItemsFromButton(button).toList(growable: false);
    final entries = buildPopupMenuEntries(popupItems, context);

    // Prepare event payload for menu events.
    final basePayload = _eventPayload(button, globalPosition, localPosition,
        itemCount: entries.length);

    // If there are no menu entries, send dismiss event.
    if (entries.isEmpty) {
      widget.control.triggerEvent("dismiss", basePayload);
      return;
    }

    // Notify that the menu is opening.
    widget.control.triggerEvent("open", basePayload);

    // Show the popup menu and wait for user selection.
    final menuFuture = showMenu<String>(
      context: context,
      position: position,
      items: entries,
    );
    _pendingMenu = menuFuture;
    final selection = await menuFuture;

    if (!mounted) return;
    _pendingMenu = null;

    // Handle the user's selection or dismissal.
    if (selection != null) {
      final selectedControl = popupItems
          .firstWhereOrNull((item) => item.id.toString() == selection);
      widget.control.triggerEvent(
          "select",
          _eventPayload(
            button,
            globalPosition,
            localPosition,
            itemId: parseInt(selection),
            itemCount: popupItems.length,
            itemIndex: selectedControl != null
                ? popupItems.indexOf(selectedControl)
                : null,
          ));
    } else {
      widget.control.triggerEvent(
          "dismiss",
          _eventPayload(
            button,
            globalPosition,
            localPosition,
            itemCount: popupItems.length,
          ));
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "open":
        // Get the render box for positioning the context menu.
        final renderBox = context.findRenderObject() as RenderBox?;
        if (renderBox == null || !renderBox.hasSize) {
          throw StateError(
              "ContextMenu render box is not ready to display a menu.");
        }

        var globalPosition = parseOffset(args["global_position"]);
        var localPosition = parseOffset(args["local_position"]);

        // If only local position is provided, obtain global position from it.
        if (globalPosition == null && localPosition != null) {
          globalPosition = renderBox.localToGlobal(localPosition);
        }
        // If only global position is provided, obtain local position from it.
        else if (globalPosition != null && localPosition == null) {
          localPosition = renderBox.globalToLocal(globalPosition);
        }

        // Default to center of the render box if positions are missing.
        localPosition ??= renderBox.size.center(Offset.zero);
        globalPosition ??= renderBox.localToGlobal(localPosition);

        // Show the context menu at the calculated position.
        _showMenu(globalPosition: globalPosition, localPosition: localPosition);
        return null;
      default:
        throw ArgumentError("Unsupported method: $name");
    }
  }
}

enum _MouseButton { primary, secondary, tertiary }

enum ContextMenuTrigger { disabled, down, longPress }

ContextMenuTrigger? parseContextMenuTrigger(String? value,
    [ContextMenuTrigger? defaultValue]) {
  if (value == null) return defaultValue;
  return ContextMenuTrigger.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
