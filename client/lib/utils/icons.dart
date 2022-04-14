import 'package:flutter/material.dart';

import 'material_icons.dart';

IconData? getMaterialIcon(String iconName) {
  return materialIcons[iconName.toLowerCase()];
}
