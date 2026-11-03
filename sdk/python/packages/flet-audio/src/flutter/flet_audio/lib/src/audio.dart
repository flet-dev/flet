import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';

import 'utils/audio.dart';

class AudioService extends FletService {
  AudioService({required super.control});

  AudioPlayer player = AudioPlayer();
  Duration? _duration;
  int _position = -1;
  StreamSubscription? _onDurationChangedSubscription;
  StreamSubscription? _onStateChangedSubscription;
  StreamSubscription? _onPositionChangedSubscription;
  StreamSubscription? _onSeekCompleteSubscription;

  String? _src;
  Uint8List? _srcBytes;
  ReleaseMode? _releaseMode;

  /// The context last applied to [player].
  ///
  /// On Android, it starts as the default that `Extension.ensureInitialized`
  /// gives every player. On iOS, it starts as `null`: a context applies to the
  /// whole app there, so any context that is set must be applied, even one equal
  /// to the default.
  AudioContext? _audioContext =
      isAndroidMobile() ? parseAudioContext(null) : null;

  double? _volume;
  double? _balance;
  double? _playbackRate;

  /// Incremented whenever the source is set, cleared or the service is
  /// disposed, so that an [update] that is still preparing an earlier source
  /// can tell that it was superseded.
  int _sourceVersion = 0;
  Future<void> _sourcePreparation = Future<void>.value();

  /// The error from preparing the latest source, if that failed.
  Object? _sourceError;

