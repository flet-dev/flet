import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'utils/theme.dart';

class ShadAvatarControl extends StatelessWidget {
  final Control control;

  const ShadAvatarControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ShadAvatar build: ${control.id}");

    final size = control.getDouble("size");
    final placeholder = control.buildTextOrWidget("placeholder");
    final src = control.getString("src");

    // The image is built with Flet's own loader, so `src` is resolved like
    // `ft.Image.src` (URL, asset path or file), with `placeholder` shown if it
    // fails. ShadAvatar's own loader would treat Flet asset paths as bundle
    // assets.
    return LayoutControl(
      control: control,
      child: withShadTheme(
        context,
        ShadAvatar(
          null,
          size: size != null ? Size.square(size) : null,
          backgroundColor: control.getColor("bgcolor", context),
          placeholder: src != null
              ? buildImage(
                  context: context,
                  src: src,
                  errorCtrl: placeholder,
                  width: size ?? 40,
                  height: size ?? 40,
                  fit: BoxFit.cover,
                )
              : placeholder,
        ),
      ),
    );
  }
}
