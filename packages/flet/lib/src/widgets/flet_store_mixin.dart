import 'package:flutter/widgets.dart';
import 'package:provider/provider.dart';

import '../flet_backend.dart';
import '../models/page_args_model.dart';
import '../models/page_size_view_model.dart';

mixin FletStoreMixin {
  Widget withPageArgs(Widget Function(BuildContext, PageArgsModel) build) {
    return Selector<FletBackend, PageArgsModel>(
      selector: (_, backend) =>
          PageArgsModel(pageUri: backend.pageUri, assetsDir: backend.assetsDir),
      builder: (context, view, _) => build(context, view),
    );
  }

  Widget withPageSize(Widget Function(BuildContext, PageSizeViewModel) build) {
    return Selector<FletBackend, PageSizeViewModel>(
      selector: (_, backend) => PageSizeViewModel(
          size: backend.pageSize, breakpoints: backend.sizeBreakpoints),
      builder: (context, view, _) => build(context, view),
    );
  }

  Widget withPagePlatform(Widget Function(BuildContext, TargetPlatform) build) {
    return Selector<FletBackend, TargetPlatform>(
      selector: (_, backend) => backend.platform,
      builder: (context, platform, _) => build(context, platform),
    );
  }
}
