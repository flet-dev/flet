import 'dart:convert';

import 'package:flet_view/utils/images.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/uri.dart';
import 'create_control.dart';
import 'error.dart';

class ImageControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ImageControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var src = control.attrString("src", "")!;
    var srcBase64 = control.attrString("srcBase64", "")!;
    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Image must have 'src' or 'src_base64' specified.");
    }
    double? width = control.attrDouble("width", null);
    double? height = control.attrDouble("height", null);
    var repeat = parseImageRepeat(control, "repeat");
    var fit = parseBoxFit(control, "fit");

    var uri = Uri.parse(src);
    return StoreConnector<AppState, Uri?>(
        distinct: true,
        converter: (store) => store.state.pageUri,
        builder: (context, pageUri) {
          Image? image;

          if (srcBase64 != "") {
            try {
              Uint8List bytes = base64Decode(srcBase64);
              image = Image.memory(bytes,
                  width: width, height: height, repeat: repeat, fit: fit);
            } catch (ex) {
              return ErrorControl("Error decoding base64: ${ex.toString()}");
            }
          } else {
            image = Image.network(
                uri.hasAuthority ? src : getAssetUri(pageUri!, src).toString(),
                width: width,
                height: height,
                repeat: repeat,
                fit: fit);
          }

          return constrainedControl(
              _clipCorners(image, control), parent, control);
        });
  }

  Widget _clipCorners(Widget image, Control control) {
    var borderRadius = parseBorderRadius(control, "borderRadius");
    return borderRadius != null
        ? ClipRRect(
            borderRadius: borderRadius,
            child: image,
          )
        : image;
  }
}
