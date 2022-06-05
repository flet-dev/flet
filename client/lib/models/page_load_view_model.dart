import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'page_media_view_model.dart';

class PageLoadViewModel extends Equatable {
  final Uri? pageUri;
  final String sessionId;
  final PageMediaViewModel sizeViewModel;

  const PageLoadViewModel(
      {required this.pageUri,
      required this.sessionId,
      required this.sizeViewModel});

  static PageLoadViewModel fromStore(Store<AppState> store) {
    return PageLoadViewModel(
        pageUri: store.state.pageUri,
        sessionId: store.state.sessionId,
        sizeViewModel: PageMediaViewModel.fromStore(store));
  }

  @override
  List<Object?> get props => [pageUri, sizeViewModel];
}
