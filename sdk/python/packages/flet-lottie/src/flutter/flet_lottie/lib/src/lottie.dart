import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:lottie/lottie.dart';

class LottieControl extends StatefulWidget {
  final Control control;

  const LottieControl({super.key, required this.control});

  @override
  State<LottieControl> createState() => _LottieControlState();
}

class _LottieControlState extends State<LottieControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Lottie build: ${widget.control.id} (${widget.control.hashCode})");

    var src = widget.control.getString("src");
    var srcBase64 = widget.control.getString("src_base64");

    if (src == null && srcBase64 == null) {
      return const ErrorControl(
          "Lottie must have either \"src\" or \"src_base64\" specified.");
    }

    var repeat = widget.control.getBool("repeat", true)!;
    var backgroundLoading = widget.control.getBool("background_loading");
    var reverse = widget.control.getBool("reverse", false)!;
    var animate = widget.control.getBool("animate", true)!;
    var fit = widget.control.getBoxFit("fit");
    var alignment = widget.control.getAlignment("alignment");
    var filterQuality = widget.control.getFilterQuality("filter_quality");
    var errorContent = widget.control.buildWidget("error_content");
    var options = LottieOptions(
      enableMergePaths: widget.control.getBool("enable_merge_paths", false)!,
      enableApplyingOpacityToLayers:
          widget.control.getBool("enable_layers_opacity", false)!,
    );
    void onError(String value) {
      if (widget.control.getBool("on_error", false)!) {
        widget.control.triggerEvent("error", value);
      }
    }

    void onLoad(LottieComposition composition) {
      if (widget.control.getBool("on_load", false)!) {
        widget.control.triggerEvent("load");
      }
    }

    Widget errorBuilder(context, error, stackTrace) {
      onError(error.toString());
      return errorContent ??
          ErrorControl("Error loading Lottie", description: error.toString());
    }

    Widget? lottie;

    if (srcBase64 != null) {
      try {
        Uint8List bytes = base64Decode(srcBase64);
        lottie = Lottie.memory(
          bytes,
          repeat: repeat,
          reverse: reverse,
          animate: animate,
          alignment: alignment,
          fit: fit,
          filterQuality: filterQuality,
          options: options,
          backgroundLoading: backgroundLoading,
          errorBuilder: errorBuilder,
          onLoaded: onLoad,
          onWarning: onError,
        );
      } catch (ex) {
        onError(ex.toString());
        return errorContent ??
            ErrorControl("Error decoding src_base64",
                description: ex.toString());
      }
    } else {
      var assetSrc = widget.control.backend.getAssetSource(src!);
      if (assetSrc.isFile) {
        // Local File
        lottie = Lottie.asset(assetSrc.path,
            repeat: repeat,
            reverse: reverse,
            animate: animate,
            alignment: alignment,
            options: options,
            fit: fit,
            filterQuality: filterQuality,
            backgroundLoading: backgroundLoading,
            errorBuilder: errorBuilder,
            onLoaded: onLoad,
            onWarning: onError);
      } else {
        // URL
        lottie = Lottie.network(assetSrc.path,
            repeat: repeat,
            reverse: reverse,
            animate: animate,
            alignment: alignment,
            fit: fit,
            options: options,
            filterQuality: filterQuality,
            backgroundLoading: backgroundLoading,
            headers: widget.control.get("headers")?.cast<String, String>(),
            errorBuilder: errorBuilder,
            onLoaded: onLoad,
            onWarning: onError);
      }
    }

    return ConstrainedControl(control: widget.control, child: lottie);
  }
}
