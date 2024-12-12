import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:audio_service/audio_service.dart';
import 'package:rxdart/rxdart.dart';


import 'utils/video.dart';

class VideoControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const VideoControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<VideoControl> createState() => _VideoControlState();
}

class _VideoControlState extends State<VideoControl> with FletStoreMixin {
  int _lastProcessedIndex = -1;
  int _lastPercent = -1;
  late final playerConfig = PlayerConfiguration(
    title: widget.control.attrString("title", "Flet Video")!,
    muted: widget.control.attrBool("muted", false)!,
    pitch: widget.control.attrDouble("pitch") != null ? true : false,
    ready: () {
      if (widget.control.attrBool("onLoaded", false)!) {
        widget.backend.triggerControlEvent(widget.control.id, "loaded");
      }
    },
  );

  late final Player player = Player(
    configuration: playerConfig,
  );
  late final AudioHandler _audioHandler;

  late final videoControllerConfiguration = parseControllerConfiguration(
      widget.control, "configuration", const VideoControllerConfiguration())!;
  late final controller =
      VideoController(player, configuration: videoControllerConfiguration);


  @override
  void initState() {
    super.initState();

    AudioService.init(
      builder: () => MyAudioHandler(player),
      config: const AudioServiceConfig(
        androidNotificationChannelId: 'com.appveyor.flet.channel.audio',
        androidNotificationChannelName: 'Audio playback',
        androidNotificationOngoing: true,
      ),
    ).then((handler) {
      _audioHandler = handler;
      // Now you can use _audioHandler for audio service operations
    }).catchError((error) {
      // Handle errors during initialization
      debugPrint('Error initializing AudioService: $error');
    });
    player.open(Playlist(parseVideoMedia(widget.control, "playlist")),
        play: widget.control.attrBool("autoPlay", false)!);

  }

  @override
  void dispose() {
    player.dispose();
    super.dispose();
  }

  void _onError(String? message) {
    debugPrint("Video onError: $message");
    widget.backend
        .triggerControlEvent(widget.control.id, "error", message ?? "");
  }

  void _onCompleted(String? message) {
  debugPrint("Video onCompleted: $message");
  widget.backend
      .triggerControlEvent(widget.control.id, "completed", message ?? "");
  }

  void _onTrackChanged(String? message) {
  debugPrint("Video onTrackChanged: $message");
  widget.backend
      .triggerControlEvent(widget.control.id, "track_changed", message ?? "");
  }

