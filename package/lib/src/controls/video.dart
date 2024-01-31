import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

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
    // Play a [Media] or [Playlist].
    player.open(Media(
        'https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4'));
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
    double? width = widget.control.attrDouble("width", null);
    double? height = widget.control.attrDouble("height", null);
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var errorContentCtrls =
        widget.children.where((c) => c.name == "error_content" && c.isVisible);

    return withPageArgs((context, pageArgs) {
      Video? video = Video(controller: controller);

      // var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);

      return constrainedControl(context, video, widget.parent, widget.control);
    });
  }
}
