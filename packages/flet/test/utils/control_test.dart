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

  test("applyPatch ADD creates missing intermediate map", () {
    var c1 = Control(
        id: 1,
        type: "Button",
        properties: {"content": "Click me"},
        backend: backend);

    c1.applyPatch([
      [
        0,
        {"_internals": [1]}
      ],
      [
        1,
        1,
        "style",
        {
          "bgcolor": "green",
        }
      ]
    ], backend);

    expect(c1.properties["_internals"], isA<Map>());
    expect(c1.properties["_internals"]["style"]["bgcolor"], "green");
  });
}
