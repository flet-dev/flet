import 'dart:async';

import 'package:flet_view/models/page_media_view_model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';

class PageMedia extends StatefulWidget {
  const PageMedia({Key? key}) : super(key: key);

  @override
  State<PageMedia> createState() => _PageMediaState();
}

class _PageMediaState extends State<PageMedia> {
  Timer? _debounce;

  _onScreenSizeChanged(Size newSize, Function dispatch) {
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () {
      debugPrint("Send current size to reducer: $newSize");
      dispatch(PageSizeChangeAction(newSize));
    });
  }

  _onScreenBrightnessChanged(Brightness brightness, Function dispatch) {
    debugPrint("Send new brightness to reducer: $brightness");
    dispatch(PageBrightnessChangeAction(brightness));
  }

  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, PageMediaViewModel>(
        distinct: true,
        converter: (store) => PageMediaViewModel.fromStore(store),
        builder: (context, viewModel) {
          MediaQueryData media = MediaQuery.of(context);
          if (media.size != viewModel.size) {
            _onScreenSizeChanged(media.size, viewModel.dispatch);
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

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }
}
