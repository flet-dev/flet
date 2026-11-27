import 'dart:typed_data';

import 'package:flet/src/host_requests.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  late List<List<dynamic>> sent;
  late HostRequests requests;

  setUp(() {
    sent = [];
    requests = HostRequests(
        send: (id, name, args) => sent.add([id, name, args]),
        maxPending: 2,
        maxArgsSize: 100);
  });

  test("a request is sent and completed with the host's result", () async {
    final reply = requests.request("fletbase.oauth", {"provider": "google"});
    expect(sent.single.sublist(1), [
      "fletbase.oauth",
      {"provider": "google"}
    ]);
    expect(
        requests.complete(sent.single[0], {
          "result": {"fb_code": "c"}
        }),
        isTrue);
    expect(await reply, {
      "result": {"fb_code": "c"}
    });
    expect(requests.pendingCount, 0);
  });

  test("the host's error keeps its kind; an unknown kind is failed", () async {
    final refused = requests.request("a", null);
    final odd = requests.request("b", null);
    requests.complete(sent[0][0], {
      "error": {"kind": "refused", "message": "No"}
    });
    requests.complete(sent[1][0], {
      "error": {"kind": "whatever", "message": "x"}
    });
    expect(await refused, hostRequestError("refused", "No"));
    expect(await odd, hostRequestError("failed", "x"));
  });

  test("an unknown or repeated id is ignored", () async {
    final reply = requests.request("a", null);
    expect(requests.complete(sent.single[0] + 1000, {"result": 1}), isFalse);
    expect(requests.complete(sent.single[0], {"result": 2}), isTrue);
    expect(requests.complete(sent.single[0], {"result": 3}), isFalse);
    expect(await reply, {"result": 2});
  });

  test("ids are unique across instances", () {
    final other = HostRequests(send: (id, name, args) => sent.add([id]));
    requests.request("a", null);
    other.request("a", null);
    expect(sent[0][0], isNot(sent[1][0]));
    // A reply for one instance's id doesn't complete the other's request.
    expect(other.complete(sent[0][0], {"result": 1}), isFalse);
  });

  test("a request times out, and a late reply is dropped", () async {
    final reply =
        requests.request("a", null, timeout: const Duration(milliseconds: 10));
    expect((await reply)["error"]["kind"], "timeout");
    expect(requests.complete(sent.single[0], {"result": 1}), isFalse);
    expect(requests.pendingCount, 0);
  });

  test("too many pending requests fail without reaching the host", () async {
    requests.request("a", null);
    requests.request("b", null);
    final third = await requests.request("c", null);
    expect(third["error"]["kind"], "failed");
    expect(sent.length, 2);
  });

  test("large args and an empty name fail without reaching the host", () async {
    expect((await requests.request("a", "x" * 101))["error"]["kind"], "failed");
    expect(
        (await requests.request("a", {"b": Uint8List(200)}))["error"]["kind"],
        "failed");
    expect((await requests.request("", null))["error"]["kind"], "failed");
    expect(sent, isEmpty);
  });

  test("cancelAll fails every pending request", () async {
    final a = requests.request("a", null);
    final b =
        requests.request("b", null, timeout: const Duration(milliseconds: 50));
    requests.cancelAll("unhandled", "The app was closed.");
    expect(await a, hostRequestError("unhandled", "The app was closed."));
    expect(await b, hostRequestError("unhandled", "The app was closed."));
    expect(requests.pendingCount, 0);
  });
}
