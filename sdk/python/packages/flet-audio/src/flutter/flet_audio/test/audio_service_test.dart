import 'dart:async';
import 'package:audioplayers_platform_interface/audioplayers_platform_interface.dart';
import 'package:flet/flet.dart';
import 'package:flet_audio/src/audio.dart';
import 'package:flet_audio/src/extension.dart';
import 'package:flet_audio/src/utils/audio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:path_provider_platform_interface/path_provider_platform_interface.dart';

class _AudioPlatform extends AudioplayersPlatformInterface {
  final events = <String, StreamController<AudioEvent>>{};
  final sources = <String>[];
  int sourcesWhenFocusApplied = -1;
  int resumes = 0;
  double rate = 1;
  Completer<void>? volumeGate;
  Completer<void>? sourceGate;
  Completer<void>? contextGate;
  bool failNextSource = false;
  bool failSources = false;
  ReleaseMode? releaseMode;
  bool prepared = false;
  final contexts = <AudioContext>[];
  int contextRepreparations = 0;

  List<AndroidAudioFocus> get audioFocuses =>
      contexts.map((context) => context.android.audioFocus).toList();

  @override
  Future<void> setAudioContext(String id, AudioContext context) async {
    contexts.add(context);
    sourcesWhenFocusApplied = sources.length;
    if (sources.isNotEmpty) {
      // Android stops and asynchronously re-prepares an existing source when
      // its context changes. The method returns before it is prepared again.
      prepared = false;
      contextRepreparations++;
    }
    final gate = contextGate;
    contextGate = null;
    if (gate != null) await gate.future;
  }

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
    if (failNextSource || failSources) {
      failNextSource = false;
      events[id]!.addError(StateError('superseded load failed'));
      return;
    }
    sources.add(url);
    prepared = true;
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
  Future<void> setReleaseMode(String id, ReleaseMode mode) async {
    releaseMode = mode;
  }

