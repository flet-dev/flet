import 'dart:async';

import '../flet_app_services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';
import '../models/page_media_view_model.dart';
import '../utils/desktop.dart';

class PageMedia extends StatefulWidget {
  const PageMedia({Key? key}) : super(key: key);

  @override
  State<PageMedia> createState() => _PageMediaState();
}

class _PageMediaState extends State<PageMedia> {
  Timer? _debounce;

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  _onScreenSizeChanged(bool isRegistered, Size newSize, Function dispatch) {
    if (isRegistered) {
      if (_debounce?.isActive ?? false) _debounce!.cancel();
      _debounce = Timer(const Duration(milliseconds: 300), () {
        debugPrint("Send current size to reducer: $newSize");
        getWindowMediaData().then((wmd) {
          dispatch(PageSizeChangeAction(
              newSize, wmd, FletAppServices.of(context).ws));
        });
      });
    } else {
      dispatch(
          PageSizeChangeAction(newSize, null, FletAppServices.of(context).ws));
    }
  }

  _onScreenBrightnessChanged(Brightness brightness, Function dispatch) {
    debugPrint("Send new brightness to reducer: $brightness");
    dispatch(PageBrightnessChangeAction(brightness));
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Page media build");

    return StoreConnector<AppState, PageMediaViewModel>(
        distinct: true,
        converter: (store) => PageMediaViewModel.fromStore(store),
        builder: (context, viewModel) {
          MediaQueryData media = MediaQuery.of(context);
          if (media.size != viewModel.size) {
            _onScreenSizeChanged(
                viewModel.isRegistered, media.size, viewModel.dispatch);
          } else {
            debugPrint("Page size did not change.");
          }
          if (media.platformBrightness != viewModel.displayBrightness) {
            _onScreenBrightnessChanged(
                media.platformBrightness, viewModel.dispatch);
          } else {
            debugPrint("Page brightness did not change.");
          }
          return const SizedBox.shrink();
        });
  }
}
