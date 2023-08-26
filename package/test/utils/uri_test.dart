import 'package:flet/src/utils/uri.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test("Empty URI can be parsed", () {
    var uri = Uri.parse("");
    expect(uri.hasAuthority, false);
  });
  test("Relative URI can be parsed", () {
    var uri = Uri.parse("images/test.png");
    expect(uri.hasAuthority, false);
  });

  test("getWebPageName returns correct name from Uri", () {
    expect(
        getWebPageName(Uri.parse('http://localhost:8550/p/test/')), "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/p/test')), "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/aaa')), "aaa");
    expect(getWebPageName(Uri.parse('http://localhost:8550/p/test/store')),
        "p/test");
    expect(
        getWebPageName(
            Uri.parse('http://localhost:8550/p/test/store/products/1')),
        "p/test");
    expect(getWebPageName(Uri.parse('http://localhost:8550/')), "");
    expect(getWebPageName(Uri.parse('http://localhost:8550/#/')), "");
  });
}
