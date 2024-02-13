import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/page_media_view_model.dart';
import '../protocol/page_media_data.dart';
import '../utils/debouncer.dart';
import '../utils/desktop.dart';

class PageMedia extends StatefulWidget {
  const PageMedia({super.key});

  @override
  State<PageMedia> createState() => _PageMediaState();
}

class _PageMediaState extends State<PageMedia> {
  final _debouncer = Debouncer(milliseconds: 250);
  int _pageMediaTimestamp = 0;

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  _onScreenSizeChanged(bool isRegistered, Size newSize, Function dispatch) {
    if (isRegistered) {
      _debouncer.run(() {
        debugPrint("Send current size to reducer: $newSize");
        getWindowMediaData().then((wmd) {
          dispatch(PageSizeChangeAction(
              newSize, wmd, FletAppServices.of(context).server));
        });
      });
    } else {
      dispatch(PageSizeChangeAction(
          newSize, null, FletAppServices.of(context).server));
    }
  }

  _onScreenBrightnessChanged(Brightness brightness, Function dispatch) {
    debugPrint("Send new brightness to reducer: $brightness");
    dispatch(PageBrightnessChangeAction(
        brightness, FletAppServices.of(context).server));
  }

  _onMediaChanged(PageMediaData media, Function dispatch) {
    var now = DateTime.now().millisecondsSinceEpoch;
    if (now - _pageMediaTimestamp > 50) {
      _pageMediaTimestamp = now;
      debugPrint("Send new page media data to reducer: $media");
      dispatch(
          PageMediaChangeAction(media, FletAppServices.of(context).server));
    }
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

          var newMdeia = PageMediaData(
              padding: PaddingData(media.padding),
              viewPadding: PaddingData(media.viewPadding),
              viewInsets: PaddingData(media.viewInsets));

          if (newMdeia != viewModel.media) {
            _onMediaChanged(newMdeia, viewModel.dispatch);
          } else {
            debugPrint("Page media data did not change.");
          }
          return const SizedBox.shrink();
        });
  }
}