  void _onPercentChanged(String? message) {
    // Let's not debug print this, cause to much traffic on console
    // debugPrint("Video onPercentChanged: $message");
    widget.backend
        .triggerControlEvent(widget.control.id, "percent_changed", message ?? "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Video build: ${widget.control.id}");

    FilterQuality filterQuality = parseFilterQuality(
        widget.control.attrString("filterQuality"), FilterQuality.low)!;

    return withPageArgs((context, pageArgs) {
      SubtitleTrack? subtitleTrack;
      Map<String, dynamic>? subtitleConfiguration = parseSubtitleConfiguration(
          Theme.of(context), widget.control, "subtitleConfiguration");
      if (subtitleConfiguration?["src"] != null) {
        try {
          var assetSrc = getAssetSrc(subtitleConfiguration?["src"],
              pageArgs.pageUri!, pageArgs.assetsDir);
          subtitleTrack = parseSubtitleTrack(
              assetSrc,
              subtitleConfiguration?["title"],
              subtitleConfiguration?["language"]);
        } catch (ex) {
          _onError(ex.toString());
          subtitleTrack = SubtitleTrack.no();
        }
      }

      SubtitleViewConfiguration? subtitleViewConfiguration =
          subtitleConfiguration?["subtitleViewConfiguration"];

      bool onError = widget.control.attrBool("onError", false)!;
      bool onCompleted = widget.control.attrBool("onCompleted", false)!;
      bool onTrackChanged = widget.control.attrBool("onTrackChanged", false)!;
      bool onPercentChanged = widget.control.attrBool("onPercentChanged", false)!;

      double? volume = widget.control.attrDouble("volume");
      double? pitch = widget.control.attrDouble("pitch");
      double? playbackRate = widget.control.attrDouble("playbackRate");
      bool? shufflePlaylist = widget.control.attrBool("shufflePlaylist");
      bool? showControls = widget.control.attrBool("showControls", true)!;
      PlaylistMode? playlistMode = PlaylistMode.values.firstWhereOrNull((e) =>
          e.name.toLowerCase() ==
          widget.control.attrString("playlistMode")?.toLowerCase());

      final double? prevVolume = widget.control.state["volume"];
      final double? prevPitch = widget.control.state["pitch"];
      final double? prevPlaybackRate = widget.control.state["playbackRate"];
      final bool? prevShufflePlaylist = widget.control.state["shufflePlaylist"];
      final PlaylistMode? prevPlaylistMode =
          widget.control.state["playlistMode"];
      final SubtitleTrack? prevSubtitleTrack =
          widget.control.state["subtitleTrack"];

      Video? video = Video(
        controller: controller,
        wakelock: widget.control.attrBool("wakelock", true)!,
        controls: showControls ? AdaptiveVideoControls : null,
        pauseUponEnteringBackgroundMode:
            widget.control.attrBool("pauseUponEnteringBackgroundMode", true)!,
        resumeUponEnteringForegroundMode:
            widget.control.attrBool("resumeUponEnteringForegroundMode", false)!,
        alignment:
            parseAlignment(widget.control, "alignment", Alignment.center)!,
        fit: parseBoxFit(widget.control.attrString("fit"), BoxFit.contain)!,
        filterQuality: filterQuality,
        subtitleViewConfiguration:
            subtitleViewConfiguration ?? const SubtitleViewConfiguration(),
        fill: parseColor(Theme.of(context),
                widget.control.attrString("fillColor", "")!) ??
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

        if (subtitleTrack != null && subtitleTrack != prevSubtitleTrack) {
          widget.control.state["subtitleTrack"] = subtitleTrack;
          debugPrint("Video.setSubtitleTrack($subtitleTrack)");
          await player.setSubtitleTrack(subtitleTrack);
        }

        widget.backend.subscribeMethods(widget.control.id,
            (methodName, args) async {
          switch (methodName) {
            case "play":
              debugPrint("Video.play($hashCode)");
              await _audioHandler.play();
              break;
            case "pause":
              debugPrint("Video.pause($hashCode)");
              await _audioHandler.pause();
              break;
            case "play_or_pause":
              debugPrint("Video.playOrPause($hashCode)");
              await _audioHandler.play();
              break;
            case "stop":
              debugPrint("Video.stop($hashCode)");
              await _audioHandler.stop();
              player.open(Playlist(parseVideoMedia(widget.control, "playlist")),
                  play: false);
              break;
            case "seek":
              debugPrint("Video.jump($hashCode)");
              await _audioHandler.seek(Duration(
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
              await player.jump(parseInt(args["media_index"], 0)!);
              break;
            case "playlist_add":
              debugPrint("Video.add($hashCode)");
              Map<String, dynamic> extras =
                  json.decode(args["extras"]!.replaceAll("'", "\""));
              Map<String, String> httpHeaders =
                  (json.decode(args["http_headers"]!.replaceAll("'", "\""))
                          as Map)
                      .map((key, value) =>
                          MapEntry(key.toString(), value.toString()));
              await player.add(Media(args["resource"]!,
                  extras: extras.isNotEmpty ? extras : null,
                  httpHeaders: httpHeaders.isNotEmpty ? httpHeaders : null));
              break;
            case "playlist_remove":
              debugPrint("Video.remove($hashCode)");
              await player.remove(parseInt(args["media_index"], 0)!);
              break;
            case "is_playing":
              debugPrint("Video.isPlaying($hashCode)");
              return player.state.playing.toString();
            case "is_completed":
              debugPrint("Video.isCompleted($hashCode)");
              return player.state.completed.toString();
            case "get_duration":
              debugPrint("Video.getDuration($hashCode)");
              return player.state.duration.inMilliseconds.toString();
            case "get_current_position":
              debugPrint("Video.getCurrentPosition($hashCode)");
              return player.state.position.inMilliseconds.toString();
          }
          return null;
        });
      }();

      player.stream.error.listen((event) {
        if (onError) {
          _onError(event.toString());
        }
      });

      player.stream.completed.listen((event) {
        if (onCompleted) {
          _onCompleted(event.toString());
        }
      });
      // Send percentage position change between 0-100 to use with flet slider.
      // This will make flet event loop less busy sending round int numbers
      // as well as throttling to 1 second to not overload flet socket
      player.stream.position.throttleTime(const Duration(seconds: 1)).listen((position) {
        if (onPercentChanged) {
          try {
            final int percent = (position.inMilliseconds / player.state.duration.inMilliseconds * 100).toInt();
            if (percent != _lastPercent) {
              _lastPercent = percent;
              _onPercentChanged(percent.toString());
            }
          } catch (e) {
            debugPrint("Error calculating percentage: $e");
          }
        }
      });

      player.stream.playlist.listen((event) {
        if (event.index != _lastProcessedIndex) { // prevent duplicates
          _lastProcessedIndex = event.index;
          if (onTrackChanged) {
            _onTrackChanged(event.index.toString());
          }
          // We want this outside of onTrackChanged as we need to update
          // notification bar regardless if they subscribed to handler or not.
          _audioHandler.customAction('update_notification', {'index': event.index});
        }
      });

      return constrainedControl(context, video, widget.parent, widget.control);
    });
  }
}

class MyAudioHandler extends BaseAudioHandler {
  final Player player;
  MyAudioHandler(this.player);
  final PlaybackState _basePlaybackState = PlaybackState(
    controls: [
      MediaControl.skipToPrevious,
      MediaControl.play,
      MediaControl.pause,
      MediaControl.skipToNext,
    ],
    systemActions: const {
      MediaAction.seek,
    },
    processingState: AudioProcessingState.ready,
  );

  @override
  Future<dynamic> customAction(String name,
      [Map<String, dynamic>? extras]) async {
    if (name == 'update_notification') {
      final index = extras?['index'] as int?;
      if (index != null) {
        updatePlaybackState(index);
      }
    } else {
      debugPrint("Unknown custom action: $name");
    }
  }

  @override
  Future<void> play() async {
    try {
      await player.playOrPause();
      // we need to trigger updatePlaybackState if first time hitting play
      // or seek on notification bar will not work correctly
      if (player.state.position.inMilliseconds == 0) {
        updatePlaybackState(player.state.playlist.index);
      } else {
        playbackState.add(_basePlaybackState.copyWith(playing: player.state.playing, updatePosition: player.state.position));
      }
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }

  @override
  Future<void> pause() async {
    try {
      await player.playOrPause();
      playbackState.add(_basePlaybackState.copyWith(playing: player.state.playing, updatePosition: player.state.position));
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }

  @override
  Future<void> stop() async {
    try {
      await player.stop();
      playbackState.add(_basePlaybackState.copyWith(playing: player.state.playing, updatePosition: player.state.position));
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }
  // Because these 2 functions are changing songs, no need to call
  // playbackState as track change will trigger player.stream.playlist.listen
  // to call updatePlaybackState() to do it for us, still required for
  // bluetooth etc devices to work correctly
  @override
  Future<void> skipToNext() async {
    try {
      await player.next();
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }

  @override
  Future<void> skipToPrevious() async {
    try {
      await player.previous();
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }

  @override
  Future<void> seek(Duration position) async {
    try {
      await player.seek(position);
      playbackState.add(_basePlaybackState.copyWith(playing: player.state.playing, updatePosition: position));
    } catch (e) {
      debugPrint("Playback error: ${e}");
    }
  }

  void updatePlaybackState(int index) {
    final currentMedia = player.state.playlist.medias[index];
    final extras = currentMedia.extras;
    // Url Decode and extract filename
    // I am going to assume structure of https://blah.com/Artist - SongName.mp3
    // Let's attempt to split their filename into title/artist if they did not
    // include extras { title and artist } as full http url would be ugly
    final filename = Uri.decodeFull(player.state.playlist.medias[index].uri.split('/').last);
    final parts = filename.split('.');
    final filenameWithoutExtension = parts.sublist(0, parts.length - 1).join('.');
    final artistAndTitle = filenameWithoutExtension.split('-');
    final title = extras?['title'] ?? artistAndTitle.last.trim();
    final artist = extras?['artist'] ?? artistAndTitle.sublist(0, artistAndTitle.length - 1).join('-').trim();
    final artUri = extras?['artUri'] as String?;
    final album = extras?['album'] as String?;
    final genre = extras?['genre'] as String?;
    final displayTitle = extras?['displayTitle'] as String?;
    final displaySubtitle = extras?['displaySubtitle'] as String?;
    final displayDescription = extras?['displayDescription'] as String?;

    mediaItem.add(MediaItem(
      id: index.toString(),
      title: title,
      artist: artist,
      artUri: artUri != null ? Uri.parse(artUri) : null,
      album: album != null ? album : null,
      genre: genre != null ? genre : null,
      displayTitle: displayTitle != null ? displayTitle : null,
      displaySubtitle: displaySubtitle != null ? displaySubtitle : null,
      displayDescription: displayDescription != null ? displayDescription : null,
      duration: player.state.duration,
    ));
    playbackState.add(_basePlaybackState.copyWith(playing: player.state.playing, updatePosition: Duration.zero));
    debugPrint("Now playing: ${player.state.playlist.medias[index].uri} with index ${player.state.playlist.index}");
  }
}