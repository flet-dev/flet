import 'dart:async';
import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flet/flet.dart';
import 'package:flet_audio/src/audio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:path_provider_platform_interface/path_provider_platform_interface.dart';

class _AudioPlatform extends AudioplayersPlatformInterface {
  final events = <String, StreamController<AudioEvent>>{};
  final sources = <String>[];
  double rate = 1;
  Completer<void>? volumeGate;
  Completer<void>? sourceGate;
  bool failNextSource = false;
  @override
  Future<void> create(String id) async {}
  @override
  Stream<AudioEvent> getEventStream(String id) => events
      .putIfAbsent(id, () => StreamController<AudioEvent>.broadcast())
      .stream;
  @override
  Future<void> setSourceUrl(String id, String url,
      {bool? isLocal, String? mimeType}) async {
    final gate = sourceGate;
    sourceGate = null;
    if (gate != null) await gate.future;
    if (failNextSource) {
      failNextSource = false;
      events[id]!.addError(StateError('superseded load failed'));
      return;
    }
    sources.add(url);
    events[id]!.add(
        const AudioEvent(eventType: AudioEventType.prepared, isPrepared: true));
  }

  @override
  Future<void> setVolume(String id, double volume) async {
    final gate = volumeGate;
    volumeGate = null;
    if (gate != null) await gate.future;
  }

  @override
  Future<void> setPlaybackRate(String id, double r) async {
    rate = r;
  }

  @override
  Future<void> setReleaseMode(String id, ReleaseMode mode) async {}
  @override
  Future<void> setBalance(String id, double balance) async {}
  @override
  Future<int?> getCurrentPosition(String id) async => 0;
  @override
  Future<void> pause(String id) async {}
  @override
  Future<void> stop(String id) async {}
  @override
  Future<void> release(String id) async {}
  @override
  Future<void> dispose(String id) async {
    await events.remove(id)?.close();
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _GlobalPlatform extends GlobalAudioplayersPlatformInterface {
  @override
  Future<void> init() async {}
  @override
  Stream<GlobalAudioEvent> getGlobalEventStream() => const Stream.empty();
  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _PathProvider extends PathProviderPlatform {
  _PathProvider(this.directory);
  final Directory directory;
  Completer<void>? gate;
  @override
  Future<String?> getTemporaryPath() async {
    if (gate != null) await gate!.future;
    return directory.path;
  }
}

class _Control extends Control {
  _Control(FletBackend backend, Map<String, dynamic> properties)
      : super(id: 1, type: 'Audio', properties: properties, backend: backend);
  final events = <String>[];
  @override
  void triggerEvent(String name, [dynamic data]) => events.add(name);
}

Future<void> _settle() async {
  for (var i = 0; i < 20; i++) {
    await Future<void>.delayed(Duration.zero);
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late _AudioPlatform platform;
  late _PathProvider paths;
  late Directory directory;
  late FletBackend backend;
  late _Control control;
  late AudioService service;
  late AudioplayersPlatformInterface originalPlatform;
  late GlobalAudioplayersPlatformInterface originalGlobal;
  late PathProviderPlatform originalPaths;
  setUp(() async {
    originalPlatform = AudioplayersPlatformInterface.instance;
    originalGlobal = GlobalAudioplayersPlatformInterface.instance;
    originalPaths = PathProviderPlatform.instance;
    platform = _AudioPlatform();
    AudioplayersPlatformInterface.instance = platform;
    GlobalAudioplayersPlatformInterface.instance = _GlobalPlatform();
    directory = await Directory.systemTemp.createTemp('flet-audio-test-');
    paths = _PathProvider(directory);
    PathProviderPlatform.instance = paths;
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    backend = FletBackend(
        pageUri: Uri.parse('http://localhost'),
        assetsDir: '',
        multiView: false,
        extensions: []);
    control = _Control(backend, {'src': null, 'playback_rate': 1.0});
    service = AudioService(control: control);
    await service.player.creatingCompleter.future;
  });
  tearDown(() async {
    await service.player.dispose();
    backend.dispose();
    await directory.delete(recursive: true);
    debugDefaultTargetPlatformOverride = null;
    AudioplayersPlatformInterface.instance = originalPlatform;
    GlobalAudioplayersPlatformInterface.instance = originalGlobal;
    PathProviderPlatform.instance = originalPaths;
  });
  test('reads the latest rate after awaiting post-load volume', () async {
    control.properties['src'] = 'https://example.com/first.wav';
    service.update();
    await _settle();
    final gate = Completer<void>();
    platform.volumeGate = gate;
    control.properties['src'] = 'https://example.com/second.wav';
    service.update();
    await _settle();
    control.properties['playback_rate'] = 2.0;
    service.update();
    await _settle();
    expect(platform.rate, 2.0);
    gate.complete();
    await _settle();
    expect(platform.rate, 2.0);
    expect(control.events.where((e) => e == 'loaded'), hasLength(2));
  });
  test('installs the latest URL after a superseded byte file write', () async {
    final gate = Completer<void>();
    paths.gate = gate;
    control.properties['src'] = Uint8List.fromList([1, 2, 3]);
    service.update();
    await _settle();
    control.properties['src'] = '';
    service.update();
    await _settle();
    control.properties['src'] = 'https://example.com/latest.wav';
    service.update();
    await _settle();
    gate.complete();
    // Exercise audioplayers' real temporary-file write before preparation.
    for (var i = 0; i < 100 && platform.sources.length < 2; i++) {
      await Future<void>.delayed(const Duration(milliseconds: 5));
    }
    await _settle();
    expect(platform.sources, hasLength(2));
    expect(platform.sources.last, 'https://example.com/latest.wav');
    expect(control.events.where((e) => e == 'loaded'), hasLength(1));
  });
  test('a failed superseded preparation does not poison the queue', () async {
    final gate = Completer<void>();
    platform.sourceGate = gate;
    platform.failNextSource = true;
    control.properties['src'] = 'https://example.com/failing.wav';
    service.update();
    await _settle();
    control.properties['src'] = 'https://example.com/latest.wav';
    service.update();
    gate.complete();
    await _settle();
    expect(platform.sources, ['https://example.com/latest.wav']);
    expect(control.events.where((e) => e == 'loaded'), hasLength(1));
  });
}