  @override
  void init() {
    super.init();
    debugPrint("Audio(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);

    _onDurationChangedSubscription =
        player.onDurationChanged.listen((duration) {
      control.triggerEvent("duration_change", {"duration": duration});
      _duration = duration;
    });

    _onStateChangedSubscription =
        player.onPlayerStateChanged.listen((PlayerState state) {
      control.triggerEvent("state_change", {"state": state.name});
      _trackIosDucking(state);
    });

    _onPositionChangedSubscription =
        player.onPositionChanged.listen((position) {
      int posMs = (position.inMilliseconds / 1000).round() * 1000;
      if (posMs != _position) {
        _position = posMs;
      } else if (position.inMilliseconds == _duration?.inMilliseconds) {
        _position = _duration!.inMilliseconds;
      } else {
        return;
      }
      control.triggerEvent("position_change", {"position": posMs});
    });

    _onSeekCompleteSubscription = player.onSeekComplete.listen((event) {
      control.triggerEvent("seek_complete");
    });

    update();
  }

  /// Applies the control's properties to [player].
  ///
  /// A missing or empty `src` means there is no source yet, e.g. until the
  /// user picks a file: the other properties are still applied, and playback
  /// of a source set earlier stops.
  ///
  /// The player is paused rather than released: the web player keeps the URL
  /// of a released source and skips loading it again, so setting the same
  /// `src` again would leave nothing to play.
  ///
  /// When `src` changes again while a source is still being prepared, the
  /// earlier preparation neither triggers `loaded` nor starts autoplay.
  ///
  /// Volume, balance and playback rate are applied again after a new source
  /// is loaded, and before `loaded` is triggered, since loading can reset
  /// them: a web media element resets its playback rate when it loads.
  ///
  /// Settings, `autoplay` included, are read from the control when they are
  /// applied, not when [update] is called, so an update that finishes loading
  /// a source after a later update never applies outdated values.
  ///
  /// The audio context is applied before the source, because changing it later
  /// makes the Android player prepare its source again.
  @override
  void update() {
    debugPrint("Audio(${control.id}).update: ${control.properties}");

    final resolvedSrc = control.get("src") != null
        ? control.getSrc("src")
        : const ResolvedAssetSource();
    if (resolvedSrc.error != null) {
      throw Exception("Audio src decode error: ${resolvedSrc.error}");
    }
    () async {
      bool srcChanged = false;
      if (resolvedSrc.isEmpty) {
        // no source
        if (_hasSource) {
          _src = null;
          _srcBytes = null;
          _sourceVersion++;
          await player.pause();
        }
      } else if (resolvedSrc.uri != null && resolvedSrc.uri != _src) {
        // URL or file
        _src = resolvedSrc.uri;
        _srcBytes = null;
        srcChanged = true;
      } else if (resolvedSrc.bytes != null &&
          (_srcBytes == null || !listEquals(_srcBytes, resolvedSrc.bytes))) {
        // bytes
        _srcBytes = resolvedSrc.bytes;
        _src = null;
        srcChanged = true;
      }

      final sourceVersion = srcChanged ? ++_sourceVersion : _sourceVersion;
      final contextApplied = _applyAudioContext();
      if (!srcChanged) {
        await contextApplied;
        if (sourceVersion != _sourceVersion) return;
      } else {
        try {
          await _applySource(after: contextApplied);
        } catch (_) {
          if (sourceVersion != _sourceVersion) return;
          rethrow;
        }
        if (sourceVersion != _sourceVersion) return;
        _volume = null;
        _balance = null;
        _playbackRate = null;
      }

      await _applySettings();

      if (srcChanged && sourceVersion == _sourceVersion) {
        control.triggerEvent("loaded");
        if (control.getBool("autoplay", false)!) {
          await _resume();
        }
      }
    }();
  }

  /// Applies the control's release mode, volume, playback rate and balance to
  /// [player], when they changed.
  Future<void> _applySettings() async {
    // releaseMode
    final releaseMode = parseReleaseMode(control.getString("release_mode"));
    if (releaseMode != null && releaseMode != _releaseMode) {
      _releaseMode = releaseMode;
      await player.setReleaseMode(releaseMode);
    }

    // volume
    final volume = control.getDouble("volume", 1.0)!;
    if (volume != _volume && volume >= 0 && volume <= 1) {
      _volume = volume;
      await player.setVolume(volume);
    }

    // playbackRate
    final playbackRate = control.getDouble("playback_rate", 1)!;
    if (playbackRate != _playbackRate) {
      _playbackRate = playbackRate;
      await player.setPlaybackRate(playbackRate);
    }

    // balance
    final balance = control.getDouble("balance", 0.0)!;
    if (!kIsWeb && balance != _balance && balance >= -1 && balance <= 1) {
      _balance = balance;
      await player.setBalance(balance);
    }
  }

  /// Loads a source that failed to load again, then does what [update] couldn't
  /// do after the failure.
  Future<void> _reloadSource() async {
    await _applySource();
    _volume = null;
    _balance = null;
    _playbackRate = null;
    await _applySettings();
    control.triggerEvent("loaded");
  }

  /// Applies the control's `context` to [player] on the platforms that
  /// support audio contexts.
  Future<void> _applyAudioContext() async {
    if (!isMobilePlatform()) return;
    final value = control.get("context");
    if (value == null && _audioContext == null) return;
    final audioContext = parseAudioContext(value);
    if (audioContext == _audioContext) return;
    _audioContext = audioContext;
    await player.setAudioContext(audioContext);
    if (isIOSMobile()) await IosDucking.contextApplied(audioContext);
  }

  /// Starts [player], after restoring any context [IosDucking] released.
  Future<void> _resume() async {
    if (!isIOSMobile()) return player.resume();
    try {
      await IosDucking.startPlaying(this);
      await player.resume();
    } catch (_) {
      await IosDucking.stopPlaying(this);
      rethrow;
    }
  }

  /// Tells [IosDucking] when [player] stops playing.
  ///
  /// iOS reports [PlayerState.completed] each time audio under
  /// [ReleaseMode.loop] restarts, while it keeps playing.
  void _trackIosDucking(PlayerState state) {
    if (!isIOSMobile() ||
        state == PlayerState.playing ||
        (state == PlayerState.completed && _releaseMode == ReleaseMode.loop)) {
      return;
    }
    IosDucking.stopPlaying(this);
  }

  /// Whether a source is set, in [_src] or [_srcBytes].
  bool get _hasSource => _src != null || _srcBytes != null;

  /// Pushes the currently tracked source ([_src] or [_srcBytes]) to the native
  /// [player], preparing it for playback.
  ///
  /// Used both when the source changes (from [update]) and to re-prepare
  /// playback after the player has reached [PlayerState.completed] under
  /// [ReleaseMode.release], where the native source has already been freed.
  /// Preparations run in order because setting a byte source may first write
  /// a temporary file. A superseded preparation must finish before the latest
  /// source is installed, otherwise its delayed write could replace that source.
  ///
  /// The source is set once [after] completes, while the preparation is queued
  /// right away, so that a method call received in the meantime waits for it.
  Future<void> _applySource({Future<void>? after}) {
    final src = _src;
    final srcBytes = _srcBytes;
    final sourceVersion = _sourceVersion;
    final preparation = _sourcePreparation.then((_) async {
      await after;
      if (sourceVersion != _sourceVersion) return;
      if (src != null) {
        final assetSrc = control.backend.getAssetSource(src);
        if (assetSrc.isFile) {
          await player.setSourceDeviceFile(assetSrc.path);
        } else {
          await player.setSourceUrl(assetSrc.path);
        }
      } else if (srcBytes != null) {
        await player.setSourceBytes(srcBytes);
      }
    });
    // Keep the queue usable after a failed load. The caller still receives the
    // original error and decides whether this preparation was superseded.
    _sourcePreparation = preparation.then<void>((_) {
      _sourceError = null;
    }, onError: (Object error, StackTrace stackTrace) {
      _sourceError = error;
    });
    return preparation;
  }

  /// Handles a method call from Python.
  ///
  /// `play`, `resume` and `seek` throw while no source is set. The native
  /// players don't reject them: a seek never reports completion, so the call
  /// would only fail after timing out, and the web and Linux players remember
  /// a `resume` and start playing as soon as a source is set.
  ///
  /// They also wait for a source that is still being prepared, because a seek
  /// before that never completes on iOS. A source that failed to load is loaded
  /// again, so they either report its error at once or work once it is available.
  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Audio.$name($args)");
    if (const ["play", "resume", "seek"].contains(name)) {
      if (!_hasSource) {
        throw Exception("Audio must have \"src\" specified to $name.");
      }
      await _sourcePreparation;
      if (_sourceError != null) await _reloadSource();
    }
    switch (name) {
      case "play":
        final position = parseDuration(args["position"]);
        if (player.state == PlayerState.completed) {
          // Playback finished. Under ReleaseMode.release the native source has
          // been freed, so re-prepare it before resuming.
          if ((_releaseMode ?? ReleaseMode.release) == ReleaseMode.release) {
            await _applySource();
          }
          // Position is already reset to the start after completion, so only
          // seek when a specific non-zero position was requested.
          if (position != null && position > Duration.zero) {
            await player.seek(position);
          }
        } else if (position != null) {
          await player.seek(position);
        }
        await _resume();
        break;
      case "resume":
        await _resume();
        break;
      case "pause":
        await player.pause();
        break;
      case "release":
        await player.release();
        break;
      case "seek":
        final position = parseDuration(args["position"]);
        if (position != null) {
          if (player.state == PlayerState.completed &&
              (_releaseMode ?? ReleaseMode.release) == ReleaseMode.release) {
            // Source was freed on completion (see "play"); re-prepare it,
            // otherwise the seek would hang waiting for onSeekComplete.
            await _applySource();
          }
          await player.seek(position);
        }
        break;
      case "get_duration":
        return await player.getDuration();
      case "get_current_position":
        return await player.getCurrentPosition();
      default:
        throw Exception("Unknown Audio method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("Audio(${control.id}).dispose()");
    _sourceVersion++;
    control.removeInvokeMethodListener(_invokeMethod);
    _onDurationChangedSubscription?.cancel();
    _onStateChangedSubscription?.cancel();
    _onPositionChangedSubscription?.cancel();
    _onSeekCompleteSubscription?.cancel();
    player.dispose();
    if (isIOSMobile()) IosDucking.stopPlaying(this);
    super.dispose();
  }
}
