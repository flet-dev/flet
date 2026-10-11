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
  double? _volume;
  double? _balance;
  double? _playbackRate;

  /// Incremented whenever the source is set, cleared or the service is
  /// disposed, so that an [update] that is still preparing an earlier source
  /// can tell that it was superseded.
  int _sourceVersion = 0;

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
  @override
  void update() {
    debugPrint("Audio(${control.id}).update: ${control.properties}");

    final resolvedSrc = control.get("src") != null
        ? control.getSrc("src")
        : const ResolvedAssetSource();
    if (resolvedSrc.error != null) {
      throw Exception("Audio src decode error: ${resolvedSrc.error}");
    }
    var autoplay = control.getBool("autoplay", false)!;
    var volume = control.getDouble("volume", 1.0)!;
    var balance = control.getDouble("balance", 0.0)!;
    var playbackRate = control.getDouble("playback_rate", 1)!;
    var releaseMode = parseReleaseMode(control.getString("release_mode"));

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
      if (srcChanged) {
        try {
          await _applySource();
        } catch (_) {
          if (sourceVersion != _sourceVersion) return;
          rethrow;
        }
        if (sourceVersion != _sourceVersion) return;
        control.triggerEvent("loaded");
      }

      // releaseMode
      if (releaseMode != null && releaseMode != _releaseMode) {
        _releaseMode = releaseMode;
        await player.setReleaseMode(releaseMode);
      }

      // volume
      if (volume != _volume && volume >= 0 && volume <= 1) {
        _volume = volume;
        await player.setVolume(volume);
      }

      // playbackRate
      if (playbackRate != _playbackRate) {
        _playbackRate = playbackRate;
        await player.setPlaybackRate(playbackRate);
      }

      // balance
      if (!kIsWeb && balance != _balance && balance >= -1 && balance <= 1) {
        _balance = balance;
        await player.setBalance(balance);
      }

      // autoplay
      if (srcChanged && autoplay && sourceVersion == _sourceVersion) {
        await player.resume();
      }
    }();
  }

  /// Whether a source is set, in [_src] or [_srcBytes].
  bool get _hasSource => _src != null || _srcBytes != null;

  /// Pushes the currently tracked source ([_src] or [_srcBytes]) to the native
  /// [player], preparing it for playback.
  ///
  /// Used both when the source changes (from [update]) and to re-prepare
  /// playback after the player has reached [PlayerState.completed] under
  /// [ReleaseMode.release], where the native source has already been freed.
  Future<void> _applySource() async {
    if (_src != null) {
      final assetSrc = control.backend.getAssetSource(_src!);
      if (assetSrc.isFile) {
        await player.setSourceDeviceFile(assetSrc.path);
      } else {
        await player.setSourceUrl(assetSrc.path);
      }
    } else if (_srcBytes != null) {
      await player.setSourceBytes(_srcBytes!);
    }
  }

  /// Handles a method call from Python.
  ///
  /// `play`, `resume` and `seek` throw while no source is set. The native
  /// players don't reject them: a seek never reports completion, so the call
  /// would only fail after timing out, and the web and Linux players remember
  /// a `resume` and start playing as soon as a source is set.
  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Audio.$name($args)");
    if (!_hasSource && const ["play", "resume", "seek"].contains(name)) {
      throw Exception("Audio must have \"src\" specified to $name.");
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
        await player.resume();
        break;
      case "resume":
        await player.resume();
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
    super.dispose();
  }
}
