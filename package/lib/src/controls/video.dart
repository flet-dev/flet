import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

import '../flet_app_services.dart';

class VideoControl extends StatefulWidget {
  final Control? parent;
  final List<Control> children;
  final Control control;
  final bool parentDisabled;

  const VideoControl(
      {super.key,
      required this.parent,
      required this.children,
      required this.control,
      required this.parentDisabled});

  @override
  State<VideoControl> createState() => _VideoControlState();
}

class _VideoControlState extends State<VideoControl>
    with FletControlStatefulMixin, FletStoreMixin {
  late final Player player = Player(
    configuration: PlayerConfiguration(
      // Supply your options:
      title: 'My awesome package:media_kit application',
      ready: () {
        debugPrint('VIDEO: The initialization is complete.');
      },
    ),
  );
  late final controller = VideoController(player);

  @override
  void initState() {
    super.initState();
    player.open(
        Playlist([
          Media(
              'https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4')
        ]),
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

    var src = widget.control.attrString("src", "")!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    FilterQuality filterQuality = FilterQuality.values.firstWhere((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("filterQuality", "low")!.toLowerCase());

    Future<void> onEnterFullscreen() async {
      FletAppServices.of(context).server.sendPageEvent(
          eventTarget: widget.control.id,
          eventName: "enterFullscreen",
          eventData: "");
    }

    return withPageArgs((context, pageArgs) {
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
        fill: HexColor.fromString(Theme.of(context),
                widget.control.attrString("fillColor", "")!) ??
            const Color(0xFF000000),
        onEnterFullscreen: widget.control.attrBool("onEnterFullscreen", false)!
            ? () async {
                FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "enter_fullscreen",
                    eventData: "");
              }
            : defaultEnterNativeFullscreen,
        onExitFullscreen: widget.control.attrBool("onExitFullscreen", false)!
            ? () async {
                FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: widget.control.id,
                    eventName: "exit_fullscreen",
                    eventData: "");
              }
            : defaultExitNativeFullscreen,
      );

    () async {
      subscribeMethods(widget.control.id, (methodName, args) async {
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
            break;
          case "seek":
            await player.seek(Duration(
                milliseconds: int.tryParse(args["position"] ?? "") ?? 0));
            break;
          case "next":
            await player.next();
            break;
          case "previous":
            await player.previous();
            break;
          case "add_media":
            debugPrint("Video.addMedia(${args['media']}");
            // await player.add(); TODO
            break;
        }
        return null;
      });
    }();

      return constrainedControl(context, video, widget.parent, widget.control);
    });
  }
}
