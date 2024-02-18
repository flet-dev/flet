import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:lottie/lottie.dart';

class LottieControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const LottieControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<LottieControl> createState() => _LottieControlState();
}

class _LottieControlState extends State<LottieControl> with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Lottie build: ${widget.control.id} (${widget.control.hashCode})");

    var src = widget.control.attrString("src", "")!;
    var srcBase64 = widget.control.attrString("srcBase64", "")!;

    if (src == "" && srcBase64 == "") {
      return const ErrorControl(
          "Lottie must have either \"src\" or \"src_base64\" specified.");
    }

    var repeat = widget.control.attrBool("repeat");
    var backgroundLoading = widget.control.attrBool("backgroundLoading");
    var reverse = widget.control.attrBool("reverse");
    var animate = widget.control.attrBool("animate");
    var fit = parseBoxFit(widget.control, "fit");
    FilterQuality filterQuality = FilterQuality.values.firstWhere((e) =>
        e.name.toLowerCase() ==
        widget.control.attrString("filterQuality", "low")!.toLowerCase());

    void onWarning(String value) {
      if (widget.control.attrBool("onError", false)!) {
        widget.backend.triggerControlEvent(widget.control.id, "error", value);
      }
    }

    return withPageArgs((context, pageArgs) {
      Widget? lottie;

      if (srcBase64 != "") {
        try {
          Uint8List bytes = base64Decode(srcBase64);
          lottie = Lottie.memory(bytes,
              repeat: repeat,
              reverse: reverse,
              animate: animate,
              fit: fit,
              filterQuality: filterQuality,
              backgroundLoading: backgroundLoading,
              onWarning: onWarning);
        } catch (ex) {
          return ErrorControl("Error decoding base64: ${ex.toString()}");
        }
      } else {
        var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);
        if (assetSrc.isFile) {
          // Local File
          lottie = Lottie.asset(assetSrc.path,
              repeat: repeat,
              reverse: reverse,
              animate: animate,
              fit: fit,
              filterQuality: filterQuality,
              backgroundLoading: backgroundLoading,
              onWarning: onWarning);
        } else {
          // URL
          lottie = Lottie.network(assetSrc.path,
              repeat: repeat,
              reverse: reverse,
              animate: animate,
              fit: fit,
              filterQuality: filterQuality,
              backgroundLoading: backgroundLoading,
              onWarning: onWarning);
        }
      }

      return constrainedControl(context, lottie, widget.parent, widget.control);
    });
  }
}
