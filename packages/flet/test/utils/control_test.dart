import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

var backend = FletBackend(
    pageUri: Uri.parse("uri"), assetsDir: "", extensions: [], multiView: false);

void main() {
  test("Both controls must be equal", () {
    var c1 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
          "b": 2,
          "c": {"c_0": "test"}
        },
        backend: backend);
    var c2 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
          "b": 2,
          "c": {"c_0": "test"}
        },
        backend: backend);
    expect(c1 == c2, true);
  });

  test("Update control with a Map", () {
    var c1 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
          "b": 2,
          "c": {"c_0": "test"}
        },
        backend: backend);
    bool changed = c1.update({
      "a": 10,
      "d": true,
      "c": {"c_0": "test_2", "sub_1": "something"}
    });
    expect(changed, true);
    expect(c1.properties["a"] == 10, true);
    expect(c1.properties["b"] == 2, true);
    expect(c1.properties["d"], true);
    expect(c1.properties["c"]["c_0"] == "test_2", true);
    expect(c1.properties["c"]["sub_1"] == "something", true);
  });

  test("updateControl did not change control", () {
    var a1 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
          "b": 2,
          "c": {"c_0": "test"}
        },
        backend: backend);
    bool changed = a1.update({
      "a": 1,
      "b": 2,
      "c": {"c_0": "test"}
    });
    expect(changed, false);
  });

  test("updateControl on 1st level changed control", () {
    var a1 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
        },
        backend: backend);
    bool changed = a1.update({
      "a": 2,
    });
    expect(changed, true);
  });

  test("updateControl on 2nd level changed control", () {
    var a1 = Control(
        id: 1,
        type: "Button",
        properties: {
          "a": 1,
          "c": {"c_0": "test"}
        },
        backend: backend);
    bool changed = a1.update({
      "c": {"c_0": "changed!"}
    });
    expect(changed, true);
  });

  test("unwrapComponent resolves nested component bodies", () {
    var button = Control(
        id: 3, type: "Button", properties: {"text": "ok"}, backend: backend);
    var inner =
        Control(id: 2, type: "C", properties: {"_b": button}, backend: backend);
    var outer =
        Control(id: 1, type: "C", properties: {"_b": inner}, backend: backend);
    expect(outer.unwrapComponent(), button);
  });

  test("unwrapComponent returns null for a component with no body", () {
    // A re-rendering component is patched to a null body first and receives
    // its new body in a follow-up message; a frame drawn in between must not
    // crash.
    var c =
        Control(id: 1, type: "C", properties: {"_b": null}, backend: backend);
    expect(c.unwrapComponent(), isNull);
  });

  test("children skips components with no body", () {
    var text = Control(
        id: 2, type: "Text", properties: {"value": "hi"}, backend: backend);
    var pending =
        Control(id: 3, type: "C", properties: {"_b": null}, backend: backend);
    var column = Control(
        id: 1,
        type: "Column",
        properties: {
          "controls": [text, pending]
        },
        backend: backend);
    expect(column.children("controls"), [text]);
  });
}
