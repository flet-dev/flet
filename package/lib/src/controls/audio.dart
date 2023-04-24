import 'dart:convert';

import 'package:audioplayers/audioplayers.dart';
import 'package:collection/collection.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/page_args_model.dart';
import '../protocol/update_control_props_payload.dart';
import '../utils/images.dart';
import 'error.dart';

class AudioControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final dynamic dispatch;
  final Widget? nextChild;

  const AudioControl(
      {Key? key,
      required this.parent,
      required this.control,
      required this.dispatch,
      required this.nextChild})
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
  double? _playbackRate;
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
    double? playbackRate = widget.control.attrDouble("playbackRate", null);
    var releaseMode = ReleaseMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("releaseMode", "")!.toLowerCase());
    bool onPositionChanged =
        widget.control.attrBool("onPositionChanged", false)!;

    var server = FletAppServices.of(context).server;

    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: (context, pageArgs) {
          _onDurationChanged = (duration) {
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "duration_changed",
                eventData: duration.inMilliseconds.toString());
          };

          _onStateChanged = (state) {
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "state_changed",
                eventData: state.name.toString());
          };

          if (onPositionChanged) {
            _onPositionChanged = (duration) {
              server.sendPageEvent(
                  eventTarget: widget.control.id,
                  eventName: "position_changed",
                  eventData: duration.toString());
            };
          }

          _onSeekComplete = () {
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "seek_complete",
                eventData: "");
          };

          () async {
            bool srcChanged = false;
            if (src != "" && src != _src) {
              _src = src;
              srcChanged = true;

              // URL or file?
              var assetSrc =
                  getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);
              if (assetSrc.isFile) {
                await player.setSourceDeviceFile(assetSrc.path);
              } else {
                await player.setSourceUrl(assetSrc.path);
              }
            } else if (srcBase64 != "" && srcBase64 != _srcBase64) {
              _srcBase64 = srcBase64;
              srcChanged = true;
              await player.setSourceBytes(base64Decode(srcBase64));
            }

            if (srcChanged) {
              server.sendPageEvent(
                  eventTarget: widget.control.id,
                  eventName: "loaded",
                  eventData: "");
            }

            if (releaseMode != null && releaseMode != _releaseMode) {
              _releaseMode = releaseMode;
              await player.setReleaseMode(releaseMode);
            }

            if (volume != null &&
                volume != _volume &&
                volume >= 0 &&
                volume <= 1) {
              _volume = volume;
              await player.setVolume(volume);
            }

            if (playbackRate != null &&
                playbackRate != _playbackRate &&
                playbackRate >= 0 &&
                playbackRate <= 2) {
              _playbackRate = playbackRate;
              await player.setPlaybackRate(playbackRate);
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
              debugPrint("Audio JSON method: $method, $_method");

              List<Map<String, String>> props = [
                {"i": widget.control.id, "method": ""}
              ];
              widget.dispatch(UpdateControlPropsAction(
                  UpdateControlPropsPayload(props: props)));
              server.updateControlProps(props: props);

              var mj = json.decode(method);
              var i = mj["i"] as int;
              var name = mj["n"] as String;
              var params = List<String>.from(mj["p"] as List);

              sendResult(Object? result, String? error) {
                server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "method_result",
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
                  await player.seek(
                      Duration(milliseconds: int.tryParse(params[0]) ?? 0));
                  break;
                case "get_duration":
                  sendResult(
                      (await player.getDuration())?.inMilliseconds.toString(),
                      null);
                  break;
                case "get_current_position":
                  sendResult(
                      (await player.getCurrentPosition())
                          ?.inMilliseconds
                          .toString(),
                      null);
                  break;
              }
            }
          }();

          return widget.nextChild ?? const SizedBox.shrink();
        });
  }
}
