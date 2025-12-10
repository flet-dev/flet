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

        var assetSrc = control.backend.getAssetSource(_src!);
        if (assetSrc.isFile) {
          await player.setSourceDeviceFile(assetSrc.path);
        } else {
          await player.setSourceUrl(assetSrc.path);
        }
      } else if (resolvedSrc.bytes != null &&
          (_srcBytes == null || !listEquals(_srcBytes, resolvedSrc.bytes))) {
        // bytes
        _srcBytes = resolvedSrc.bytes;
        _src = null;
        srcChanged = true;
        await player.setSourceBytes(resolvedSrc.bytes!);
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

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Audio.$name($args)");
    switch (name) {
      case "play":
        final position = parseDuration(args["position"]);
        if (position != null) {
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
