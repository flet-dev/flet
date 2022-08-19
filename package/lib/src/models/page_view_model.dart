import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';

class PageViewModel extends Equatable {
  final bool isLoading;
  final String error;
  final Control? page;

  const PageViewModel(
      {required this.isLoading, required this.error, this.page});

  static PageViewModel fromStore(Store<AppState> store) {
    return PageViewModel(
        isLoading: store.state.isLoading,
        error: store.state.error,
        page: store.state.controls["page"]);
  }

  @override
  List<Object?> get props => [isLoading, error, page];
}
