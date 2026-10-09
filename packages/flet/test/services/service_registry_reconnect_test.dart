/// A reconnect snapshot must preserve service state and in-flight invocations.
library;

import 'dart:async';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flet/src/services/service_registry.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

const _registryId = 7;
const _pickerId = 9;

class _FakeChannel implements FletBackendChannel {
  final List<Uint8List> sent = [];
  late FletBackendChannelOnPacketCallback _onPacket;

  FletBackendChannelBuilder get builder => ({
        required FletBackendChannelOnPacketCallback onPacket,
        required FletBackendChannelOnDisconnectCallback onDisconnect,
      }) {
        _onPacket = onPacket;
        return this;
      };

  void receive(MessageAction action, Map<String, dynamic> payload) {
    final body = msgpack.serialize([action.value, payload]);
    _onPacket(Uint8List.fromList([0x00, ...body]));
  }

  List<Map> get invokeResponses => sent
      .where((p) => p.isNotEmpty && p[0] == 0x00)
      .map((p) => msgpack.deserialize(Uint8List.sublistView(p, 1)) as List)
      .where((m) => m[0] == MessageAction.invokeControlMethod.value)
      .map((m) => m[1] as Map)
      .toList();

  @override
  Future connect() async {}
  @override
  bool get isLocalConnection => true;
  @override
  int get defaultReconnectIntervalMs => 0;
  @override
  void send(Uint8List packet) => sent.add(Uint8List.fromList(packet));
  @override
  void disconnect() {}
}

/// Mimics FilePickerService: `pick` stores a selection, `upload` needs it.
class _PickerLike extends FletService {
  _PickerLike({required super.control});
  Completer<void>? dialog;
  List<String>? files;
  int inits = 0;
  int disposals = 0;
  int updates = 0;

  @override
  void update() {
    updates++;
  }

  @override
  void init() {
    super.init();
    inits++;
    control.addInvokeMethodListener(_invoke);
  }

  @override
  void dispose() {
    disposals++;
    control.removeInvokeMethodListener(_invoke);
    super.dispose();
  }

  Future<dynamic> _invoke(String name, dynamic args) async {
    if (name == "pick_files") {
      dialog = Completer<void>();
      await dialog!.future; // user is choosing a file
      files = args["cancel"] == true ? [] : ["sample.txt"];
      return files;
    }
    if (name == "upload") {
      if (files == null) throw Exception("selection lost");
      return "uploaded:${files!.join(',')}";
    }
  }
}

class _Ext extends FletExtension {
  final List<_PickerLike> created = [];
  @override
  FletService? createService(Control control) {
    if (control.type != "Probe" && control.type != "OtherProbe") return null;
    return (created..add(_PickerLike(control: control))).last;
  }
}

Map<String, dynamic> _snapshot({
  List<Map<String, dynamic>>? services,
  String uid = "registry",
}) =>
    {
      "_c": "Page",
      "_i": 1,
      "_services": {
        "_c": "ServiceRegistry",
        "_i": _registryId,
        "_internals": {"uid": uid},
        "_services": services ??
            [
              {"_c": "Probe", "_i": _pickerId}
            ],
      },
    };

