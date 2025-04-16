import 'package:flutter/foundation.dart';

import 'models/control.dart';

abstract class FletService {
  Control control;

  FletService({required this.control});

  @mustCallSuper
  void init() {}

  void update() {}

  @mustCallSuper
  void dispose() {}
}
