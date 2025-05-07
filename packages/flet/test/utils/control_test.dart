import 'package:flet/flet.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Both controls must be equal", () {
    var backend = FletBackend(
        pageUri: Uri.parse("uri"),
        assetsDir: "",
        extensions: [],
        multiView: false);
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
}
