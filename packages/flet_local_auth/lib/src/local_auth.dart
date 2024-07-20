import 'dart:developer';
import 'dart:io' show Platform;
import 'dart:io';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:local_auth/local_auth.dart';

class LocalAuthenticationControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const LocalAuthenticationControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<LocalAuthenticationControl> createState() =>
      _LocalAuthenticationControlState();
}

class _LocalAuthenticationControlState
    extends State<LocalAuthenticationControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("LocalAuthentication build: ${widget.control.id}");

    if (Platform.isIOS || Platform.isAndroid || Platform.isWindows) {
      () async {
        final LocalAuthentication auth = LocalAuthentication();

        widget.backend.subscribeMethods(widget.control.id,
            (methodName, args) async {
          switch (methodName) {
            case "supported":
              try {
                // get's available biometrics
                final List<BiometricType> availableBiometrics =
                    await auth.getAvailableBiometrics();
                // check's if device is supported
                final bool canAuthenticate = await auth.isDeviceSupported();
                // creates a map of retrieved data to convert into string
                final Map output = {
                  "biometrics": availableBiometrics.isNotEmpty,
                  "weak": availableBiometrics.contains(BiometricType.weak),
                  "strong": availableBiometrics.contains(BiometricType.strong),
                  "devicesupport": canAuthenticate,
                };
                debugPrint("$output");
                return "$output";
              } on Exception catch (_) {
                debugPrint("An error has occured: $_");
                return "0";
              }
            case "authenticate":
              try {
                final bool didAuthenticate = await auth.authenticate(
                  // if no title is given, uses "Authentication required" as the title
                  localizedReason: args['title'] ?? "Authentication required",
                  options: AuthenticationOptions(
                    biometricOnly:
                        args['biometricsOnly'] == 'true' ? true : false,
                    useErrorDialogs:
                        args['useErrorDialogs'] == 'true' ? true : false,
                  ),
                );
                return "$didAuthenticate";
              } on Exception catch (_) {
                debugPrint("An error has occured: $_");
                return "0";
              }
          }
          return null;
        });
      }();

      return const SizedBox.shrink();
    } else {
      return const ErrorControl(
          "LocalAuthentication Control is not supported on this platform yet.");
    }
  }
}
