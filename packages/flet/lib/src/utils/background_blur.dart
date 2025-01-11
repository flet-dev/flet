
import 'package:flutter/material.dart';
import 'package:flutter_acrylic/flutter_acrylic.dart';

bool _isInitialized = false;

Future<void> initializeWindow() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (!_isInitialized) {
    await Window.initialize();
    _isInitialized = true;
  }
}

Future<void> setWindowEffect(String effectName) async {
  if (!_isInitialized) {
    await initializeWindow();
  }

  WindowEffect effect;

  switch (effectName.toLowerCase()) {
    case 'mica':
      effect = WindowEffect.mica;
      break;
    case 'acrylic':
      effect = WindowEffect.acrylic;
      break;
    case 'transparent':
      effect = WindowEffect.transparent;
      break;
    case 'disabled':
      effect = WindowEffect.disabled;
      break;
    case 'tabbed':
      effect = WindowEffect.tabbed;
      break;
    default:
      effect = WindowEffect.disabled;
      break;
  }
//Color.fromARGB(0, 255, 255, 255),
  await Window.setEffect(
    effect: effect,
    color: Colors.transparent,
    dark: true
  );
}
