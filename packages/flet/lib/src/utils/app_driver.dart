import 'dart:async';

import 'package:flutter/gestures.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../controls/control_widget.dart';
import '../models/control.dart';
import 'keys.dart';

/// Lets a host see and use a running Flet app the way a person would: list
/// the controls on screen, tap them, type into fields.
///
/// Used by embedders (a [FletApp] control's `describe` and `act` methods), for
/// example an AI agent checking an app it just built in a preview.
///
/// Controls are found by walking the element tree under [root] for
/// [ControlWidget]s, so they're reported the way the Python code wrote them:
/// type, `key`, text. Positions are logical pixels relative to [root]'s box,
/// the same space as the app's `page.width` and `page.height`.
class AppDriver {
  AppDriver(this.root);

  /// The element whose subtree is the app, and whose box is the app's area.
  final Element root;

  static int _nextPointer = 0x40000000;
  static final Stopwatch _clock = Stopwatch()..start();

  /// Controls without these are left out of [describe] unless they have a
  /// `key`, events or a tooltip: they're layout and would only be noise.
  static const _inputTypes = {
    "TextField",
    "CupertinoTextField",
    "Checkbox",
    "CupertinoCheckbox",
    "Switch",
    "CupertinoSwitch",
    "Radio",
    "CupertinoRadio",
    "Slider",
    "CupertinoSlider",
    "RangeSlider",
    "Dropdown",
    "DropdownM2",
    "SearchBar",
    "SegmentedButton",
    "CupertinoSegmentedButton",
    "CupertinoSlidingSegmentedControl",
    "AutoComplete",
    "ProgressBar",
    "ProgressRing",
  };

  /// Control types that live on top of the page.
  static const _dialogTypes = {
    "AlertDialog",
    "CupertinoAlertDialog",
    "BottomSheet",
    "CupertinoBottomSheet",
    "CupertinoActionSheet",
    "SnackBar",
    "Banner",
    "DatePicker",
    "TimePicker",
    "CupertinoDatePicker",
    "CupertinoTimerPicker",
    "CupertinoPicker",
    "NavigationDrawer",
    "ContextMenu",
  };

  /// The page and its views fill the app: listing them is only noise.
  static const _containerTypes = {"Page", "View"};

  static const _maxText = 80;

  /// Returns the controls on screen, in tree order.
  ///
  /// Each item: `id`, `type`, `key`, `text`, `value`, `tooltip`, `disabled`,
  /// `events` (the `on_*` handlers the control has), `rect` (`[x, y, w, h]`,
  /// the visible part), `covered` (something else, such as a dialog, is on
  /// top of its centre) and `layer` (`page` or `dialog`). Text drawn by a
  /// control that has no control of its own (a navigation bar's labels, a
  /// date picker's days) is listed with `type` `"label"` and `in`, the id of
  /// the control around it. Password field values are never returned.
  Map<String, dynamic> describe({int maxItems = 100}) {
    final items = _collect();
    return {
      "width": _rootBox?.size.width,
      "height": _rootBox?.size.height,
      "controls": [for (final i in items.take(maxItems)) i.toMap()],
      "truncated": items.length > maxItems,
    };
  }

