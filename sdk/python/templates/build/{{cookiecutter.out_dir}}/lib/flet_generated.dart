// GENERATED FILE — do not edit.
//
// All build-time (cookiecutter / jinja) declarations live here so that
// `main.dart` stays plain, editable Dart with no template noise.

import 'dart:convert';

import 'package:flet/flet.dart';

{% for dep in cookiecutter.flutter.dependencies %}
import 'package:{{ dep }}/{{ dep }}.dart' as {{ dep }};
{% endfor %}

{% set hide_window_on_start = get_pyproject("tool.flet." ~ cookiecutter.options.config_platform ~ ".app.hide_window_on_start")
                        or get_pyproject("tool.flet.app.hide_window_on_start") %}

const pythonModuleName = "{{ cookiecutter.python_module_name }}";

final hideWindowOnStart =
    bool.tryParse("{{ hide_window_on_start }}".toLowerCase()) ?? false;

const bootScreenName = "{{ cookiecutter.boot_screen.name }}";

final bootScreenOptions = (jsonDecode(utf8
        .decode(base64Decode("{{ cookiecutter.boot_screen.options_b64 }}")))
    as Map)
    .cast<String, dynamic>();

List<FletExtension> extensions = [
{% for dep in cookiecutter.flutter.dependencies %}
  {{ dep }}.Extension(),
{% endfor %}
];
