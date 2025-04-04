import 'package:flutter/foundation.dart';

import 'flet_backend.dart';
import 'models/control.dart';

abstract class FletService {
  Control control;
  FletBackend backend;
  FletService({required this.control, required this.backend});

  @mustCallSuper
  void init() {}

  void update() {}

  @mustCallSuper
  void dispose() {}
}
