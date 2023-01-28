import 'package:easy_image_viewer/easy_image_viewer.dart';
import 'package:flutter/material.dart';
import '../utils/colors.dart';

/// Shows the given [imageProvider] in a full-screen [Dialog].
/// The optional [swipeDismissible] boolean defaults to false and allows swipe-down-to-dismiss.
/// The optional [doubleTapZoomable] boolean defaults to false and allows double tap to zoom.
/// The [backgroundColor] defaults to black, but can be set to any other color.
/// The [closeButtonColor] defaults to white, but can be set to any other color.
/// The [closeButtonTooltip] text is displayed when the user long-presses on the close button.
/// Setting [immersive] to false will prevent the top and bottom bars from being hidden.
/// The [initialIndex] is the image to start with in a MultiPage viewer.
Future openImageViewer(String image, bool swipeDismissible, bool doubleTapZoomable, String? backgroundColor, String? closeButtonColor, String? closeButtonTooltip, bool? immersive, int? initialIndex) async {
  List<String> imageList = [];
  var imageProvider;
  if (image.contains('|')) {
    for (String i in image.split('|')) {
      imageList.add(Image.network(i).image);
    }
    if (imageList.length > 1)
      imageProvider = MultiImageProvider(imageList, initialIndex = initialIndex);
    else
      imageProvider = SingleImageProvider(Image.network(image).image);
  } else
    imageProvider = SingleImageProvider(Image.network(image).image);
  return Builder(
    builder: (context) {
      var background_color = checkString(backgroundColor) ? HexColor.fromString(Theme.of(context), backgroundColor!) : Colors.black;
      var close_button_color = checkString(closeButtonColor) ? HexColor.fromString(Theme.of(context), closeButtonColor!) : Colors.white;
      showImageViewerPager(
        context,
        imageProvider,
        swipeDismissible = swipeDismissible,
        doubleTapZoomable = doubleTapZoomable,
        backgroundColor = background_color,
        closeButtonColor = close_button_color,
        closeButtonTooltip = closeButtonTooltip,
        immersive = immersive,
        initialIndex = initialIndex,
      );
    },
  );
}

bool checkString(value) => !(['', null, 0, false].contains(value));