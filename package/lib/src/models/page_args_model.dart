import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';

class PageArgsModel extends Equatable {
  final Uri? pageUri;
  final String assetsDir;

  const PageArgsModel({required this.pageUri, required this.assetsDir});

  static PageArgsModel fromStore(Store<AppState> store) {
    return PageArgsModel(
        pageUri: store.state.pageUri, assetsDir: store.state.assetsDir);
  }

  @override
  List<Object?> get props => [pageUri, assetsDir];
}