  @override
  Future<void> setBalance(String id, double balance) async {}
  @override
  Future<int?> getCurrentPosition(String id) async => 0;
  @override
  Future<int?> getDuration(String id) async => prepared ? 1000 : null;
  @override
  Future<void> resume(String id) async {
    resumes++;
  }

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
  final audioFocuses = <AndroidAudioFocus>[];
  final iosOptions = <Set<AVAudioSessionOptions>>[];
  @override
  Future<void> setGlobalAudioContext(AudioContext context) async {
    audioFocuses.add(context.android.audioFocus);
    iosOptions.add(context.iOS.options);
  }

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
  late _GlobalPlatform globalPlatform;
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
    globalPlatform = _GlobalPlatform();
    GlobalAudioplayersPlatformInterface.instance = globalPlatform;
    directory = await Directory.systemTemp.createTemp('flet-audio-test-');
    paths = _PathProvider(directory);
    PathProviderPlatform.instance = paths;
    debugDefaultTargetPlatformOverride = TargetPlatform.macOS;
    IosDucking.reset();
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
  test('applies audio context before preparing the initial source', () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.android;
    control.properties['src'] = 'https://example.com/effect.wav';
    control.properties['context'] = {'focus': 'mixWithOthers'};

    service.update();
    await _settle();

    expect(platform.contexts.single.android.audioFocus, AndroidAudioFocus.none);
    expect(control.events.where((e) => e == 'loaded'), hasLength(1));
    expect(await service.player.getDuration(), const Duration(seconds: 1));
    expect(platform.contextRepreparations, 0);
  });

  test('applies audio context without a source', () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.android;
    control.properties['context'] = {'focus': 'mixWithOthers'};

    service.update();
    await _settle();

    expect(platform.contexts.single.android.audioFocus, AndroidAudioFocus.none);
    expect(platform.sources, isEmpty);
    expect(control.events, isNot(contains('loaded')));
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
  test('play waits for a source that is still being prepared', () async {
    final gate = Completer<void>();
    platform.sourceGate = gate;
    control.properties['src'] = 'https://example.com/a.wav';
    service.init();
    await _settle();
    final play = control.invokeMethod(
        'play', {'position': null}, const Duration(seconds: 5));
    await _settle();
    expect(platform.resumes, 0);
    gate.complete();
    await play;
    expect(platform.sources, hasLength(1));
    expect(platform.resumes, 1);
  });
  test('play reports a source that fails to load', () async {
    platform.failSources = true;
    runZonedGuarded(() {
      control.properties['src'] = 'https://example.com/missing.wav';
      service.init();
    }, (_, __) {});
    await _settle();
    await expectLater(
        control.invokeMethod(
            'play', {'position': null}, const Duration(seconds: 5)),
        throwsA(anything));
    expect(platform.resumes, 0);
  });
  test('play loads a source again after it failed to load', () async {
    platform.failNextSource = true;
    runZonedGuarded(() {
      control.properties['src'] = 'https://example.com/a.wav';
      control.properties['release_mode'] = 'loop';
      service.init();
    }, (_, __) {});
    await _settle();
    await control.invokeMethod(
        'play', {'position': null}, const Duration(seconds: 5));
    expect(platform.sources, hasLength(1));
    expect(platform.resumes, 1);
    expect(platform.releaseMode, ReleaseMode.loop);
    expect(control.events.where((e) => e == 'loaded'), hasLength(1));
  });
  group('context', () {
    Future<void> createService(TargetPlatform targetPlatform) async {
      debugDefaultTargetPlatformOverride = targetPlatform;
      await service.player.dispose();
      service = AudioService(control: control);
      await service.player.creatingCompleter.future;
    }

    setUp(() => createService(TargetPlatform.android));

    test('leaves the default context to the extension', () async {
      control.properties['src'] = 'https://example.com/a.wav';
      service.update();
      await _settle();
      expect(platform.audioFocuses, isEmpty);
    });

    test('is applied once and before the source', () async {
      control.properties['src'] = 'https://example.com/a.wav';
      control.properties['context'] = {'focus': 'mixWithOthers'};
      service.update();
      await _settle();
      service.update();
      await _settle();
      expect(platform.audioFocuses, [AndroidAudioFocus.none]);
      expect(platform.sourcesWhenFocusApplied, 0);
      expect(platform.sources, hasLength(1));
    });

    test('a source set while the focus is applied replaces the earlier one',
        () async {
      final gate = Completer<void>();
      platform.contextGate = gate;
      control.properties['src'] = 'https://example.com/first.wav';
      control.properties['context'] = {'focus': 'mixWithOthers'};
      service.update();
      await _settle();
      control.properties['src'] = 'https://example.com/latest.wav';
      service.update();
      await _settle();
      gate.complete();
      await _settle();
      expect(platform.sources, ['https://example.com/latest.wav']);
      expect(control.events.where((e) => e == 'loaded'), hasLength(1));
    });

    test('maps every value and returns to the default when cleared', () async {
      for (final value in ['gain', 'mixWithOthers', null]) {
        control.properties['context'] = value == null ? null : {'focus': value};
        service.update();
        await _settle();
      }
      expect(platform.audioFocuses, [
        AndroidAudioFocus.gain,
        AndroidAudioFocus.none,
        AndroidAudioFocus.gainTransientMayDuck,
      ]);
    });

    test('applies only a set context on iOS', () async {
      await createService(TargetPlatform.iOS);
      service.update();
      await _settle();
      expect(platform.audioFocuses, isEmpty);
      control.properties['context'] = {'focus': 'mixWithOthers'};
      service.update();
      await _settle();
      expect(platform.audioFocuses, hasLength(1));
    });

    test('applies a context equal to the default on iOS', () async {
      await createService(TargetPlatform.iOS);
      control.properties['context'] = {'focus': 'gain'};
      service.update();
      await _settle();
      expect(platform.contexts.single.iOS.options, isEmpty);
    });

    group('ducking on iOS', () {
      const duck = {AVAudioSessionOptions.duckOthers};
      const mix = {AVAudioSessionOptions.mixWithOthers};

      Future<dynamic> call(_Control target, String method) => target
          .invokeMethod(method, {'position': null}, const Duration(seconds: 5));

      setUp(() async {
        await createService(TargetPlatform.iOS);
        control.properties['src'] = 'https://example.com/a.wav';
        control.properties['context'] = {'focus': 'duckOthers'};
        service.init();
        await _settle();
      });

      test('is released until the audio plays', () async {
        expect(globalPlatform.iosOptions, [mix]);
        await call(control, 'play');
        expect(globalPlatform.iosOptions, [mix, duck]);
      });

      test('is released and restored when pausing and resuming', () async {
        await call(control, 'play');
        await call(control, 'pause');
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck, mix]);
        await call(control, 'resume');
        expect(globalPlatform.iosOptions, [mix, duck, mix, duck]);
      });

      test('is released when the audio is released', () async {
        await call(control, 'play');
        await call(control, 'release');
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck, mix]);
      });

      test('is released when the audio completes', () async {
        await call(control, 'play');
        platform.events.values.single
            .add(const AudioEvent(eventType: AudioEventType.complete));
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck, mix]);
      });

      test('stays while looping audio restarts', () async {
        control.properties['release_mode'] = 'loop';
        service.update();
        await _settle();
        await call(control, 'play');
        platform.events.values.single
            .add(const AudioEvent(eventType: AudioEventType.complete));
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck]);
      });

      test('stays until the last playing audio stops', () async {
        final other = _Control(backend, {'src': 'https://example.com/b.wav'});
        final otherService = AudioService(control: other);
        await otherService.player.creatingCompleter.future;
        otherService.init();
        await _settle();
        await call(control, 'play');
        await call(other, 'play');
        await call(control, 'pause');
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck]);
        await call(other, 'pause');
        await _settle();
        expect(globalPlatform.iosOptions, [mix, duck, mix]);
        otherService.dispose();
      });

      test('never changes a context without ducking', () async {
        IosDucking.reset();
        globalPlatform.iosOptions.clear();
        control.properties['context'] = {'focus': 'mixWithOthers'};
        service.update();
        await _settle();
        await call(control, 'play');
        await call(control, 'pause');
        await _settle();
        expect(globalPlatform.iosOptions, isEmpty);
      });
    });

    test('is ignored on other platforms', () async {
      await createService(TargetPlatform.macOS);
      control.properties['context'] = {'focus': 'mixWithOthers'};
      service.update();
      await _settle();
      expect(platform.audioFocuses, isEmpty);
    });

    test('the extension sets the default for every player on Android',
        () async {
      Extension().ensureInitialized();
      await _settle();
      expect(globalPlatform.audioFocuses,
          [AndroidAudioFocus.gainTransientMayDuck]);
    });

    test('the extension sets no default on other platforms', () async {
      for (final other in [TargetPlatform.iOS, TargetPlatform.macOS]) {
        debugDefaultTargetPlatformOverride = other;
        Extension().ensureInitialized();
        await _settle();
      }
      expect(globalPlatform.audioFocuses, isEmpty);
    });
  });
}
