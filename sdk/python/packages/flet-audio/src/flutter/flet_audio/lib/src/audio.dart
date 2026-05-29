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

  @override
  void update() {
    debugPrint("Audio(${control.id}).update: ${control.properties}");

    final resolvedSrc = control.getSrc("src");
    if (resolvedSrc.error != null) {
      throw Exception("Audio src decode error: ${resolvedSrc.error}");
    }
    if (resolvedSrc.isEmpty) {
      throw Exception("Audio must have \"src\" specified.");
    }
    var autoplay = control.getBool("autoplay", false)!;
    var volume = control.getDouble("volume", 1.0)!;
    var balance = control.getDouble("balance", 0.0)!;
    var playbackRate = control.getDouble("playback_rate", 1)!;
    var releaseMode = parseReleaseMode(control.getString("release_mode"));

    () async {
      bool srcChanged = false;
      // URL or file
      if (resolvedSrc.uri != null && resolvedSrc.uri != _src) {
        _src = resolvedSrc.uri;
        _srcBytes = null;
        srcChanged = true;
        await _applySource();
      } else if (resolvedSrc.bytes != null &&
          (_srcBytes == null || !listEquals(_srcBytes, resolvedSrc.bytes))) {
        // bytes
        _srcBytes = resolvedSrc.bytes;
        _src = null;
        srcChanged = true;
        await _applySource();
      }

      if (srcChanged) {
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
      if (srcChanged && autoplay) {
        await player.resume();
      }
    }();
  }

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

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Audio.$name($args)");
    switch (name) {
      case "play":
        final position = parseDuration(args["position"]);
        if (player.state == PlayerState.completed) {
          // Playback finished. Under ReleaseMode.release the native source has
          // been freed, so re-prepare it before resuming: seeking/resuming a
          // freed source hangs forever (the player never emits onSeekComplete,
          // surfacing on the Python side as a 30s TimeoutException). See #6536.
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
    control.removeInvokeMethodListener(_invokeMethod);
    _onDurationChangedSubscription?.cancel();
    _onStateChangedSubscription?.cancel();
    _onPositionChangedSubscription?.cancel();
    _onSeekCompleteSubscription?.cancel();
    player.dispose();
    super.dispose();
  }
}