void main() {
  late _FakeChannel channel;
  late _Ext ext;
  late FletBackend backend;
  late ServiceRegistry registry;

  void register({Map<String, dynamic>? snapshot}) => channel.receive(
      MessageAction.registerClient,
      {"session_id": "s", "page_patch": snapshot ?? _snapshot(), "error": ""});

  void invoke(String id, String name, {bool cancel = false}) =>
      channel.receive(MessageAction.invokeControlMethod, {
        "control_id": _pickerId,
        "call_id": id,
        "name": name,
        "args": <String, dynamic>{"cancel": cancel},
        "timeout": 2,
      });

  Map resp(String id) =>
      channel.invokeResponses.firstWhere((r) => r["call_id"] == id);

  setUp(() async {
    channel = _FakeChannel();
    ext = _Ext();
    backend = FletBackend(
        pageUri: Uri.parse("mock"),
        assetsDir: "",
        extensions: [ext],
        multiView: false,
        channelBuilder: channel.builder);
    await backend.connect();
    register();
    registry = ServiceRegistry(
        control: backend.page.child("_services")!,
        propertyName: "_services",
        backend: backend);
  });

  tearDown(() {
    registry.dispose();
    backend.dispose();
  });

  test('pick -> reconnect -> upload preserves selection and lifecycle',
      () async {
    invoke("p", "pick_files");
    await pumpEventQueue();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    expect(resp("p")["error"], isNull);

    register(); // reconnect
    invoke("u", "upload");
    await pumpEventQueue();
    expect(resp("u")["error"], isNull);
    expect(resp("u")["result"], "uploaded:sample.txt");
    expect(ext.created.length, 1, reason: "service reused, not recreated");
    expect(ext.created.single.inits, 1);
    expect(ext.created.single.disposals, 0);
    expect(
        identical(
            backend.controlsIndex.get(_pickerId), ext.created.single.control),
        isTrue);
  });

  test('reconnect while dialog open -> pick completes -> upload', () async {
    invoke("p", "pick_files");
    await pumpEventQueue();
    register(); // reconnect while dialog is open (the Android case)
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    expect(resp("p")["error"], isNull,
        reason: "in-flight pick must survive the rebind");
    expect(resp("p")["result"], ["sample.txt"]);

    invoke("u", "upload");
    await pumpEventQueue();
    expect(resp("u")["error"], isNull);
    expect(resp("u")["result"], "uploaded:sample.txt");
  });

  test('repeated reconnects keep routing', () async {
    for (var i = 0; i < 3; i++) {
      register();
    }
    invoke("p", "pick_files");
    await pumpEventQueue();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    invoke("u", "upload");
    await pumpEventQueue();
    expect(resp("u")["result"], "uploaded:sample.txt");
  });

  test('snapshot synchronizes properties omitted back to defaults', () {
    register(
        snapshot: _snapshot(services: [
      {
        "_c": "Probe",
        "_i": _pickerId,
        "on_result": true,
        "options": {"a": 1}
      }
    ]));
    final service = ext.created.single;
    final original = service.control;
    register();
    expect(identical(backend.controlsIndex.get(_pickerId), original), isTrue);
    expect(original.get("on_result"), isNull);
    expect(original.get("options"), isNull);
    expect(service.updates, greaterThan(0));
    expect(service.inits, 1);
    expect(service.disposals, 0);
  });

  test('reordering and adding services preserves existing bindings', () {
    final first = ext.created.single;
    register(
        snapshot: _snapshot(services: [
      {"_c": "Probe", "_i": 10},
      {"_c": "Probe", "_i": _pickerId}
    ]));
    final second = ext.created.last;
    register(
        snapshot: _snapshot(services: [
      {"_c": "Probe", "_i": _pickerId},
      {"_c": "Probe", "_i": 10}
    ]));
    expect(ext.created.length, 2);
    expect(
        identical(backend.controlsIndex.get(_pickerId), first.control), isTrue);
    expect(identical(backend.controlsIndex.get(10), second.control), isTrue);
    expect(first.inits, 1);
    expect(second.inits, 1);
    expect(first.disposals + second.disposals, 0);
    expect(registry.control.children("_services").map((c) => c.id),
        [_pickerId, 10]);
  });

  test('removed service is disposed once', () {
    final service = ext.created.single;
    register(snapshot: _snapshot(services: []));
    register(snapshot: _snapshot(services: []));
    expect(service.disposals, 1);
    expect(service.control.hasInvokeMethodListeners, isFalse);
  });

  test('omitted empty service list disposes previous services', () {
    final service = ext.created.single;
    final snapshot = _snapshot();
    (snapshot["_services"] as Map).remove("_services");
    register(snapshot: snapshot);
    expect(service.disposals, 1);
    expect(registry.control.children("_services"), isEmpty);
  });

  test('same id with a changed type deliberately replaces service', () {
    final old = ext.created.single;
    register(
        snapshot: _snapshot(services: [
      {"_c": "OtherProbe", "_i": _pickerId}
    ]));
    expect(ext.created.length, 2);
    expect(old.disposals, 1);
    expect(ext.created.last.control.type, "OtherProbe");
    expect(
        identical(
            backend.controlsIndex.get(_pickerId), ext.created.last.control),
        isTrue);
  });

  test('new registry uid does not reuse old service controls', () {
    final old = ext.created.single;
    final snapshot = _snapshot(uid: "new-registry");
    final incoming = snapshot["_services"] as Map;
    final internals = incoming.remove("_internals");
    incoming["_internals"] = internals;
    register(snapshot: snapshot);
    expect(ext.created.length, 2);
    expect(old.disposals, 1);
    expect(identical(old.control, ext.created.last.control), isFalse);
  });

  test('unchanged snapshots do not invoke service update', () {
    final service = ext.created.single;
    register();
    register();
    expect(service.updates, 0);
    expect(service.inits, 1);
    expect(service.disposals, 0);
  });

  test('nested map properties are synchronized as a snapshot', () {
    register(
        snapshot: _snapshot(services: [
      {
        "_c": "Probe",
        "_i": _pickerId,
        "options": {"keep": 1, "remove": 2}
      }
    ]));
    register(
        snapshot: _snapshot(services: [
      {
        "_c": "Probe",
        "_i": _pickerId,
        "options": {"keep": 3}
      }
    ]));
    expect(ext.created.single.control.get("options"), {"keep": 3});
  });

  test('cancelled pick survives reconnect and subsequent pick still works',
      () async {
    invoke("cancel", "pick_files", cancel: true);
    await pumpEventQueue();
    register();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    expect(resp("cancel")["error"], isNull);
    expect(resp("cancel")["result"], isEmpty);
    invoke("again", "pick_files");
    await pumpEventQueue();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    expect(resp("again")["result"], ["sample.txt"]);
  });

  test('cancelled selection before reconnect does not retain a stale result',
      () async {
    invoke("cancel", "pick_files", cancel: true);
    await pumpEventQueue();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    register();
    invoke("again", "pick_files");
    await pumpEventQueue();
    ext.created.single.dialog!.complete();
    await pumpEventQueue();
    expect(resp("cancel")["result"], isEmpty);
    expect(resp("again")["result"], ["sample.txt"]);
    expect(ext.created.single.inits, 1);
    expect(ext.created.single.disposals, 0);
  });

  test('registry uid change before service list also replaces bindings', () {
    final old = ext.created.single;
    register(snapshot: _snapshot(uid: "new-registry"));
    expect(old.disposals, 1);
    expect(ext.created.length, 2);
    expect(identical(old.control, ext.created.last.control), isFalse);
  });

  test('ordinary control lists keep their existing replacement semantics', () {
    backend.page.update({
      "controls": [
        {"_c": "Text", "_i": 20}
      ]
    });
    final original = backend.controlsIndex.get(20);
    backend.page.update({
      "controls": [
        {"_c": "Text", "_i": 20}
      ]
    });
    expect(identical(original, backend.controlsIndex.get(20)), isFalse);
  });

  test('ordinary property patches do not remove services', () {
    final service = ext.created.single;
    registry.control.update({"disabled": true}, shouldNotify: true);
    expect(registry.control.children("_services"), hasLength(1));
    expect(service.disposals, 0);
  });
}
