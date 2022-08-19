import 'dart:convert';

import 'package:flet/src/models/control_type.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flet/src/models/control.dart';

void main() {
  test("Two controls are equal", () {
    Control c1 = const Control(
        id: "i1",
        pid: "p1",
        type: ControlType.stack,
        name: null,
        childIds: ["txt1", "btn1"],
        attrs: {"text": "Hello!", "width": "200"});

    Control c2 = const Control(
        id: "i1",
        pid: "p1",
        type: ControlType.stack,
        name: null,
        childIds: ["txt1", "btn1"],
        attrs: {"width": "200", "text": "Hello!"});

    expect(c1 == c2, true);
  });

  test('Deserialize control', () {
    const t1 = '''{
        "t": "stack",
        "p": "",
        "i": "s1",
        "n": "content",
        "c": ["txt1", "txt2"],
        "at": "0",
        "value": "Hello, world!"
      }''';

    final j1 = json.decode(t1);
    final c1 = Control.fromJson(j1);

    expect(c1.id, "s1");
    expect(c1.pid, "");
    expect(c1.type, ControlType.stack);
    expect(c1.name, "content");
    expect(c1.childIds, ["txt1", "txt2"]);
    expect(c1.attrs.length, 2);
    expect(c1.attrs["at"], "0");
    expect(c1.attrs["value"], "Hello, world!");
  });
}
