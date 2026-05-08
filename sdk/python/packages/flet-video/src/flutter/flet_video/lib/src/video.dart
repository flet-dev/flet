import 'dart:async';

import 'package:collection/collection.dart';
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
  GlobalKey<VideoState> _videoKey = GlobalKey<VideoState>();
  StreamSubscription<String?>? _errorSub;
  StreamSubscription<bool>? _completedSub;
  StreamSubscription<Playlist>? _playlistSub;
  StreamSubscription<Duration>? _positionSub;
  StreamSubscription<Duration>? _durationSub;
  late Player _player;
  late VideoController _controller;
  bool _initialized = false;
  Future<void>? _openFuture;

  /// Snapshot of the last-known playlist, used to diff against incoming
  /// updates so single add/remove changes can be applied without a full reload.
  dynamic _playlist;

  /// Deep equality used to compare playlist entries (lists of media maps).
  static const _playlistEquality = DeepCollectionEquality();

  /// Returns a deep copy of [value] so the snapshot is decoupled from the
  /// source and won't be mutated by reference.
  dynamic _copyPlaylist(dynamic value) {
    if (value is List) {
      return value.map(_copyPlaylist).toList();
    }
    if (value is Map) {
      return value.map((key, value) => MapEntry(key, _copyPlaylist(value)));
    }
    return value;
  }

  /// Returns the appended media if [current] differs from [previous] only by
  /// a single trailing item, otherwise `null`.
  dynamic _appendedPlaylistMedia(List previous, List current) {
    if (current.length != previous.length + 1) {
      return null;
    }
    for (var i = 0; i < previous.length; i++) {
      if (!_playlistEquality.equals(previous[i], current[i])) {
        return null;
      }
    }
    return current.last;
  }

  /// Returns the removed index if [current] differs from [previous] only by
  /// a single removed item, otherwise `null`.
  int? _removedPlaylistIndex(List previous, List current) {
    if (previous.length != current.length + 1) {
      return null;
    }

    int? removedIndex;
    var currentIndex = 0;
    for (var previousIndex = 0;
        previousIndex < previous.length;
        previousIndex++) {
      if (currentIndex < current.length &&
          _playlistEquality.equals(
              previous[previousIndex], current[currentIndex])) {
        currentIndex++;
      } else if (removedIndex == null) {
        removedIndex = previousIndex;
      } else {
        return null;
      }
    }
    return removedIndex;
  }

  /// Applies an updated [playlist] by issuing a single `add` or `remove` when
  /// the diff is a one-item append/removal; otherwise falls back to reopening
  /// the player with the full playlist (preserving play state).
  Future<void> _updatePlaylist(dynamic playlist) async {
    final previousPlaylist = _playlist;
    _playlist = _copyPlaylist(playlist);

    if (previousPlaylist is List && playlist is List) {
      // add
      final addedMedia = _appendedPlaylistMedia(previousPlaylist, playlist);
      if (addedMedia != null) {
        final media = parseVideoMedia(addedMedia, widget.control.backend);
        if (media != null) {
          await _player.add(media);
          return;
        }
      }

      // remove
      final removedIndex = _removedPlaylistIndex(previousPlaylist, playlist);
      if (removedIndex != null) {
        await _player.remove(removedIndex);
        return;
      }
    }

    final play =
        widget.control.getBool("autoplay", false)! || _player.state.playing;
    await _player.open(
        Playlist(parseVideoMedias(playlist, widget.control.backend, [])!),
        play: play);
  }

  Future<void> _applyMpvProperties(Control control) async {
    final cfg = control.get("configuration");
    if (cfg is! Map) return;

    final mpvPropsRaw = cfg["mpv_properties"];
    if (mpvPropsRaw is! Map) return;

    final platform = _player.platform;
    if (platform is! NativePlayer) return;
    final native = platform as dynamic;

    for (final entry in mpvPropsRaw.entries) {
      final key = entry.key.toString();
      final val = entry.value;
      if (val == null) continue;
      final valueStr = val is bool ? (val ? "yes" : "no") : val.toString();
      await native.setProperty(key, valueStr);
    }
  }

  void _setup(Control control) {
    final playerConfig = PlayerConfiguration(
      title: control.getString("title", "flet-video")!,
      muted: control.getBool("muted", false)!,
      pitch: control.getDouble("pitch") != null,
      ready: control.hasEventHandler("load")
          ? () => control.triggerEvent("load")
          : null,
    );

    _player = Player(configuration: playerConfig);

    final videoControllerConfiguration = parseControllerConfiguration(
        control.get("configuration"), const VideoControllerConfiguration())!;
    _controller =
        VideoController(_player, configuration: videoControllerConfiguration);

    _initialized = true;

    control.addInvokeMethodListener(_invokeMethod);

    if (control.hasEventHandler("error")) {
      _errorSub = _player.stream.error.listen((message) {
        control.triggerEvent("error", message);
      });
    }

    if (control.hasEventHandler("complete")) {
      _completedSub = _player.stream.completed.listen((completed) {
        control.triggerEvent("complete", completed);
      });
    }

    if (control.hasEventHandler("track_change")) {
      _playlistSub = _player.stream.playlist.listen((playlist) {
        control.triggerEvent("track_change", playlist.index);
      });
    }

    if (control.hasEventHandler("position_change")) {
      _positionSub = _player.stream.position.listen((position) {
        control.triggerEvent("position_change", position);
      });
    }

    if (control.hasEventHandler("duration_change")) {
      _durationSub = _player.stream.duration.listen((duration) {
        control.triggerEvent("duration_change", duration);
      });
    }

    final playlist =
        Playlist(parseVideoMedias(control.get("playlist"), control.backend, [])!);
    final autoplay = control.getBool("autoplay", false)!;
    _playlist = _copyPlaylist(control.get("playlist"));

    _openFuture = () async {
      await _applyMpvProperties(control);
      await _player.open(playlist, play: autoplay);
    }();
  }

  void _teardown(Control control) {
    if (!_initialized) {
      return;
    }

    control.removeInvokeMethodListener(_invokeMethod);

    _errorSub?.cancel();
    _errorSub = null;
    _completedSub?.cancel();
    _completedSub = null;
    _playlistSub?.cancel();
    _playlistSub = null;
    _positionSub?.cancel();
    _positionSub = null;
    _durationSub?.cancel();
    _durationSub = null;

    _player.dispose();
    _openFuture = null;
    _initialized = false;
  }

  Future<void> _handleEnterFullscreen() async {
    widget.control.updateProperties({"_fullscreen": true}, python: false);
    if (!widget.control.getBool("fullscreen", false)!) {
      widget.control.updateProperties({"fullscreen": true});
    }
    widget.control.triggerEvent("enter_fullscreen");
    await defaultEnterNativeFullscreen();
  }

  Future<void> _handleExitFullscreen() async {
    widget.control.updateProperties({"_fullscreen": false}, python: false);
    if (widget.control.getBool("fullscreen", false)!) {
      widget.control.updateProperties({"fullscreen": false});
    }
    widget.control.triggerEvent("exit_fullscreen");
    await defaultExitNativeFullscreen();
  }

  @override
  void initState() {
    super.initState();
    _setup(widget.control);
  }

  @override
  void didUpdateWidget(covariant VideoControl oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (oldWidget.control != widget.control) {
      _teardown(oldWidget.control);
      _videoKey = GlobalKey<VideoState>();
      _setup(widget.control);
    }
  }

  @override
  void dispose() {
    _teardown(widget.control);
    super.dispose();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Video.$name($args)");
    switch (name) {
      case "play":
        await _player.play();
        break;
      case "pause":
        await _player.pause();
        break;
      case "play_or_pause":
        await _player.playOrPause();
        break;
      case "stop":
        await _player.stop();
        _player.open(
            Playlist(parseVideoMedias(
                widget.control.get("playlist"), widget.control.backend, [])!),
            play: false);
        break;
      case "seek":
        var position = parseDuration(args["position"]);
        if (position != null) await _player.seek(position);
        break;
      case "next":
        await _player.next();
        break;
      case "previous":
        await _player.previous();
        break;
      case "jump_to":
        final mediaIndex = parseInt(args["media_index"]);
        if (mediaIndex != null) await _player.jump(mediaIndex);
        break;
      case "is_playing":
        return _player.state.playing;
      case "is_completed":
        return _player.state.completed;
      case "get_duration":
        return _player.state.duration;
      case "get_current_position":
        return _player.state.position;
      case "take_screenshot":
        await _openFuture;
        if (!_initialized) return null;
        final format =
            args.containsKey("format") ? args["format"] : "image/png";
        return await _player.screenshot(
          format: format,
          includeLibassSubtitles: args["include_libass_subtitles"] == true,
        );
      default:
        throw Exception("Unknown Video method: $name");
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Video build: ${widget.control.id}");

    var subtitleConfiguration = parseSubtitleConfiguration(
        widget.control.get("subtitle_configuration"),
        Theme.of(context),
        const SubtitleViewConfiguration())!;
    var subtitleTrack =
        parseSubtitleTrack(widget.control.get("subtitle_track"), context);

    var volume = widget.control.getDouble("volume");
    var pitch = widget.control.getDouble("pitch");
    var playbackRate = widget.control.getDouble("playback_rate");
    var playlist = widget.control.get("playlist");
    var shufflePlaylist = widget.control.getBool("shuffle_playlist");
    var controls = widget.control.getBool("show_controls", true)!
        ? widget.control.get("controls")
        : null;
    var playlistMode =
        parsePlaylistMode(widget.control.getString("playlist_mode"));
    var fullscreen = widget.control.getBool("fullscreen", false)!;

    // previous values
    final prevVolume = widget.control.getDouble("_volume");
    final prevPitch = widget.control.getDouble("_pitch");
    final prevPlaybackRate = widget.control.getDouble("_playback_rate");
    final prevShufflePlaylist = widget.control.getBool("_shuffle_playlist");
    final PlaylistMode? prevPlaylistMode = widget.control.get("_playlist_mode");
    final SubtitleTrack? prevSubtitleTrack =
        widget.control.get("_subtitle_track");
    final prevFullscreen = widget.control.getBool("_fullscreen", false)!;

    Video video = Video(
      key: _videoKey,
      controller: _controller,
      wakelock: widget.control.getBool("wakelock", true)!,
      controls: parseVideoControls(controls),
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
      onEnterFullscreen: _handleEnterFullscreen,
      onExitFullscreen: _handleExitFullscreen,
    );

    final themedVideo =
        wrapVideoControlsTheme(video, controls, Theme.of(context));

    () async {
      // volume
      if (volume != null &&
          volume != prevVolume &&
          volume >= 0 &&
          volume <= 100) {
        widget.control.updateProperties({"_volume": volume}, python: false);
        await _player.setVolume(volume);
      }

      // pitch
      if (pitch != null && pitch != prevPitch) {
        widget.control.updateProperties({"_pitch": pitch}, python: false);
        await _player.setPitch(pitch);
      }

      // playbackRate
      if (playbackRate != null && playbackRate != prevPlaybackRate) {
        widget.control
            .updateProperties({"_playback_rate": playbackRate}, python: false);
        await _player.setRate(playbackRate);
      }

      // playlist
      if (!_playlistEquality.equals(playlist, _playlist)) {
        await _updatePlaylist(playlist);
      }

      // shufflePlaylist
      if (shufflePlaylist != null && shufflePlaylist != prevShufflePlaylist) {
        widget.control.updateProperties({"_shuffle_playlist": shufflePlaylist},
            python: false);
        await _player.setShuffle(shufflePlaylist);
      }

      // playlistMode
      if (playlistMode != null && playlistMode != prevPlaylistMode) {
        widget.control
            .updateProperties({"_playlist_mode": playlistMode}, python: false);
        await _player.setPlaylistMode(playlistMode);
      }

      // subtitleTrack
      if (subtitleTrack != null && subtitleTrack != prevSubtitleTrack) {
        await _openFuture;
        if (!_initialized) return;
        widget.control.updateProperties({"_subtitle_track": subtitleTrack},
            python: false);
        await _player.setSubtitleTrack(subtitleTrack);
      }

      // fullscreen
      if (fullscreen != prevFullscreen) {
        widget.control
            .updateProperties({"_fullscreen": fullscreen}, python: false);
        // Defer fullscreen transition until after this frame's build completes.
        WidgetsBinding.instance.addPostFrameCallback((_) {
          final videoState = _videoKey.currentState;
          if (videoState == null) {
            return;
          }
          if (fullscreen) {
            videoState.enterFullscreen();
          } else {
            videoState.exitFullscreen();
          }
        });
      }
    }();

    return LayoutControl(control: widget.control, child: themedVideo);
  }
}
