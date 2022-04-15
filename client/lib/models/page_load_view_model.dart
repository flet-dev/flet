import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'package:flet_view/models/page_size_view_model.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';

class PageLoadViewModel extends Equatable {
  final Uri? pageUri;
  final String sessionId;
  final PageSizeViewModel sizeViewModel;

  const PageLoadViewModel(
      {required this.pageUri,
      required this.sessionId,
      required this.sizeViewModel});

  static PageLoadViewModel fromStore(Store<AppState> store) {
    return PageLoadViewModel(
        pageUri: store.state.pageUri,
        sessionId: store.state.sessionId,
        sizeViewModel: PageSizeViewModel.fromStore(store));
  }

  @override
  List<Object?> get props => [pageUri, sizeViewModel];
}
