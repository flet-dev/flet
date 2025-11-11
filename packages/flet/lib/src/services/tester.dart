import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import '../utils/keys.dart';

class TesterService extends FletService {
  TesterService({required super.control});
  final Map<int, TestFinder> _finders = {};

  @override
  void init() {
    super.init();
    debugPrint("Tester(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void dispose() {
    debugPrint("Tester(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Tester.$name($args)");
    switch (name) {
      case "pump":
        await control.backend.tester!
            .pump(duration: parseDuration(args["duration"]));

      case "pump_and_settle":
        await control.backend.tester!
            .pumpAndSettle(duration: parseDuration(args["duration"]));

      case "find_by_text":
        var finder = control.backend.tester!.findByText(args["text"]);
        _finders[finder.id] = finder;
        return finder.toMap();

      case "find_by_text_containing":
        var finder =
            control.backend.tester!.findByTextContaining(args["pattern"]);
        _finders[finder.id] = finder;
        return finder.toMap();

      case "find_by_key":
        var controlKey = parseKey(args["key"])!;
        var key = controlKey is ControlScrollKey
            ? control.backend.globalKeys[controlKey.toString()]
            : ValueKey(controlKey.value);
        if (key == null) {
          throw Exception("Key not found: $key");
        }
        var finder = control.backend.tester!.findByKey(key);
        _finders[finder.id] = finder;
        return finder.toMap();

      case "find_by_tooltip":
        var finder = control.backend.tester!.findByTooltip(args["value"]);
        _finders[finder.id] = finder;
        return finder.toMap();

      case "find_by_icon":
        var iconCode = args["icon"];
        var icon = parseIconData(iconCode, control.backend);
        if (icon == null) {
          throw Exception("Icon not found: $iconCode");
        }
        var finder = control.backend.tester!.findByIcon(icon);
        _finders[finder.id] = finder;
        return finder.toMap();

      case "take_screenshot":
        return await control.backend.tester!.takeScreenshot(args["name"]);

      case "tap":
        var finder = _finders[args["finder_id"]];
        if (finder != null) {
          await control.backend.tester!.tap(finder, args["finder_index"]);
        }

      case "long_press":
        var finder = _finders[args["finder_id"]];
        if (finder != null) {
          await control.backend.tester!.longPress(finder, args["finder_index"]);
        }

      case "enter_text":
        var finder = _finders[args["finder_id"]];
        if (finder != null) {
          await control.backend.tester!
              .enterText(finder, args["finder_index"], args["text"]);
        }

      case "mouse_hover":
        var finder = _finders[args["finder_id"]];
        if (finder != null) {
          await control.backend.tester!
              .mouseHover(finder, args["finder_index"]);
        }

      case "teardown":
        control.backend.tester?.teardown();

      default:
        throw Exception("Unknown Tester method: $name");
    }
  }
}