  /// Runs [steps] in order and stops at the first that fails.
  ///
  /// A step is a map with `action` and its arguments:
  ///
  /// - `tap`, `long_press`: `target`.
  /// - `enter_text`: `target` (a text field), `text`, optional `submit`
  ///   (then the field's submit action runs, as when pressing Enter).
  /// - `tap_at`: `x`, `y` in the app's logical pixels.
  /// - `wait`: `ms`.
  ///
  /// A target is a map with one of `id`, `key`, `text` (exact, then
  /// case-insensitive containing), `tooltip` or `type`, and an optional
  /// `index` among the matches.
  ///
  /// [pointer] is `touch` or `mouse`. Returns `steps`, one result per step
  /// that ran: `status` (`ok`, `not_found`, `covered`, `disabled`,
  /// `read_only`, `not_a_text_field` or `error`), the tap `point`, the `target` that was
  /// used and, when nothing matched, `candidates`.
  Future<Map<String, dynamic>> act(
    List steps, {
    String pointer = "touch",
    Duration targetTimeout = const Duration(seconds: 5),
  }) async {
    final kind =
        pointer == "mouse" ? PointerDeviceKind.mouse : PointerDeviceKind.touch;
    final results = <Map<String, dynamic>>[];
    for (final raw in steps) {
      final step =
          raw is Map ? Map<String, dynamic>.from(raw) : <String, dynamic>{};
      Map<String, dynamic> result;
      try {
        result = await _runStep(
          step,
          kind,
          results.isEmpty ? Duration.zero : targetTimeout,
        );
      } catch (e) {
        result = {"status": "error", "error": e.toString()};
      }
      results.add({"action": step["action"], ...result});
      await _frame();
      if (result["status"] != "ok") break;
    }
    return {"steps": results};
  }

  Future<Map<String, dynamic>> _runStep(
    Map<String, dynamic> step,
    PointerDeviceKind kind,
    Duration targetTimeout,
  ) async {
    final action = step["action"];
    switch (action) {
      case "wait":
        final ms = (step["ms"] as num?)?.toInt() ?? 500;
        await Future.delayed(Duration(milliseconds: ms.clamp(0, 10000)));
        return {"status": "ok"};
      case "tap_at":
        final box = _rootBox;
        if (box == null) {
          return {"status": "error", "error": "The app isn't on screen."};
        }
        final x = (step["x"] as num?)?.toDouble();
        final y = (step["y"] as num?)?.toDouble();
        if (x == null || y == null) {
          return {"status": "error", "error": "tap_at needs x and y."};
        }
        final point = Offset(x, y);
        if (!(Offset.zero & box.size).contains(point)) {
          return {
            "status": "error",
            "error": "($x, $y) is outside the app (${box.size.width.round()}"
                "x${box.size.height.round()}).",
          };
        }
        final global = box.localToGlobal(point);
        if (!_hits(box, global, guest: box)) {
          return {
            "status": "covered",
            "point": [x, y]
          };
        }
        await _tap(global, kind);
        return {
          "status": "ok",
          "point": [x, y],
        };
      case "tap":
      case "long_press":
      case "enter_text":
        var found = _find(step["target"]);
        if (found.failure?["status"] == "not_found" &&
            targetTimeout > Duration.zero) {
          found = await _waitForTarget(step["target"], found, targetTimeout);
        }
        if (found.item == null) return found.failure!;
        final item = found.item!;
        if (item.disabled) {
          return {"status": "disabled", "target": item.summary()};
        }
        final local = item.rect.center;
        final guest = _rootBox!;
        final global = guest.localToGlobal(local);
        if (!_hits(item.hitBox, global, guest: guest)) {
          return {"status": "covered", "target": item.summary()};
        }
        if (action == "enter_text") {
          return _enterText(item, step);
        }
        await _tap(
          global,
          kind,
          hold: action == "long_press"
              ? kLongPressTimeout + const Duration(milliseconds: 100)
              : Duration.zero,
        );
        return {
          "status": "ok",
          "target": item.summary(),
          "point": [_round(local.dx), _round(local.dy)],
        };
      default:
        return {"status": "error", "error": "Unknown action: $action"};
    }
  }

