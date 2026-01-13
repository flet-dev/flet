import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

FlutterSecureStorage createSecureStorage(dynamic value) {
  return FlutterSecureStorage(
    aOptions: parseAndroidOptions(value["android"], AndroidOptions.defaultOptions)!,
    iOptions: parseIosOptions(value["ios"], IOSOptions.defaultOptions)!,
    lOptions: LinuxOptions.defaultOptions,
    wOptions: parseWindowsOptions(value["windows"], WindowsOptions.defaultOptions)!,
    webOptions: parseWebOptions(value["web"], WebOptions.defaultOptions)!,
    mOptions: parseMacOptions(value["macos"], MacOsOptions.defaultOptions)!,
  );
}

IOSOptions? parseIosOptions(dynamic value, [IOSOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return IOSOptions(
    accountName: value["account_name"],
    groupId: value["group_id"],
    accessibility: parseKeychainAccessibility(value["accessibility"], KeychainAccessibility.unlocked),
    synchronizable: parseBool(value["synchronizable"], false)!,
    label: value["label"],
    description: value["description"],
    comment: value["comment"],
    isInvisible: parseBool(value["is_invisible"]),
    isNegative: parseBool(value["is_negative"]),
    creationDate: parseDateTime(value["creation_date"]),
    lastModifiedDate: parseDateTime(value["last_modified_date"]),
    resultLimit: parseInt(value["result_limit"]),
    shouldReturnPersistentReference: parseBool(value["is_persistent"], false)!,
    authenticationUIBehavior: value["auth_ui_behavior"],
    accessControlFlags: parseAccessControlFlags(value["access_control_flags"], const [])!,
  );
}

MacOsOptions? parseMacOptions(dynamic value, [MacOsOptions? defaultValue]) {
  if (value == null) return defaultValue; 
  return MacOsOptions(
    accountName: value["account_name"],
    groupId: value["group_id"],
    accessibility: parseKeychainAccessibility(value["accessibility"], KeychainAccessibility.unlocked),
    synchronizable: parseBool(value["synchronizable"], false)!,
    label: value["label"],
    description: value["description"],
    comment: value["comment"],
    isInvisible: parseBool(value["is_invisible"]),
    isNegative: parseBool(value["is_negative"]),
    creationDate: parseDateTime(value["creation_date"]),
    lastModifiedDate: parseDateTime(value["last_modified_date"]),
    resultLimit: parseInt(value["result_limit"]),
    shouldReturnPersistentReference: parseBool(value["is_persistent"]),
    authenticationUIBehavior: value["auth_ui_behavior"],
    accessControlFlags: parseAccessControlFlags(value["access_control_flags"], const [])!,
    usesDataProtectionKeychain: parseBool(value["uses_data_protection_keychain"], true)!
  );
}

AndroidOptions? parseAndroidOptions(dynamic value, [AndroidOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return AndroidOptions(
    resetOnError: parseBool(value['reset_on_error'], true)!,
    migrateOnAlgorithmChange: parseBool(value['migrate_on_algorithm_change'], true)!,
    enforceBiometrics: parseBool(value['enforce_biometrics'], true)!,
    keyCipherAlgorithm: parseKeyCipherAlgorithm(
      value['key_cipher_algorithm'],
      KeyCipherAlgorithm.RSA_ECB_OAEPwithSHA_256andMGF1Padding
    )!,
    storageCipherAlgorithm: parseStorageCipherAlgorithm(
      value['storage_cipher_algorithm'],
      StorageCipherAlgorithm.AES_GCM_NoPadding
    )!,
    sharedPreferencesName: value['shared_preferences_name'],
    preferencesKeyPrefix: value['preferences_key_prefix'],
    biometricPromptTitle: value['biometric_prompt_title'],
    biometricPromptSubtitle: value['biometric_prompt_subtitle'],
  );
}

WindowsOptions? parseWindowsOptions(dynamic value, [WindowsOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return WindowsOptions(
    useBackwardCompatibility: parseBool(value["use_backward_compatibility"], false)!,
  );
}

WebOptions? parseWebOptions(dynamic value, [WebOptions? defaultValue]) {
  if (value == null) return defaultValue;
  return WebOptions(
    dbName: value["db_name"] ?? "FlutterEncryptedStorage",
    publicKey: value["public_key"] ?? "FlutterSecureStorage",
    wrapKey: value["wrap_key"] ?? "",
    wrapKeyIv: value["wrap_key_iv"] ?? "",
    useSessionStorage: parseBool(value["use_session_storage"], false)!,
  );
}

KeychainAccessibility? parseKeychainAccessibility(String? value, [KeychainAccessibility? defaultValue]) {
  if (value == null) return defaultValue;
  return KeychainAccessibility.values.firstWhereOrNull(
    (e) => e.name.toLowerCase() == value.toLowerCase()
  ) ?? defaultValue;
}

KeyCipherAlgorithm? parseKeyCipherAlgorithm(String? value, [KeyCipherAlgorithm? defaultValue]) {
  if (value == null) return defaultValue;
  return KeyCipherAlgorithm.values.firstWhereOrNull(
    (e) => e.name.toLowerCase() == value.toLowerCase()
  ) ?? defaultValue;
}

StorageCipherAlgorithm? parseStorageCipherAlgorithm(String? value, [StorageCipherAlgorithm? defaultValue]) {
  if (value == null) return defaultValue;
  return StorageCipherAlgorithm.values.firstWhereOrNull(
    (e) => e.name.toLowerCase() == value.toLowerCase()
  ) ?? defaultValue;
}

List<AccessControlFlag>? parseAccessControlFlags(List<dynamic>? value, [List<AccessControlFlag>? defaultValue]) {
  if (value == null) return defaultValue;
  return value
      .cast<String>()
      .map((e) => AccessControlFlag.values.byName(e))
      .toList();
}

DateTime? parseDateTime(dynamic value, [DateTime? defaultValue]) {
  if (value == null) return defaultValue;
  return DateTime.parse(value);
}