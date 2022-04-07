import 'dart:async';

import 'package:flet_view/models/page_size_view_model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../actions.dart';
import '../models/app_state.dart';

class ScreenSize extends StatefulWidget {
  const ScreenSize({Key? key}) : super(key: key);

  @override
  State<ScreenSize> createState() => _ScreenSizeState();
}

class _ScreenSizeState extends State<ScreenSize> {
  Timer? _debounce;

  _onScreenSizeChanged(Size newSize, Function dispatch) {
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () {
      debugPrint("Send current size to reducer: $newSize");
      dispatch(PageSizeChangeAction(newSize));
    });
  }

  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, PageSizeViewModel>(
        distinct: true,
        converter: (store) => PageSizeViewModel.fromStore(store),
        builder: (context, viewModel) {
          MediaQueryData media = MediaQuery.of(context);
          if (media.size != viewModel.size) {
            _onScreenSizeChanged(media.size, viewModel.dispatch);
          } else {
            debugPrint("Page size did not change.");
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
