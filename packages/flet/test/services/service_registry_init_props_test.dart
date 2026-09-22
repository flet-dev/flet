/// Pins down how the client builds a service that Python registers.
///
/// The client creates a service's [FletService] and calls its `init()` as soon
/// as the patch that adds the service to the page's `ServiceRegistry` arrives,
/// using only the properties in that patch. [Control.triggerEvent] sends an
/// event only when the control's `on_<event>` property is `true`, and a later
/// property patch only calls [FletService.update] - `init()` never runs again.
///
/// So an event a service raises from `init()` (for example, announcing a
/// `DataChannel` with `data_channel_open`) reaches Python only if its handler
/// flag was already part of the registration patch. That is why Python
/// registers a service only after its `init()` has returned: everything set
/// there must be in that first message
/// ([#6736](https://github.com/flet-dev/flet/discussions/6736)).
library;

import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flet/src/services/service_registry.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:msgpack_dart/msgpack_dart.dart' as msgpack;

const _registryId = 7;

/// An in-memory transport that plays the Python side of the protocol.
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

  /// Delivers a protocol message framed the way Python sends it.
  void receive(MessageAction action, Map<String, dynamic> payload) {
    final body = msgpack.serialize([action.value, payload]);
    _onPacket(Uint8List.fromList([0x00, ...body]));
  }

  /// Delivers a `PATCH_CONTROL` message for the control with [id].
  void receivePatch(int id, List<dynamic> patch) =>
      receive(MessageAction.patchControl, {"id": id, "patch": patch});

  /// The control events the client has sent to Python so far.
  List<Map> get controlEvents => sent
      .where((packet) => packet.isNotEmpty && packet[0] == 0x00)
      .map((packet) =>
          msgpack.deserialize(Uint8List.sublistView(packet, 1)) as List)
      .where((message) => message[0] == MessageAction.controlEvent.value)
      .map((message) => message[1] as Map)
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

/// A service that raises its `probe` event from `init()`, the way a user
/// service announces its `DataChannel`.
class _ProbeService extends FletService {
  _ProbeService({required super.control});

  int initCalls = 0;
  int updateCalls = 0;

  /// Whether `init()` saw a `probe` handler on the control.
  bool? hadHandlerInInit;

  @override
  void init() {
    super.init();
    initCalls++;
    hadHandlerInInit = control.hasEventHandler("probe");
    control.triggerEvent("probe", {"from": "init"});
  }

  @override
  void update() {
    updateCalls++;
  }
}

class _ProbeExtension extends FletExtension {
  /// Every probe service this extension created, by control id.
  final Map<int, _ProbeService> services = {};

  @override
  FletService? createService(Control control) {
    if (control.type != "Probe") {
      return null;
    }
    return services[control.id] = _ProbeService(control: control);
  }
}

/// The patch Python sends to the registry for the first service on a page.
///
/// An empty `_services` list is never sent with the page, so the whole list is
/// replaced.
List<dynamic> _firstServicePatch(Map<String, dynamic> service) => [
      [0],
      [
        OperationType.replace.value,
        0,
        "_services",
        [service]
      ],
    ];

/// The patch Python sends to the registry for each later service: an add
/// operation into `_services` at [index].
List<dynamic> _addServicePatch(int index, Map<String, dynamic> service) => [
      [
        0,
        {
          "_services": [1]
        }
      ],
      [OperationType.add.value, 1, index, service],
    ];

/// The patch Python sends to a service itself when `update()` changes [name].
List<dynamic> _propertyPatch(String name, dynamic value) => [
      [0],
      [OperationType.replace.value, 0, name, value],
    ];

void main() {
  group('a service added through the ServiceRegistry', () {
    late _FakeChannel channel;
    late _ProbeExtension extension;
    late FletBackend backend;
    late ServiceRegistry registry;

    setUp(() async {
      channel = _FakeChannel();
      extension = _ProbeExtension();
      backend = FletBackend(
        pageUri: Uri.parse("mock"),
        assetsDir: "",
        extensions: [extension],
        multiView: false,
        channelBuilder: channel.builder,
      );
      await backend.connect();
      channel.receive(MessageAction.registerClient, {
        "session_id": "session",
        "page_patch": {
          "_c": "Page",
          "_i": 1,
          "_services": {
            "_c": "ServiceRegistry",
            "_i": _registryId,
            "_internals": {"uid": "registry"},
          },
        },
        "error": "",
      });
      // Built the way `PageControl` builds it for the page's `_services`.
      registry = ServiceRegistry(
          control: backend.page.child("_services")!,
          propertyName: "_services",
          backend: backend);
    });

    tearDown(() {
      registry.dispose();
      backend.dispose();
    });

    test('sends an event raised in init() when its handler flag is included',
        () {
      channel.receivePatch(_registryId,
          _firstServicePatch({"_c": "Probe", "_i": 9, "on_probe": true}));
      channel.receivePatch(_registryId,
          _addServicePatch(1, {"_c": "Probe", "_i": 10, "on_probe": true}));

      expect(extension.services.keys, [9, 10]);
      for (final service in extension.services.values) {
        expect(service.initCalls, 1);
        expect(service.hadHandlerInInit, isTrue);
      }
      expect(channel.controlEvents, [
        {
          "target": 9,
          "name": "probe",
          "data": {"from": "init"}
        },
        {
          "target": 10,
          "name": "probe",
          "data": {"from": "init"}
        },
      ]);
    });

    test('drops an event raised in init() when its handler flag comes later',
        () {
      channel.receivePatch(_registryId,
          _firstServicePatch({"_c": "Probe", "_i": 9, "on_probe": true}));
      channel.receivePatch(
          _registryId, _addServicePatch(1, {"_c": "Probe", "_i": 10}));

      final lateService = extension.services[10]!;
      expect(lateService.hadHandlerInInit, isFalse);
      expect(channel.controlEvents.map((event) => event["target"]), [9]);

      // What an `update()` in Python sends once the handler is assigned.
      channel.receivePatch(10, _propertyPatch("on_probe", true));

      // The flag arrives, but only `update()` is called: `init()`, and the
      // event it raises, is not run again.
      expect(lateService.control.hasEventHandler("probe"), isTrue);
      expect(lateService.updateCalls, 1);
      expect(lateService.initCalls, 1);
      expect(channel.controlEvents.map((event) => event["target"]), [9]);
    });
  });
}
