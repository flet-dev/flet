import 'dart:convert';

import 'package:audioplayers/audioplayers.dart';
import 'package:collection/collection.dart';
import 'package:flet/src/flet_app_services.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'error.dart';

class AudioControl extends StatefulWidget {
  final Control? parent;
  final Control control;

  const AudioControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  State<AudioControl> createState() => _AudioControlState();
}

class _AudioControlState extends State<AudioControl> {
  String _src = "";
  String _srcBase64 = "";
  ReleaseMode? _releaseMode;
  double? _volume;
  double? _balance;
  String? _method;
  void Function(Duration)? _onDurationChanged;
  void Function(PlayerState)? _onStateChanged;
  void Function(int)? _onPositionChanged;
  Duration? _duration;
  int _position = -1;
  void Function()? _onSeekComplete;
  late final AudioPlayer player;

  @override
  void initState() {
    super.initState();
    player = AudioPlayer();
    player.onDurationChanged.listen((duration) {
      _onDurationChanged?.call(duration);
      _duration = duration;
    });
    player.onPlayerStateChanged.listen((state) {
      _onStateChanged?.call(state);
    });
    player.onPositionChanged.listen((position) {
      int posMs = (position.inMilliseconds / 1000).round() * 1000;
      if (posMs != _position) {
        _position = posMs;
      } else if (position.inMilliseconds == _duration?.inMilliseconds) {
        _position = _duration!.inMilliseconds;
      } else {
        return;
      }
      _onPositionChanged?.call(_position);
    });
    player.onSeekComplete.listen((event) {
      _onSeekComplete?.call();
    });
  }

  @override
  void dispose() {
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Audio build: ${widget.control.id}");

    var src = widget.control.attrString("src", "")!;
    var srcBase64 = widget.control.attrString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Audio must have either \"src\" or \"src_base64\" specified.");
    }
    bool autoplay = widget.control.attrBool("autoplay", false)!;
    double? volume = widget.control.attrDouble("volume", null);
    double? balance = widget.control.attrDouble("balance", null);
    var releaseMode = ReleaseMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("releaseMode", "")!.toLowerCase());
    bool onPositionChanged =
        widget.control.attrBool("onPositionChanged", false)!;

    var ws = FletAppServices.of(context).ws;

    _onDurationChanged = (duration) {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: "duration_changed",
          eventData: duration.inMilliseconds.toString());
    };

    _onStateChanged = (state) {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: "state_changed",
          eventData: state.name.toString());
    };

    if (onPositionChanged) {
      _onPositionChanged = (duration) {
        ws.pageEventFromWeb(
            eventTarget: widget.control.id,
            eventName: "position_changed",
            eventData: duration.toString());
      };
    }

    _onSeekComplete = () {
      ws.pageEventFromWeb(
          eventTarget: widget.control.id,
          eventName: "seek_complete",
          eventData: "");
    };

    () async {
      bool srcChanged = false;
      if (src != "" && src != _src) {
        _src = src;
        srcChanged = true;
        await player.setSourceUrl(src);
      } else if (srcBase64 != "" && srcBase64 != _srcBase64) {
        _srcBase64 = srcBase64;
        srcChanged = true;
        await player.setSourceBytes(base64Decode(srcBase64));
      }

      if (srcChanged) {
        ws.pageEventFromWeb(
            eventTarget: widget.control.id, eventName: "loaded", eventData: "");
      }

      if (releaseMode != null && releaseMode != _releaseMode) {
        _releaseMode = releaseMode;
        await player.setReleaseMode(releaseMode);
      }

      if (volume != null && volume != _volume && volume >= 0 && volume <= 1) {
        _volume = volume;
        await player.setVolume(volume);
      }

      if (!kIsWeb &&
          balance != null &&
          balance != _balance &&
          balance >= -1 &&
          balance <= 1) {
        _balance = balance;
        await player.setBalance(balance);
      }

      if (srcChanged && autoplay) {
        await player.resume();
      }

      var method = widget.control.attrString("method");
      if (method != null && method != _method) {
        _method = method;
        debugPrint("Audio JSON value: $_method");

        var mj = json.decode(method);
        var i = mj["i"] as int;
        var name = mj["n"] as String;
        var params = List<String>.from(mj["p"] as List);

        sendResult(Object? result, String? error) {
          ws.pageEventFromWeb(
              eventTarget: widget.control.id,
              eventName: "result",
              eventData: json.encode({
                "i": i,
                "r": result != null ? json.encode(result) : null,
                "e": error
              }));
        }

        switch (name) {
          case "play":
            await player.seek(const Duration(milliseconds: 0));
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
            await player
                .seek(Duration(milliseconds: int.tryParse(params[0]) ?? 0));
            break;
          case "get_duration":
            sendResult(
                (await player.getDuration())?.inMilliseconds.toString(), null);
            break;
          case "get_current_position":
            sendResult(
                (await player.getCurrentPosition())?.inMilliseconds.toString(),
                null);
            break;
        }
      }
    }();

    return const SizedBox.shrink();
  }
}
