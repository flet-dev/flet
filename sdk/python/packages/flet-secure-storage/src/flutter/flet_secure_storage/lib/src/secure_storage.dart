import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'utils/secure_storage.dart';

class SecureStorageService extends FletService {
  SecureStorageService({required super.control});

  FlutterSecureStorage? _storage;
  StreamSubscription? _onSecureDataChanged;
  AndroidOptions androidOptions = AndroidOptions.defaultOptions;
  WindowsOptions windowsOptions = WindowsOptions.defaultOptions;
  LinuxOptions linuxOptions = LinuxOptions.defaultOptions;
  MacOsOptions macOsOptions = MacOsOptions.defaultOptions;
  IOSOptions iosOptions = IOSOptions.defaultOptions;
  WebOptions webOptions = WebOptions.defaultOptions;

  FlutterSecureStorage get storage {
    return _storage ??= FlutterSecureStorage(
      lOptions: linuxOptions,
      aOptions: parseAndroidOptions(control.get<Map>("android_options"), androidOptions)!,
      wOptions: parseWindowsOptions(control.get<Map>("windows_options"), windowsOptions)!,
      mOptions: parseMacOptions(control.get<Map>("macos_options"), macOsOptions)!,
      iOptions: parseIosOptions(control.get<Map>("ios_options"), iosOptions)!,
      webOptions: parseWebOptions(control.get<Map>("web_options"), webOptions)!,
    );
  }

  @override
  void init() {
    super.init();
    debugPrint("SecureStorageService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
    _updateListeners();
  }

  @override
  void update() {
    debugPrint("SecureStorageService(${control.id}).update: ${control.properties}");
    _updateListeners();
  }

  void _updateListeners() {
    final listenChange = control.getBool("on_change") == true;
    if (listenChange && _onSecureDataChanged == null) {
      _onSecureDataChanged = storage.onCupertinoProtectedDataAvailabilityChanged?.listen(
        (bool result) {
          control.triggerEvent("change", {"available": result});
        }, onError: (error) {
            debugPrint("SecureStorageService: error listening to connectivity: $error");
        }
      );
    } else if (!listenChange && _onSecureDataChanged != null) {
      _onSecureDataChanged?.cancel();
      _onSecureDataChanged = null;
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    AndroidOptions aOptions = parseAndroidOptions(args?["android"], storage.aOptions)!;
    IOSOptions iOptions = parseIosOptions(args?["ios"], storage.iOptions)!;
    LinuxOptions lOptions = storage.lOptions;
    WindowsOptions wOptions = parseWindowsOptions(args?["windows"], storage.wOptions)!;
    WebOptions webOptions = parseWebOptions(args?["web"], storage.webOptions)!;
    MacOsOptions mOptions = parseMacOptions(args?["macos"], storage.mOptions as MacOsOptions)!;
    switch (name) {
      case "set":
        return await storage.write(
          key: args["key"]!,
          value: args["value"]!,
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "get":
        return await storage.read(
          key: args["key"]!,
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "get_all":
        return await storage.readAll(
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "contains_key":
        return await storage.containsKey(
          key: args["key"]!,
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "remove":
        return await storage.delete(
          key: args["key"]!,
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "clear":
        return await storage.deleteAll(
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      case "get_availability":
        return await storage.isCupertinoProtectedDataAvailable();
      default:
        throw Exception("Unknown SecureStorage method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("SecureStorageService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _onSecureDataChanged?.cancel();
    super.dispose();
  }
}