  Future<Map<String, dynamic>> _enterText(
    _Item item,
    Map<String, dynamic> step,
  ) async {
    final editable = _editableIn(item.element);
    if (editable == null) {
      return {"status": "not_a_text_field", "target": item.summary()};
    }
    if (editable.widget.readOnly) {
      return {"status": "read_only", "target": item.summary()};
    }
    final text = (step["text"] ?? "").toString();
    editable.requestKeyboard();
    editable.userUpdateTextEditingValue(
      TextEditingValue(
        text: text,
        selection: TextSelection.collapsed(offset: text.length),
      ),
      SelectionChangedCause.keyboard,
    );
    if (step["submit"] == true) {
      await _frame();
      final w = editable.widget;
      editable.performAction(
        w.textInputAction ??
            (w.maxLines == 1 ? TextInputAction.done : TextInputAction.newline),
      );
    }
    return {"status": "ok", "target": item.summary()};
  }

  // ---------------------------------------------------------------------
  // Finding controls

  RenderBox? get _rootBox {
    final r = root.findRenderObject();
    return r is RenderBox && r.attached && r.hasSize ? r : null;
  }

  List<_Item> _collect() {
    final rootBox = _rootBox;
    if (rootBox == null) return [];
    final view = _viewOf(rootBox);
    final bounds = Offset.zero & rootBox.size;
    final items = <_Item>[];

    void visit(
        Element e, Control? around, RenderBox? aroundBox, _Item? reported) {
      final widget = e.widget;
      if (widget is ControlWidget) {
        final control = widget.control;
        around = control;
        final r = e.findRenderObject();
        aroundBox = r is RenderBox ? r : aroundBox;
        // A Text that only repeats the label of the control around it (a
        // button's or a list tile's) isn't listed again.
        final repeats = control.type == "Text" &&
            reported != null &&
            reported.text != null &&
            reported.text == _clip(_textOf(control));
        if (_interesting(control) && !repeats) {
          final item = _measure(e, control, rootBox, bounds, view);
          if (item != null) {
            items.add(item);
            reported = item;
          }
        }
      } else if (widget is Text || widget is RichText) {
        final text = widget is Text
            ? (widget.data ?? widget.textSpan?.toPlainText())
            : (widget as RichText).text.toPlainText();
        // Text a Flet Text control (or the reported control around it)
        // already shows isn't listed twice.
        if (text != null &&
            text.trim().isNotEmpty &&
            !_isGlyph(text) &&
            around != null &&
            reported?.control?.type != "Text" &&
            reported?.text != _clip(text)) {
          final item = _measure(
            e,
            null,
            rootBox,
            bounds,
            view,
            text: text,
            around: around,
            aroundBox: aroundBox,
          );
          if (item != null) items.add(item);
        }
        return; // a Text's subtree is a RichText
      }
      e.debugVisitOnstageChildren(
          (child) => visit(child, around, aroundBox, reported));
    }

    root.debugVisitOnstageChildren((child) => visit(child, null, null, null));
    return items;
  }

  bool _interesting(Control c) =>
      _containerTypes.contains(c.type) ? c.getKey("key") != null : _listed(c);

  bool _listed(Control c) =>
      c.type == "Text" ||
      _inputTypes.contains(c.type) ||
      _events(c).isNotEmpty ||
      c.getKey("key") != null ||
      c.get("tooltip") is String;

  _Item? _measure(
    Element e,
    Control? control,
    RenderBox rootBox,
    Rect bounds,
    _View? view, {
    String? text,
    Control? around,
    RenderBox? aroundBox,
  }) {
    final r = e.findRenderObject();
    if (r is! RenderBox || !r.attached || !r.hasSize) return null;
    var rect = MatrixUtils.transformRect(
      r.getTransformTo(rootBox),
      Offset.zero & r.size,
    );
    // Only the part inside every scrolling viewport around it is visible.
    RenderObject? p = r.parent;
    while (p != null && p != rootBox) {
      if (p is RenderBox && p.hasSize && p is RenderAbstractViewport) {
        rect = rect.intersect(
          MatrixUtils.transformRect(
            p.getTransformTo(rootBox),
            Offset.zero & p.size,
          ),
        );
      }
      p = p.parent;
    }
    rect = rect.intersect(bounds);
    if (rect.isEmpty || rect.width < 1 || rect.height < 1) return null;
    final owner = control ?? around!;
    final item = _Item(
      control: control,
      element: e,
      box: r,
      rect: rect,
      text: _clip(text ?? (control != null ? _textOf(control) : null)),
      around: control == null ? around?.id : null,
      layer: _inDialog(owner) ? "dialog" : "page",
      // Text inside a control (a field's hint, a tab's label) often isn't
      // hit-testable itself: it's covered when its control is.
      hitBox: control == null ? aroundBox ?? r : r,
    );
    item.covered = !_hits(item.hitBox, rootBox.localToGlobal(rect.center),
        guest: rootBox, view: view);
    return item;
  }

