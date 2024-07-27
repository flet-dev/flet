import 'package:markdown/markdown.dart' as md;

md.ExtensionSet? parseMarkdownExtensionSet(String? value,
    [md.ExtensionSet? defValue]) {
  if (value == null) {
    return defValue;
  }
  switch (value.toLowerCase()) {
    case "commonmark":
      return md.ExtensionSet.commonMark;
    case "githubweb":
      return md.ExtensionSet.gitHubWeb;
    case "githubflavored":
      return md.ExtensionSet.gitHubFlavored;
    default:
      return defValue ?? md.ExtensionSet.none;
  }
}
