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

  const ImageControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Image build: ${control.id}");

    var src = control.attrString("src", "")!;
    if (src == "") {
      return const ErrorControl("Image must have 'src' specified.");
    }

    double? width = control.attrDouble("width", null);
    double? height = control.attrDouble("height", null);
    var repeat = ImageRepeat.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("repeat", "")!.toLowerCase(),
        orElse: () => ImageRepeat.noRepeat);
    var fit = BoxFit.values.firstWhere(
        (e) =>
            e.name.toLowerCase() ==
            control.attrString("fit", "")!.toLowerCase(),
        orElse: () => BoxFit.none);

    var uri = Uri.parse(src);
    if (!uri.hasAuthority) {
      // wrap into StoreConnector
      return StoreConnector<AppState, Uri?>(
          distinct: true,
          converter: (store) => store.state.pageUri,
          builder: (context, pageUri) {
            return baseControl(
                _clipCorners(
                    Image.network(getAssetUri(pageUri!, src).toString(),
                        width: width, height: height, repeat: repeat, fit: fit),
                    control),
                parent,
                control);
          });
    } else {
      return baseControl(
          _clipCorners(
              Image.network(src,
                  width: width, height: height, repeat: repeat, fit: fit),
              control),
          parent,
          control);
    }
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