  bool _hits(RenderBox box, Offset global,
      {required RenderBox guest, _View? view}) {
    view ??= _viewOf(guest);
    if (view == null) return false;
    final result = HitTestResult();
    RendererBinding.instance.hitTestInView(result, global, view.id);
    if (!result.path.any((entry) => entry.target == box)) return false;
    // A translucent host overlay can receive the same pointer as the guest.
    // Every render target must belong to the guest or be one of its ancestors.
    for (final entry in result.path) {
      final target = entry.target;
      if (target is RenderObject &&
          !_inSubtree(target, guest) &&
          !_inSubtree(guest, target)) {
        return false;
      }
    }
    return true;
  }

  bool _inSubtree(RenderObject node, RenderObject ancestor) {
    RenderObject? current = node;
    while (current != null && current.depth > ancestor.depth) {
      current = current.parent;
    }
    return current == ancestor;
  }

  _FoundItem _find(dynamic target) {
    if (target is! Map) {
      return _FoundItem.fail({
        "status": "error",
        "error": "A target is needed, e.g. {\"text\": \"Save\"}.",
      });
    }
    final items = _collect();
    List<_Item> matches;
    if (target["id"] != null) {
      final id = (target["id"] as num).toInt();
      matches = items.where((i) => i.control?.id == id).toList();
    } else if (target["key"] != null) {
      final key = target["key"].toString();
      matches = items.where((i) => i.key == key).toList();
    } else if (target["tooltip"] != null) {
      final t = target["tooltip"].toString();
      matches = items.where((i) => i.tooltip == t).toList();
    } else if (target["text"] != null) {
      final t = target["text"].toString();
      matches = items.where((i) => i.text == t || i.value == t).toList();
      if (matches.isEmpty) {
        final low = t.toLowerCase();
        matches = items
            .where((i) => (i.text ?? "").toLowerCase().contains(low))
            .toList();
      }
      // A button over its own label: tap the control that handles it.
      matches.sort(
        (a, b) => (b.events.isNotEmpty ? 1 : 0).compareTo(
          a.events.isNotEmpty ? 1 : 0,
        ),
      );
    } else if (target["type"] != null) {
      final t = target["type"].toString();
      matches = items.where((i) => i.control?.type == t).toList();
    } else {
      return _FoundItem.fail({
        "status": "error",
        "error": "A target needs one of id, key, text, tooltip or type.",
      });
    }
    // On top first: with a dialog open, "OK" means the dialog's button.
    final onTop = matches.where((i) => i.layer == "dialog").toList();
    if (onTop.isNotEmpty) {
      matches = [...onTop, ...matches.where((i) => i.layer != "dialog")];
    }
    final index = (target["index"] as num?)?.toInt() ?? 0;
    if (index < 0 || index >= matches.length) {
      return _FoundItem.fail({
        "status": "not_found",
        "matches": matches.length,
        "candidates": _candidates(items, target),
      });
    }
    return _FoundItem(matches[index]);
  }

