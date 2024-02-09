import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import '../utils/alignment.dart';
import '../utils/colors.dart';
import '../utils/images.dart';
import '../utils/numbers.dart';
import '../utils/video.dart';
import 'create_control.dart';

class VideoControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;
  final FletControlBackend backend;

  const VideoControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.parentDisabled,
      required this.backend});

  @override
  State<VideoControl> createState() => _VideoControlState();
}

class _VideoControlState extends State<VideoControl> {
  late final playerConfig = PlayerConfiguration(
    title: widget.control.attrString("title", "Flet Video")!,
    muted: widget.control.attrBool("muted", false)!,
    pitch: widget.control.attrDouble("pitch") != null ? true : false,
    ready: () {
      if (widget.control.attrBool("onLoaded", false)!) {
        widget.backend.triggerControlEvent(widget.control.id, "loaded", "");
      }
    },
  );

  late final Player player = Player(
    configuration: playerConfig,
  );
  late final controller = VideoController(player);

  @override
  void initState() {
    super.initState();
    player.open(Playlist(parseVideoMedia(widget.control, "playlist")),
        play: widget.control.attrBool("autoPlay", false)!);
  }

  @override
  void dispose() {
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Video build: ${widget.control.id}");

    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    FilterQuality filterQuality = FilterQuality.values.firstWhere((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("filterQuality", "low")!.toLowerCase());

    double? volume = widget.control.attrDouble("volume");
    double? pitch = widget.control.attrDouble("pitch");
    double? playbackRate = widget.control.attrDouble("playbackRate");
    bool? shufflePlaylist = widget.control.attrBool("shufflePlaylist");
    PlaylistMode? playlistMode = PlaylistMode.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("playlistMode")?.toLowerCase());

    final double? prevVolume = widget.control.state["volume"];
    final double? prevPitch = widget.control.state["pitch"];
    final double? prevPlaybackRate = widget.control.state["playbackRate"];
    final bool? prevShufflePlaylist = widget.control.state["shufflePlaylist"];
    final PlaylistMode? prevPlaylistMode = widget.control.state["playlistMode"];

    Video? video = Video(
      controller: controller,
      wakelock: widget.control.attrBool("wakelock", true)!,
      pauseUponEnteringBackgroundMode:
          widget.control.attrBool("pauseUponEnteringBackgroundMode", true)!,
      resumeUponEnteringForegroundMode:
          widget.control.attrBool("resumeUponEnteringForegroundMode", false)!,
      alignment:
          parseAlignment(widget.control, "alignment") ?? Alignment.center,
      fit: parseBoxFit(widget.control, "fit") ?? BoxFit.contain,
      filterQuality: filterQuality,
      fill: HexColor.fromString(
              Theme.of(context), widget.control.attrString("fillColor", "")!) ??
          const Color(0xFF000000),
      onEnterFullscreen: widget.control.attrBool("onEnterFullscreen", false)!
          ? () async {
              widget.backend.triggerControlEvent(
                  widget.control.id, "enter_fullscreen", "");
            }
          : defaultEnterNativeFullscreen,
      onExitFullscreen: widget.control.attrBool("onExitFullscreen", false)!
          ? () async {
              widget.backend.triggerControlEvent(
                  widget.control.id, "exit_fullscreen", "");
            }
          : defaultExitNativeFullscreen,
    );

    () async {
      if (volume != null &&
          volume != prevVolume &&
          volume >= 0 &&
          volume <= 100) {
        widget.control.state["volume"] = volume;
        debugPrint("Video.setVolume($volume)");
        await player.setVolume(volume);
      }

      if (pitch != null && pitch != prevPitch) {
        widget.control.state["pitch"] = pitch;
        debugPrint("Video.setPitch($pitch)");
        await player.setPitch(pitch);
      }

      if (playbackRate != null && playbackRate != prevPlaybackRate) {
        widget.control.state["playbackRate"] = playbackRate;
        debugPrint("Video.setPlaybackRate($playbackRate)");
        await player.setRate(playbackRate);
      }

      if (shufflePlaylist != null && shufflePlaylist != prevShufflePlaylist) {
        widget.control.state["shufflePlaylist"] = shufflePlaylist;
        debugPrint("Video.setShufflePlaylist($shufflePlaylist)");
        await player.setShuffle(shufflePlaylist);
      }

      if (playlistMode != null && playlistMode != prevPlaylistMode) {
        widget.control.state["playlistMode"] = playlistMode;
        debugPrint("Video.setPlaylistMode($playlistMode)");
        await player.setPlaylistMode(playlistMode);
      }

      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "play":
            debugPrint("Video.play($hashCode)");
            await player.play();
            break;
          case "pause":
            debugPrint("Video.pause($hashCode)");
            await player.pause();
            break;
          case "play_or_pause":
            debugPrint("Video.playOrPause($hashCode)");
            await player.playOrPause();
            break;
          case "stop":
            debugPrint("Video.stop($hashCode)");
            await player.stop();
            player.open(Playlist(parseVideoMedia(widget.control, "playlist")),
                play: false);
            break;
          case "seek":
            debugPrint("Video.jump($hashCode)");
            await player.seek(Duration(
                milliseconds: int.tryParse(args["position"] ?? "") ?? 0));
            break;
          case "next":
            debugPrint("Video.next($hashCode)");
            await player.next();
            break;
          case "previous":
            debugPrint("Video.previous($hashCode)");
            await player.previous();
            break;
          case "jump_to":
            debugPrint("Video.jump($hashCode)");
            await player.jump(parseInt(args["media_index"], 0));
            break;
          case "playlist_add":
            debugPrint("Video.add($hashCode)");
            Map<String, dynamic> extras =
                json.decode(args["extras"]!.replaceAll("'", "\""));
            Map<String, String> httpHeaders = (json
                    .decode(args["http_headers"]!.replaceAll("'", "\"")) as Map)
                .map(
                    (key, value) => MapEntry(key.toString(), value.toString()));
            await player.add(Media(args["resource"]!,
                extras: extras.isNotEmpty ? extras : null,
                httpHeaders: httpHeaders.isNotEmpty ? httpHeaders : null));
            break;
          case "playlist_remove":
            debugPrint("Video.remove($hashCode)");
            await player.remove(parseInt(args["media_index"], 0));
            break;
        }
        return null;
      });
    }();

    return constrainedControl(context, video, widget.parent, widget.control);
  }
}
