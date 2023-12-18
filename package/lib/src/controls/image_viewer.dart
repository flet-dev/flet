import 'package:easy_image_viewer/easy_image_viewer.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/page_args_model.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/images.dart';

class ImageViewerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final bool parentDisabled;

  const ImageViewerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<ImageViewerControl> createState() => _ImageViewerControlState();
}

class _ImageViewerControlState extends State<ImageViewerControl> {
  bool _open = false;

  @override
  Widget build(BuildContext context) {
    debugPrint("ImageViewer build: ${widget.control.id}");
    
    var src = widget.control.attrString("src", "")!;
    bool swipeDismissible = widget.control.attrBool("swipeDismissible", true)!;
    bool doubleTapZoomable = widget.control.attrBool("doubleTapZoomable", true)!;
    String closeButtonTooltip = widget.control.attrString("closeButtonTooltip", "Close")!;
    var backgroundColor = HexColor.fromString(
        Theme.of(context), widget.control.attrString("backgroundColor", "black")!);
    var closeButtonColor = HexColor.fromString(
          Theme.of(context), widget.control.attrString("closeButtonColor", "white")!);
    bool immersive = widget.control.attrBool("immersive", true)!;
    var initialIndex = widget.control.attrInt("initialIndex", 0)!;

    return StoreConnector<AppState, PageArgsModel>(
        distinct: true,
        converter: (store) => PageArgsModel.fromStore(store),
        builder: (context, pageArgs) {
          EasyImageProvider? imageProvider;
          if (src.contains('|')) {
            List<ImageProvider<Object>> imageList = [];
            for (String img in src.split('|')) {
              var imageSrc = getAssetSrc(img, pageArgs.pageUri!, pageArgs.assetsDir);
              imageList.add(imageSrc.isFile ? getFileImageProvider(imageSrc.path) : NetworkImage(imageSrc.path));
            }
            imageProvider = MultiImageProvider(imageList, initialIndex: initialIndex);
          } else {
            var imageSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);
            imageProvider = SingleImageProvider(imageSrc.isFile ? getFileImageProvider(imageSrc.path) : NetworkImage(imageSrc.path));
          }
          
          debugPrint("ImageViewer StoreConnector build: ${widget.control.id}");

          var open = widget.control.attrBool("open", false)!;

          debugPrint("Current open state: $_open");
          debugPrint("New open state: $open");

          if (open && (open != _open)) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              showImageViewerPager(
                context,
                imageProvider!,
                swipeDismissible: swipeDismissible,
                doubleTapZoomable: doubleTapZoomable,
                backgroundColor: backgroundColor!,
                closeButtonColor: closeButtonColor!,
                closeButtonTooltip: closeButtonTooltip,
                immersive: immersive,
              );
            });
          }

          _open = open;

          return const SizedBox.shrink();
        });
  }
}
