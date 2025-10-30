import 'dart:async';

import 'package:collection/collection.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/keys.dart';
import '../utils/popup_menu.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class ContextMenuRegionControl extends StatefulWidget {
  final Control control;

  const ContextMenuRegionControl({super.key, required this.control});

  @override
  State<ContextMenuRegionControl> createState() =>
      _ContextMenuRegionControlState();
}

class _ContextMenuRegionControlState extends State<ContextMenuRegionControl> {
  ContextMenuTrigger _primaryTrigger = ContextMenuTrigger.disabled;
  ContextMenuTrigger _secondaryTrigger = ContextMenuTrigger.down;
  ContextMenuTrigger _tertiaryTrigger = ContextMenuTrigger.down;

  Future<String?>? _pendingMenu;

  @override
  Widget build(BuildContext context) {
    debugPrint("ContextMenuRegion build: ${widget.control.id}");

    var content = widget.control.buildWidget("content");
    if (content == null) {
      return const ErrorControl("ContextMenuRegion.content must be visible");
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
      button,
      globalPosition: event.position,
      localPosition: event.localPosition,
    );
  }

  void _handleLongPress(
      _MouseButton button, Offset globalPosition, Offset localPosition) {
    final trigger = _getTriggerFromButton(button);
    if (trigger != ContextMenuTrigger.longPress) return;

    _showMenu(
      button,
      globalPosition: globalPosition,
      localPosition: localPosition,
    );
  }

  ContextMenuTrigger _getTriggerFromButton(_MouseButton button) {
    switch (button) {
      case _MouseButton.primary:
        return _primaryTrigger;
      case _MouseButton.secondary:
        return _secondaryTrigger;
      case _MouseButton.tertiary:
        return _tertiaryTrigger;
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

  List<Control> _getPopupItemsFromButton(_MouseButton button) {
    List<Control> items;
    switch (button) {
      case _MouseButton.primary:
        items = widget.control.children("primary_items");
        break;
      case _MouseButton.secondary:
        items = widget.control.children("secondary_items");
        break;
      case _MouseButton.tertiary:
        items = widget.control.children("tertiary_items");
        break;
    }

    return items.isEmpty ? items = widget.control.children("items") : items;
  }

  Map<String, dynamic> _eventPayload(
      _MouseButton button, Offset globalPosition, Offset? localPosition,
      {int? itemId,
      String? itemControlId,
      int? itemIndex,
      Object? itemKey,
      int? itemCount}) {
    return {
      "b": button.name,
      "tr": _getTriggerFromButton(button).name,
      "iid": itemId,
      "cid": itemControlId,
      "idx": itemIndex,
      "key": itemKey,
      "ic": itemCount,
      "g": {"x": globalPosition.dx, "y": globalPosition.dy},
      "l": localPosition != null
          ? {"x": localPosition.dx, "y": localPosition.dy}
          : null,
    };
  }

  Future<void> _showMenu(_MouseButton button,
      {required Offset globalPosition, Offset? localPosition}) async {
    if (_pendingMenu != null) {
      Navigator.of(context).pop();
      await _pendingMenu;
      if (!mounted) return;
    }

    final overlayState = Overlay.of(context);
    final overlayRenderBox =
        overlayState.context.findRenderObject() as RenderBox?;
    if (overlayRenderBox == null || !overlayRenderBox.hasSize) {
      return;
    }

    final overlayOffset = overlayRenderBox.globalToLocal(globalPosition);
    final position = RelativeRect.fromLTRB(
      overlayOffset.dx,
      overlayOffset.dy,
      overlayRenderBox.size.width - overlayOffset.dx,
      overlayRenderBox.size.height - overlayOffset.dy,
    );

    final basePayload = _eventPayload(button, globalPosition, localPosition);

    widget.control.triggerEvent("request", basePayload);

    final popupItems = _getPopupItemsFromButton(button)
        .where((c) => c.type == "PopupMenuItem")
        .toList(growable: false);
    final entries = buildPopupMenuEntries(context, popupItems);
    basePayload.addAll({"ic": entries.length});

    // If there are no menu items, trigger the dismiss event and return.
    if (entries.isEmpty) {
      widget.control.triggerEvent("dismiss", basePayload);
      return;
    }

    widget.control.triggerEvent("open", basePayload);

    final menuFuture = showMenu<String>(
      context: context,
      position: position,
      items: entries,
    );
    _pendingMenu = menuFuture;
    final selection = await menuFuture;

    if (!mounted) return;

    _pendingMenu = null;

    if (selection != null) {
      final selectedControl = popupItems
          .firstWhereOrNull((item) => item.id.toString() == selection);
      final itemId = parseInt(selection);
      final controlKey = selectedControl?.getKey("key");
      widget.control.triggerEvent(
          "select",
          _eventPayload(
            button,
            globalPosition,
            localPosition,
            itemId: itemId,
            itemControlId: selection,
            itemKey: controlKey?.value,
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
