import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import 'controls/create_control.dart';
import 'flet_app_services.dart';
import 'models/app_state.dart';

class FletAppMain extends StatelessWidget {
  final String title;

  const FletAppMain({
    super.key,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      store: FletAppServices.of(context).store,
      child: createControl(null, "page", false),
    );
  }
}
