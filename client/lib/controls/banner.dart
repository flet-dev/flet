import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class BannerControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const BannerControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<BannerControl> createState() => _BannerControlState();
}

class _BannerControlState extends State<BannerControl> {
  bool _open = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  Widget _createBanner() {
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    var leadingCtrls =
        widget.children.where((c) => c.name == "leading" && c.isVisible);
    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    var actionCtrls =
        widget.children.where((c) => c.name == "action" && c.isVisible);

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Banner does not have any content.");
    } else if (actionCtrls.isEmpty) {
      return const ErrorControl("Banner should have at least one action.");
    }

    return MaterialBanner(
      leading: leadingCtrls.isNotEmpty
          ? createControl(widget.control, leadingCtrls.first.id, disabled)
          : null,
      leadingPadding: parseEdgeInsets(widget.control, "leadingPadding"),
      content: createControl(widget.control, contentCtrls.first.id, disabled),
      padding: parseEdgeInsets(widget.control, "contentPadding"),
      actions: actionCtrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
      forceActionsBelow: widget.control.attrBool("forceActionsBelow", false)!,
      backgroundColor: HexColor.fromString(
          Theme.of(context), widget.control.attrString("bgcolor", "")!),
    );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Banner build: ${widget.control.id}");

    return StoreConnector<AppState, Function>(
        distinct: true,
        converter: (store) => store.dispatch,
        builder: (context, dispatch) {
          debugPrint("Banner StoreConnector build: ${widget.control.id}");

          var open = widget.control.attrBool("open", false)!;

          debugPrint("Current open state: $_open");
          debugPrint("New open state: $open");

          if (open && (open != _open)) {
            var banner = _createBanner();
            if (banner is ErrorControl) {
              return banner;
            }

            WidgetsBinding.instance.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).removeCurrentMaterialBanner();

              ScaffoldMessenger.of(context)
                  .showMaterialBanner(banner as MaterialBanner);
            });
          } else if (open != _open && _open) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              ScaffoldMessenger.of(context).removeCurrentMaterialBanner();
            });
          }

          _open = open;

          return const SizedBox.shrink();
        });
  }
}
