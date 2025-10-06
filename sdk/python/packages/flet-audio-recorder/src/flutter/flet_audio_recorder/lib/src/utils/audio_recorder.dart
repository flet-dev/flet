import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:record/record.dart';

AudioEncoder? parseAudioEncoder(String? value, [AudioEncoder? defaultValue]) {
  if (value == null) return defaultValue;
  return AudioEncoder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

InputDevice? parseInputDevice(dynamic value, [InputDevice? defaultValue]) {
  if (value == null) return defaultValue;
  return InputDevice(id: value["id"], label: value["label"]);
}

AndroidAudioSource? parseAndroidAudioSource(String? value,
    [AndroidAudioSource? defaultValue]) {
  if (value == null) return defaultValue;
  return AndroidAudioSource.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

AndroidRecordConfig? parseAndroidRecordConfig(dynamic value,
    [AndroidRecordConfig? defaultValue]) {
  if (value == null) return defaultValue;
  return AndroidRecordConfig(
      audioSource: parseAndroidAudioSource(
          value["audio_source"], AndroidAudioSource.defaultSource)!,
      manageBluetooth: parseBool(value["manage_bluetooth"], true)!,
      muteAudio: parseBool(value["mute_audio"], false)!,
      useLegacy: parseBool(value["use_legacy"], false)!);
}

IosAudioCategoryOption? parseIosAudioCategoryOption(String? value,
    [IosAudioCategoryOption? defaultValue]) {
  if (value == null) return defaultValue;
  return IosAudioCategoryOption.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

IosRecordConfig? parseIosRecordConfig(dynamic value,
    [IosRecordConfig? defaultValue]) {
  if (value == null) return defaultValue;
  var options = (value["options"] as List)
      .map((o) => parseIosAudioCategoryOption(o))
      .nonNulls
      .toList();
  return IosRecordConfig(
    manageAudioSession: parseBool(value["manage_audio_session"], true)!,
    categoryOptions: options,
  );
}

RecordConfig? parseRecordConfig(dynamic value, [RecordConfig? defaultValue]) {
  if (value == null) return defaultValue;
  return RecordConfig(
    autoGain: parseBool(value["auto_gain"], false)!,
    bitRate: parseInt(value["bit_rate"], 128000)!,
    encoder: parseAudioEncoder(value["encoder"], AudioEncoder.wav)!,
    echoCancel: parseBool(value["cancel_echo"], false)!,
    noiseSuppress: parseBool(value["suppress_noise"], false)!,
    numChannels: parseInt(value["channels"], 2)!,
    device: parseInputDevice(value["device"]),
    sampleRate: parseInt(value["sample_rate"], 44100)!,
    androidConfig: parseAndroidRecordConfig(
        value["android_configuration"], const AndroidRecordConfig())!,
    iosConfig: parseIosRecordConfig(
        value["ios_configuration"], const IosRecordConfig())!,
  );
}
