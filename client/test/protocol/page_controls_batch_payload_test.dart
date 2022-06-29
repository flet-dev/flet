import 'dart:convert';

import 'package:flet_view/protocol/page_controls_batch_payload.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("PageControlsBatchPayload serialize to message", () {
    const myJsonAsString = '''[
      {"action":"updateControlProps","payload":{"props":[{"i":"page","width":"100","height":"200"},{"i":"txt1","value":"Hello, world!"}]}},
      {"action":"removeControl","payload":{"ids":["a1", "b2"]}}
    ]
    ''';

    final s = PageControlsBatchPayload.fromJson(json.decode(myJsonAsString));
    expect(s.messages.length, 2);
  });
}
