import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
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

  Future<dynamic> _invokeMethod(String name, dynamic args) =>
      invokeSecureStorageMethod(
          storage, control.backend.storagePrefix, name, args);

  @override
  void dispose() {
    debugPrint("SecureStorageService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _onSecureDataChanged?.cancel();
    super.dispose();
  }
}

/// Runs one `SecureStorage` method against [storage], with every key under
/// [prefix] - the app's `FletBackend.storagePrefix`, so an app embedded with
/// `FletApp` has its own space, apart from its host's keys. The app uses plain
/// key names: `get_all` lists its own entries without the prefix, and `clear`
/// removes only those. With an empty [prefix] this is the plain store.
@visibleForTesting
Future<dynamic> invokeSecureStorageMethod(
    FlutterSecureStorage storage, String prefix, String name, dynamic args) async {
  AndroidOptions aOptions = parseAndroidOptions(args?["android"], storage.aOptions)!;
  IOSOptions iOptions = parseIosOptions(args?["ios"], storage.iOptions)!;
  LinuxOptions lOptions = storage.lOptions;
  WindowsOptions wOptions = parseWindowsOptions(args?["windows"], storage.wOptions)!;
  WebOptions webOptions = parseWebOptions(args?["web"], storage.webOptions)!;
  MacOsOptions mOptions = parseMacOptions(args?["macos"], storage.mOptions as MacOsOptions)!;
  String key() => prefix + args["key"]!;
  Future<Map<String, String>> readAll() => storage.readAll(
        aOptions: aOptions,
        iOptions: iOptions,
        lOptions: lOptions,
        wOptions: wOptions,
        webOptions: webOptions,
        mOptions: mOptions,
      );
  Future<void> delete(String k) => storage.delete(
        key: k,
        aOptions: aOptions,
        iOptions: iOptions,
        lOptions: lOptions,
        wOptions: wOptions,
        webOptions: webOptions,
        mOptions: mOptions,
      );
  switch (name) {
    case "set":
      return await storage.write(
        key: key(),
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
        key: key(),
        aOptions: aOptions,
        iOptions: iOptions,
        lOptions: lOptions,
        wOptions: wOptions,
        webOptions: webOptions,
        mOptions: mOptions,
      );
    case "get_all":
      return {
        for (final e in (await readAll()).entries)
          if (e.key.startsWith(prefix)) e.key.substring(prefix.length): e.value,
      };
    case "contains_key":
      return await storage.containsKey(
        key: key(),
        aOptions: aOptions,
        iOptions: iOptions,
        lOptions: lOptions,
        wOptions: wOptions,
        webOptions: webOptions,
        mOptions: mOptions,
      );
    case "remove":
      return await delete(key());
    case "clear":
      if (prefix.isEmpty) {
        return await storage.deleteAll(
          aOptions: aOptions,
          iOptions: iOptions,
          lOptions: lOptions,
          wOptions: wOptions,
          webOptions: webOptions,
          mOptions: mOptions,
        );
      }
      // Only this app's keys - never its host's or another app's.
      final own = (await readAll()).keys.where((k) => k.startsWith(prefix)).toList();
      for (final k in own) {
        await delete(k);
      }
      return null;
    case "get_availability":
      return await storage.isCupertinoProtectedDataAvailable();
    default:
      throw Exception("Unknown SecureStorage method: $name");
  }
}
