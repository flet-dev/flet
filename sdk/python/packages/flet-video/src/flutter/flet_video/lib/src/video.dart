import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

import 'utils/video.dart';

class VideoControl extends StatefulWidget {
  final Control control;

  const VideoControl({super.key, required this.control});

  @override
  State<VideoControl> createState() => _VideoControlState();
}

class _VideoControlState extends State<VideoControl> with FletStoreMixin {
  late final playerConfig = PlayerConfiguration(
    title: widget.control.getString("title", "flet-video")!,
    muted: widget.control.getBool("muted", false)!,
    pitch: widget.control.getDouble("pitch") != null ? true : false,
    ready: widget.control.getBool("on_loaded", false)!
        ? () => widget.control.triggerEvent("loaded")
        : null,
  );

  late final Player player = Player(configuration: playerConfig);
  late final videoControllerConfiguration = parseControllerConfiguration(
      widget.control.get("configuration"),
      const VideoControllerConfiguration())!;
  late final controller =
      VideoController(player, configuration: videoControllerConfiguration);

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    player.open(Playlist(parseVideoMedias(widget.control.get("playlist"), [])!),
        play: widget.control.getBool("autoplay", false)!);
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    player.dispose();
    super.dispose();
  }

  void _onError(String? message) {
    if (widget.control.getBool("on_error", false)!) {
      widget.control.triggerEvent("error", message);
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Video.$name($args)");
    switch (name) {
      case "play":
        await player.play();
        break;
      case "pause":
        await player.pause();
        break;
      case "play_or_pause":
        await player.playOrPause();
        break;
      case "stop":
        await player.stop();
        player.open(
            Playlist(parseVideoMedias(widget.control.get("playlist"), [])!),
            play: false);
        break;
      case "seek":
        var position = parseDuration(args["position"]);
        if (position != null) await player.seek(position);
        break;
      case "next":
        await player.next();
        break;
      case "previous":
        await player.previous();
        break;
      case "jump_to":
        final mediaIndex = parseInt(args["media_index"]);
        if (mediaIndex != null) await player.jump(mediaIndex);
        break;
      case "playlist_add":
        var media = parseVideoMedia(args["media"]);
        if (media != null) await player.add(media);
        break;
      case "playlist_remove":
        final mediaIndex = parseInt(args["media_index"]);
        if (mediaIndex != null) await player.remove(mediaIndex);
        break;
      case "is_playing":
        return player.state.playing;
      case "is_completed":
        return player.state.completed;
      case "get_duration":
        return player.state.duration;
      case "get_current_position":
        return player.state.position;
      default:
        throw Exception("Unknown Video method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Video XXX build: ${widget.control.id}");

    var subtitleConfiguration = parseSubtitleConfiguration(
        widget.control.get("subtitle_configuration"),
        Theme.of(context),
        const SubtitleViewConfiguration())!;
    var subtitleTrack =
        parseSubtitleTrack(widget.control.get("subtitle_track"), context);

    var volume = widget.control.getDouble("volume");
    var pitch = widget.control.getDouble("pitch");
    var playbackRate = widget.control.getDouble("playback_rate");
    var shufflePlaylist = widget.control.getBool("shuffle_playlist");
    var showControls = widget.control.getBool("show_controls", true)!;
    var playlistMode =
        parsePlaylistMode(widget.control.getString("playlist_mode"));

    // previous values
    final prevVolume = widget.control.getDouble("_volume");
    final prevPitch = widget.control.getDouble("_pitch");
    final prevPlaybackRate = widget.control.getDouble("_playback_rate");
    final prevShufflePlaylist = widget.control.getBool("_shuffle_playlist");
    final PlaylistMode? prevPlaylistMode = widget.control.get("_playlist_mode");
    final SubtitleTrack? prevSubtitleTrack =
        widget.control.get("_subtitleTrack");

    Video video = Video(
      controller: controller,
      wakelock: widget.control.getBool("wakelock", true)!,
      controls: showControls ? AdaptiveVideoControls : null,
      pauseUponEnteringBackgroundMode:
          widget.control.getBool("pause_upon_entering_background_mode", true)!,
      resumeUponEnteringForegroundMode: widget.control
          .getBool("resume_upon_entering_foreground_mode", false)!,
      alignment: widget.control.getAlignment("alignment", Alignment.center)!,
      fit: widget.control.getBoxFit("fit", BoxFit.contain)!,
      filterQuality:
          widget.control.getFilterQuality("filter_quality", FilterQuality.low)!,
      subtitleViewConfiguration: subtitleConfiguration,
      fill: widget.control.getColor("fill_color", context, Colors.black)!,
      onEnterFullscreen: widget.control.getBool("on_enter_fullscreen", false)!
          ? () async => widget.control.triggerEvent("enter_fullscreen")
          : defaultEnterNativeFullscreen,
      onExitFullscreen: widget.control.getBool("on_exit_fullscreen", false)!
          ? () async => widget.control.triggerEvent("exit_fullscreen")
          : defaultExitNativeFullscreen,
    );

    () async {
      if (volume != null &&
          volume != prevVolume &&
          volume >= 0 &&
          volume <= 100) {
        widget.control.updateProperties({"_volume": volume}, python: false);
        await player.setVolume(volume);
      }

      if (pitch != null && pitch != prevPitch) {
        widget.control.updateProperties({"_pitch": pitch}, python: false);
        await player.setPitch(pitch);
      }

      if (playbackRate != null && playbackRate != prevPlaybackRate) {
        widget.control
            .updateProperties({"_playbackRate": playbackRate}, python: false);
        await player.setRate(playbackRate);
      }

      if (shufflePlaylist != null && shufflePlaylist != prevShufflePlaylist) {
        widget.control.updateProperties({"_shufflePlaylist": shufflePlaylist},
            python: false);
        await player.setShuffle(shufflePlaylist);
      }

      if (playlistMode != null && playlistMode != prevPlaylistMode) {
        widget.control
            .updateProperties({"_playlistMode": playlistMode}, python: false);
        await player.setPlaylistMode(playlistMode);
      }

      if (subtitleTrack != null && subtitleTrack != prevSubtitleTrack) {
        widget.control
            .updateProperties({"_subtitleTrack": subtitleTrack}, python: false);
        await player.setSubtitleTrack(subtitleTrack);
      }
    }();

    // listen to errors
    player.stream.error.listen((event) {
      _onError(event);
    });

    // listen to completion
    player.stream.completed.listen((event) {
      if (widget.control.getBool("on_complete", false)!) {
        widget.control.triggerEvent("complete", event);
      }
    });

    // listen to track changes
    player.stream.playlist.listen((event) {
      if (widget.control.getBool("on_track_change", false)!) {
        widget.control.triggerEvent("track_change", event.index);
      }
    });

    return ConstrainedControl(control: widget.control, child: video);
  }
}