  // A previous step's Python handler can add the target after the next frame.
  // Inspect frames the guest actually renders, even if the first arrives late.
  Future<_FoundItem> _waitForTarget(
      dynamic target, _FoundItem last, Duration timeout) {
    final result = Completer<_FoundItem>();
    final timer = Timer(timeout, () => result.complete(last));
    void afterFrame(Duration _) {
      if (result.isCompleted) return;
      try {
        if (root.mounted) last = _find(target);
        if (root.mounted && last.failure?["status"] == "not_found") {
          SchedulerBinding.instance.addPostFrameCallback(afterFrame);
        } else {
          result.complete(last);
        }
      } catch (error, stack) {
        result.completeError(error, stack);
      }
    }

    SchedulerBinding.instance.addPostFrameCallback(afterFrame);
    return result.future.whenComplete(timer.cancel);
  }

  List<Map<String, dynamic>> _candidates(List<_Item> items, Map target) {
    final words = [
      for (final v in [
        target["text"],
        target["key"],
        target["tooltip"],
        target["type"],
      ])
        if (v != null) ...v.toString().toLowerCase().split(RegExp(r"\W+")),
    ].where((w) => w.length > 1).toSet();
    return items
        .where((i) {
          final hay = [
            i.text,
            i.key,
            i.tooltip,
            i.control?.type,
          ].whereType<String>().join(" ").toLowerCase();
          return words.any(hay.contains);
        })
        .take(3)
        .map((i) => i.summary())
        .toList();
  }

  EditableTextState? _editableIn(Element element) {
    EditableTextState? found;
    void visit(Element e) {
      if (found != null) return;
      if (e is StatefulElement && e.state is EditableTextState) {
        found = e.state as EditableTextState;
        return;
      }
      e.visitChildElements(visit);
    }

    visit(element);
    return found;
  }

  // ---------------------------------------------------------------------
  // Pointer events

  Future<void> _tap(
    Offset global,
    PointerDeviceKind kind, {
    Duration hold = Duration.zero,
  }) async {
    final view = _viewOf(_rootBox!);
    final viewId = view?.id ?? 0;
    final binding = GestureBinding.instance;
    final pointer = _nextPointer++;
    final device = pointer;
    Duration now() => _clock.elapsed;
    if (kind == PointerDeviceKind.mouse) {
      binding.handlePointerEvent(
        PointerAddedEvent(
          viewId: viewId,
          timeStamp: now(),
          kind: kind,
          device: device,
          position: global,
        ),
      );
      binding.handlePointerEvent(
        PointerHoverEvent(
          viewId: viewId,
          timeStamp: now(),
          kind: kind,
          device: device,
          position: global,
        ),
      );
    }
    binding.handlePointerEvent(
      PointerDownEvent(
        viewId: viewId,
        timeStamp: now(),
        pointer: pointer,
        kind: kind,
        device: device,
        position: global,
        buttons: kPrimaryButton,
      ),
    );
    await Future.delayed(
      hold > Duration.zero ? hold : const Duration(milliseconds: 30),
    );
    binding.handlePointerEvent(
      PointerUpEvent(
        viewId: viewId,
        timeStamp: now(),
        pointer: pointer,
        kind: kind,
        device: device,
        position: global,
      ),
    );
    if (kind == PointerDeviceKind.mouse) {
      binding.handlePointerEvent(
        PointerRemovedEvent(
          viewId: viewId,
          timeStamp: now(),
          kind: kind,
          device: device,
          position: global,
        ),
      );
    }
  }

  static Future<void> _frame() {
    SchedulerBinding.instance.scheduleFrame();
    return SchedulerBinding.instance.endOfFrame;
  }

  static _View? _viewOf(RenderObject r) {
    RenderObject? p = r;
    while (p != null && p is! RenderView) {
      p = p.parent;
    }
    return p is RenderView ? _View(p.flutterView.viewId) : null;
  }

  // ---------------------------------------------------------------------
  // Control properties

  static List<String> _events(Control c) => [
        for (final e in c.properties.entries)
          if (e.key.startsWith("on_") && e.value == true) e.key.substring(3),
      ];

