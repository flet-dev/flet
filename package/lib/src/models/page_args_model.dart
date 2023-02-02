import 'package:equatable/equatable.dart';
import 'package:redux/redux.dart';

import 'app_state.dart';
import 'control.dart';
import 'control_view_model.dart';

class PageArgsModel extends Equatable {
  final Uri? pageUri;
  final String assetsDir;
  final Map<String, Function(Control?, ControlViewModel)>? controlsMapping;

  const PageArgsModel(
      {required this.pageUri, required this.assetsDir, this.controlsMapping});

  static PageArgsModel fromStore(Store<AppState> store) {
    return PageArgsModel(
        pageUri: store.state.pageUri,
        assetsDir: store.state.assetsDir,
        controlsMapping: store.state.controlsMapping);
  }

  @override
  List<Object?> get props => [pageUri, assetsDir, controlsMapping];
}
