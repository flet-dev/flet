import 'package:flet_view/controls/create_control.dart';
import 'package:flet_view/controls/error.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/uri.dart';

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
        (e) => e.name.toLowerCase() == control.attrString("repeat", "")!,
        orElse: () => ImageRepeat.noRepeat);
    var fit = BoxFit.values.firstWhere(
        (e) => e.name.toLowerCase() == control.attrString("fit", "")!,
        orElse: () => BoxFit.none);

    var uri = Uri.parse(src);
    if (!uri.hasAuthority) {
      // wrap into StoreConnector
      return StoreConnector<AppState, Uri?>(
          distinct: true,
          converter: (store) => store.state.pageUri,
          builder: (context, pageUri) {
            return baseControl(
                Image.network(getAssetUrl(pageUri!, src),
                    width: width, height: height, repeat: repeat, fit: fit),
                parent,
                control);
          });
    } else {
      return baseControl(
          Image.network(src,
              width: width, height: height, repeat: repeat, fit: fit),
          parent,
          control);
    }
  }
}
