import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:sensors_plus/sensors_plus.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';

class ShakeDetectorService extends FletService {
  ShakeDetectorService({required super.control, required super.backend});

  StreamSubscription<AccelerometerEvent>? _subscription;

  int _mShakeTimestamp = DateTime.now().millisecondsSinceEpoch;
  int _mShakeCount = 0;

  int _minimumShakeCount = 1;
  int _shakeSlopTimeMs = 500;
  int _shakeCountResetTimeMs = 3000;
  double _shakeThresholdGravity = 2.7;

  @override
  void init() {
    debugPrint("ShakeDetectorService(${control.id}).init()");
    super.init();
    update();
  }

  @override
  void update() {
    debugPrint(
        "ShakeDetectorService(${control.id}).update: ${control.properties}");

    var minimumShakeCount = control.getInt("minimum_shake_count", 1)!;
    var shakeSlopTimeMs = control.getInt("shake_slop_time_ms", 500)!;
    var shakeCountResetTimeMs =
        control.getInt("shake_count_reset_time_ms", 3000)!;
    var shakeThresholdGravity =
        control.getDouble("shake_threshold_gravity", 2.7)!;

    // Update config if changed
    if (minimumShakeCount != _minimumShakeCount ||
        shakeSlopTimeMs != _shakeSlopTimeMs ||
        shakeCountResetTimeMs != _shakeCountResetTimeMs ||
        shakeThresholdGravity != _shakeThresholdGravity) {
      _minimumShakeCount = minimumShakeCount;
      _shakeSlopTimeMs = shakeSlopTimeMs;
      _shakeCountResetTimeMs = shakeCountResetTimeMs;
      _shakeThresholdGravity = shakeThresholdGravity;

      _stopListening();
      _startListening();
    }
  }

  void _startListening() {
    _subscription = accelerometerEventStream().listen((event) {
      final gX = event.x / 9.80665;
      final gY = event.y / 9.80665;
      final gZ = event.z / 9.80665;

      final gForce = sqrt(gX * gX + gY * gY + gZ * gZ);

      if (gForce > _shakeThresholdGravity) {
        final now = DateTime.now().millisecondsSinceEpoch;

        if (_mShakeTimestamp + _shakeSlopTimeMs > now) {
          return;
        }

        if (_mShakeTimestamp + _shakeCountResetTimeMs < now) {
          _mShakeCount = 0;
        }

        _mShakeTimestamp = now;
        _mShakeCount++;

        if (_mShakeCount >= _minimumShakeCount) {
          backend.triggerControlEvent(control, "shake");
        }
      }
    });
  }

  void _stopListening() {
    _subscription?.cancel();
    _subscription = null;
  }

  @override
  void dispose() {
    debugPrint("ShakeDetectorService(${control.id}).dispose()");
    _stopListening();
    super.dispose();
  }
}

/*
Source: https://github.com/dieringe/shake/blob/master/lib/shake.dart

Copyright 2019 Deven Joshi

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
*/
