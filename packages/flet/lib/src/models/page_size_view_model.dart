import 'dart:ui';

import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';

class PageSizeViewModel extends Equatable {
  final Map<String, double> breakpoints;
  final Size size;

  const PageSizeViewModel({required this.size, required this.breakpoints});

  static PageSizeViewModel fromStore(Store<AppState> store) {
    return PageSizeViewModel(
        size: store.state.size, breakpoints: store.state.sizeBreakpoints);
  }

  @override
  List<Object?> get props => [size, breakpoints];
}