  static bool _inDialog(Control c) {
    Control? p = c;
    while (p != null) {
      if (_dialogTypes.contains(p.type)) return true;
      p = p.parent;
    }
    return false;
  }

  /// What a person would read on the control: its label, or the first Text
  /// inside it.
  static String? _textOf(Control c) {
    if (c.type == "Text") return _string(c.properties["value"]);
    for (final p in const ["text", "label", "title", "content", "hint_text"]) {
      final s = _string(c.properties[p]);
      if (s != null) return s;
    }
    for (final p in const ["content", "title", "label", "text", "leading"]) {
      final s = _firstText(c.properties[p], 3);
      if (s != null) return s;
    }
    return null;
  }

  static String? _firstText(dynamic v, int depth) {
    if (depth < 0) return null;
    if (v is List) {
      for (final x in v) {
        final s = _firstText(x, depth);
        if (s != null) return s;
      }
      return null;
    }
    if (v is! Control) return null;
    final c = v.unwrapComponent();
    if (c == null || !c.visible) return null;
    if (c.type == "Text") return _string(c.properties["value"]);
    for (final p in const ["content", "controls", "title", "label", "text"]) {
      final s = _firstText(c.properties[p], depth - 1);
      if (s != null) return s;
    }
    return null;
  }

  /// An icon drawn from an icon font: only private-use characters.
  static bool _isGlyph(String s) =>
      s.trim().runes.every((r) => (r >= 0xE000 && r <= 0xF8FF) || r >= 0xF0000);

  static String? _string(dynamic v) =>
      v is String && v.trim().isNotEmpty ? v : null;

  static String? _clip(String? s) {
    if (s == null) return null;
    final one = s.replaceAll(RegExp(r"\s+"), " ").trim();
    return one.length > _maxText ? "${one.substring(0, _maxText - 1)}…" : one;
  }

  static num _round(double v) => (v * 10).round() / 10;
}

class _View {
  const _View(this.id);
  final int id;
}

class _FoundItem {
  _FoundItem(this.item) : failure = null;
  _FoundItem.fail(this.failure) : item = null;
  final _Item? item;
  final Map<String, dynamic>? failure;
}

class _Item {
  _Item({
    required this.control,
    required this.element,
    required this.box,
    required this.rect,
    required this.text,
    required this.around,
    required this.layer,
    required this.hitBox,
  });

  final Control? control; // null for a label
  final Element element;
  final RenderBox box;
  final Rect rect;
  final String? text;
  final int? around;
  final String layer;
  final RenderBox hitBox;
  bool covered = false;

  String? get key => control?.getKey("key")?.value.toString();

  String? get tooltip {
    final t = control?.get("tooltip");
    return t is String ? t : null;
  }

  List<String> get events =>
      control == null ? const [] : AppDriver._events(control!);

  bool get disabled => control?.disabled ?? false;

  /// The control's current value: a field's text, a checkbox's state. Never
  /// a password.
  dynamic get value {
    final c = control;
    if (c == null || c.type == "Text") return null;
    if (c.get<bool>("password") == true) return null;
    final v = c.properties["value"];
    if (v is String) return AppDriver._clip(v);
    return v is num || v is bool ? v : null;
  }

  Map<String, dynamic> summary() => {
        if (control != null) "id": control!.id,
        "type": control?.type ?? "label",
        if (key != null) "key": key,
        if (text != null) "text": text,
      };

  Map<String, dynamic> toMap() => {
        ...summary(),
        if (around != null) "in": around,
        if (value != null) "value": value,
        if (tooltip != null) "tooltip": tooltip,
        if (disabled) "disabled": true,
        if (events.isNotEmpty) "events": events,
        "rect": [
          AppDriver._round(rect.left),
          AppDriver._round(rect.top),
          AppDriver._round(rect.width),
          AppDriver._round(rect.height),
        ],
        if (covered) "covered": true,
        if (layer != "page") "layer": layer,
      };
}
