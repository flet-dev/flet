import 'package:flutter/foundation.dart';

import 'flet_backend.dart';
import 'models/control.dart';

abstract class FletService {
  Control control;
  FletBackend backend;
  FletService(this.control, this.backend);

  @mustCallSuper
  void init() {}

  void update() {}

  @mustCallSuper
  void dispose() {}
}
