import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';

class PageSizeViewModel extends Equatable {
  final Size size;
  final Function dispatch;

  const PageSizeViewModel({required this.size, required this.dispatch});

  static PageSizeViewModel fromStore(Store<AppState> store) {
    return PageSizeViewModel(size: store.state.size, dispatch: store.dispatch);
  }

  @override
  List<Object?> get props => [size, dispatch];
}
