import 'package:record/record.dart';

AudioEncoder? parseAudioEncoder(String? encoding) {
  switch (encoding?.toLowerCase()) {
    case "aaclc":
      return AudioEncoder.aacLc;
    case "aaceld":
      return AudioEncoder.aacEld;
    case "aache":
      return AudioEncoder.aacHe;
    case "amrnb":
      return AudioEncoder.amrNb;
    case "amrwb":
      return AudioEncoder.amrWb;
    case "opus":
      return AudioEncoder.opus;
    case "flac":
      return AudioEncoder.flac;
    case "wav":
      return AudioEncoder.wav;
    case "pcm16bits":
      return AudioEncoder.pcm16bits;
    default:
      return null;
  }
}
