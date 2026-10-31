import contextlib
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from jinja2 import Environment, StrictUndefined

from flet_cli.commands.build_base import BaseBuildCommand
from flet_cli.utils.project_dependencies import get_project_dependencies

ANDROID_NS = "http://schemas.android.com/apk/res/android"
ANDROID_APP_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "templates/build/{{cookiecutter.out_dir}}/android/app"
)


def _command(settings):
    """Create a build command whose configuration errors raise ValueError."""
    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.get_pyproject = settings.get
    cmd.extensions = []

    def cleanup(code, message):
        """Capture a failed build setting without exiting the test process."""
        assert code == 1
        raise ValueError(message)

    cmd.cleanup = cleanup
    return cmd


def _render_gradle(cmd):
    """Render the Android Gradle template using resolved command settings."""
    env = Environment(undefined=StrictUndefined)
    env.globals["get_pyproject"] = lambda key: None
    return env.from_string(
        (ANDROID_APP_TEMPLATE / "build.gradle.kts").read_text()
    ).render(
        cookiecutter={
            "org_name_2": "com.example",
            "package_name": "example",
            "split_per_abi": False,
            "_options": {
                "android_compile_options": cmd.get_android_compile_options(),
                "android_gradle_dependencies": cmd.get_android_gradle_dependencies(),
                "android_legacy_packaging": False,
                "android_excluded_abis": [],
                "android_signing": False,
                "target_arch": [],
            },
        }
    )


def _render_manifest(cmd):
    """Parse a rendered manifest containing queries, receivers, and existing app
    entries."""
    path = ANDROID_APP_TEMPLATE / "src/main/AndroidManifest.xml"
    rendered = (
        Environment(undefined=StrictUndefined)
        .from_string(path.read_text())
        .render(
            cookiecutter={
                "product_name": "Example",
                "_pyproject": {},
                "_options": {
                    "android_application_attributes": (
                        cmd.get_android_application_attributes("Example")
                    ),
                    "android_activity": cmd.get_android_activity(),
                    "android_queries": cmd.get_android_queries(),
                    "android_receivers": cmd.get_android_receivers(),
                    "android_services": cmd.get_android_services(),
                    "android_permissions": {"android.permission.INTERNET": True},
                    "android_features": {},
                    "android_meta_data": {},
                    "android_providers": {
                        "com.example.Provider": {"exported": "false"}
                    },
                    "deep_linking": {"scheme": None, "host": None},
                },
            }
        )
    )
    return ET.fromstring(rendered)


class TestCompileOptions:
    """Cover compiler defaults, per-property overrides, and Kotlin expressions."""

    @staticmethod
    def _resolve(configured):
        """Resolve a compile-options table through the build command."""
        return _command(
            {"tool.flet.android.compile_options": configured}
        ).get_android_compile_options()

    @pytest.mark.parametrize("configured", [None, {}])
    def test_defaults_preserve_java_17(self, configured):
        """An omitted or empty table retains both Java compatibility defaults."""
        assert self._resolve(configured) == {
            "sourceCompatibility": "JavaVersion.VERSION_17",
            "targetCompatibility": "JavaVersion.VERSION_17",
        }

    def test_overrides_merge_without_changing_user_configuration(self):
        """Overrides leave the input table and defaults for later builds unchanged."""
        configured = {
            "targetCompatibility": "JavaVersion.VERSION_21",
            "isCoreLibraryDesugaringEnabled": "false",
            "encoding": '"UTF-8"',
        }
        assert self._resolve(configured) == {
            "sourceCompatibility": "JavaVersion.VERSION_17",
            **configured,
        }
        assert "sourceCompatibility" not in configured
        assert self._resolve(None)["targetCompatibility"] == "JavaVersion.VERSION_17"

    @pytest.mark.parametrize("configured", [[], ["encoding = true"], False, "", 17])
    def test_invalid_table_reports_setting(self, configured):
        """Reject non-table settings with the offending configuration path."""
        with pytest.raises(
            ValueError, match=r"tool\.flet\.android\.compile_options.*table"
        ):
            self._resolve(configured)

    @pytest.mark.parametrize("name", ["", "has space", "a.b", "x;", "x\n", "1value"])
    def test_invalid_property_name_reports_setting(self, name):
        """Reject keys that cannot be rendered as Kotlin property identifiers."""
        with pytest.raises(ValueError, match="property identifier"):
            self._resolve({name: "true"})

    @pytest.mark.parametrize("expression", [True, False, 17, [], {}, "", " \n "])
    def test_invalid_expression_reports_property(self, expression):
        """Require nonempty expression strings and identify the invalid property."""
        with pytest.raises(
            ValueError, match=r"compile_options\.encoding.*expression string"
        ):
            self._resolve({"encoding": expression})

    @pytest.mark.parametrize("enabled", [None, "true", "false"])
    def test_rendered_compile_options_preserve_kotlin_expressions(self, enabled):
        """Render actual template assignments once, with no extra quoting."""
        configured = {
            "sourceCompatibility": "JavaVersion.VERSION_17",
            "encoding": '"UTF-8"',
        }
        if enabled is not None:
            configured["isCoreLibraryDesugaringEnabled"] = enabled
        options = self._resolve(configured)
        rendered = _render_gradle(
            _command({"tool.flet.android.compile_options": configured})
        )
        for name, expression in options.items():
            assert rendered.count(f"{name} = {expression}") == 1
        assert (
            "isCoreLibraryDesugaringEnabled" in rendered
            if enabled
            else ("isCoreLibraryDesugaringEnabled" not in rendered)
        )
        assert (
            "jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17" in rendered
        )


class TestGradleDependencies:
    """Cover literal Kotlin dependency blocks and Python dependency separation."""

    @staticmethod
    def _command(configured):
        """Configure native dependencies alongside an independent Python requirement."""
        return _command(
            {
                "tool.flet.android.dependencies": ["requests>=2"],
                "tool.flet.android.gradle_dependencies": configured,
            }
        )

    @pytest.mark.parametrize("configured", [None, "", " \n  "])
    def test_empty_gradle_dependencies_preserve_python_dependencies(self, configured):
        """Empty native declarations leave platform Python requirements intact."""
        cmd = self._command(configured)
        assert cmd.get_android_gradle_dependencies() == ""
        assert get_project_dependencies(
            cmd.get_pyproject("tool.flet.android.dependencies")
        ) == ["requests >=2"]

    @pytest.mark.parametrize("configured", [[], {}, {"implementation": []}, False, 17])
    def test_invalid_dependency_setting(self, configured):
        """Reject dependency settings that are not Kotlin source strings."""
        with pytest.raises(ValueError, match=r"android\.gradle_dependencies.*string"):
            self._command(configured).get_android_gradle_dependencies()

    def test_dependency_block_preserves_kotlin_syntax(self):
        """Preserve nested Kotlin, interpolation, and template-like text verbatim."""
        configured = r"""
            // Native declarations, with Gradle/Kotlin expressions kept intact.
            implementation(platform("com.example:bom:1.0"))
            implementation("com.example:library") {
                exclude(group = "com.example", module = "unwanted")
                because("Needed by ${project.name}")
            }
            implementation(files("libs/example.jar"))
            implementation(libs.example)
            constraints {
                implementation("com.example:other:2.0")
            }
            // {{ this_must_not_be_processed_as_jinja }}
        """
        cmd = self._command(configured)
        resolved = cmd.get_android_gradle_dependencies()
        assert resolved.startswith("// Native declarations")
        assert '    because("Needed by ${project.name}")' in resolved
        assert "{{ this_must_not_be_processed_as_jinja }}" in resolved
        rendered = _render_gradle(cmd)
        expected_body = "\n".join("    " + line for line in resolved.splitlines())
        assert expected_body in rendered
        assert 'implementation(platform("com.example:bom:1.0"))' in rendered
        assert "{{ this_must_not_be_processed_as_jinja }}" in rendered


class TestApplicationAttributes:
    """Cover Flet's `<application>` defaults and the app's overrides."""

    @staticmethod
    def _application(configured):
        """Render application settings and return the `<application>` element."""
        manifest = _render_manifest(
            _command({"tool.flet.android.manifest_application": configured})
        )
        return manifest.find("application")

    @staticmethod
    def _attributes(element):
        """Return an element's Android attributes without the namespace."""
        prefix = f"{{{ANDROID_NS}}}"
        return {
            key[len(prefix) :]: value
            for key, value in element.attrib.items()
            if key.startswith(prefix)
        }

    @pytest.mark.parametrize("configured", [None, {}])
    def test_defaults_without_settings(self, configured):
        """Without settings, `<application>` gets Flet's four attributes."""
        assert self._attributes(self._application(configured)) == {
            "label": "Example",
            "name": "${applicationName}",
            "enableOnBackInvokedCallback": "true",
            "icon": "@mipmap/ic_launcher",
        }

    def test_overrides_replace_defaults_once_and_values_are_escaped(self):
        """Overriding a default writes it once; booleans and XML are normalized."""
        configured = {
            "label": 'A&B "app" <x>',
            "icon": "@mipmap/custom",
            "enableOnBackInvokedCallback": False,
            "allowBackup": False,
            "usesCleartextTraffic": "true",
            "networkSecurityConfig": "@xml/network_security_config",
        }
        before = copy.deepcopy(configured)
        attributes = self._attributes(self._application(configured))
        assert configured == before
        assert attributes == {
            "label": 'A&B "app" <x>',
            "name": "${applicationName}",
            "enableOnBackInvokedCallback": "false",
            "icon": "@mipmap/custom",
            "allowBackup": "false",
            "usesCleartextTraffic": "true",
            "networkSecurityConfig": "@xml/network_security_config",
        }

    @pytest.mark.parametrize(
        "configured, path",
        [
            ([], "tool.flet.android.manifest_application"),
            ({"bad:name": "x"}, "tool.flet.android.manifest_application"),
            ({"allowBackup": []}, "manifest_application.allowBackup"),
        ],
    )
    def test_invalid_attributes_report_the_setting_path(self, configured, path):
        """Identify the malformed application attribute in errors."""
        with pytest.raises(ValueError) as error:
            _command(
                {"tool.flet.android.manifest_application": configured}
            ).get_android_application_attributes("Example")
        assert path in str(error.value)


class TestQueries:
    """Cover package, intent, and provider queries and the built-in query."""

    @staticmethod
    def _resolve(configured):
        """Resolve query declarations through the build command."""
        return _command({"tool.flet.android.queries": configured}).get_android_queries()

    @staticmethod
    def _queries(configured):
        """Render query settings and return the manifest's `<queries>` element."""
        manifest = _render_manifest(_command({"tool.flet.android.queries": configured}))
        assert len(manifest.findall("queries")) == 1
        return manifest.find("queries")

    @staticmethod
    def _attr(element, key):
        """Return an Android XML attribute of an element."""
        return element.get(f"{{{ANDROID_NS}}}{key}")

    @pytest.mark.parametrize("configured", [None, {}])
    def test_absent_queries_keep_only_the_built_in_intent(self, configured):
        """Without settings, `<queries>` holds only Flet's PROCESS_TEXT intent."""
        queries = self._queries(configured)
        assert [child.tag for child in queries] == ["intent"]
        assert (
            self._attr(queries.find("intent/action"), "name")
            == "android.intent.action.PROCESS_TEXT"
        )

    def test_packages_intents_and_providers_render_after_the_built_in_intent(self):
        """Render every declaration in order, escaped, without mutating the input."""
        configured = {
            "packages": ["com.eg.android.AlipayGphone", "com.tencent.mm"],
            "intent": [
                {"action": "android.intent.action.VIEW", "data": {"scheme": "alipays"}},
                {
                    "action": "android.intent.action.VIEW",
                    "categories": ["android.intent.category.BROWSABLE"],
                    "data": [{"scheme": "https"}, {"host": 'a&b"<c>'}],
                },
                {
                    "action": "android.intent.action.SEND",
                    "data": {"mimeType": "image/*"},
                },
            ],
            "providers": ["com.example.settings;com.example.files"],
        }
        before = copy.deepcopy(configured)
        queries = self._queries(configured)
        assert configured == before
        assert [child.tag for child in queries] == [
            "intent",
            "package",
            "package",
            "intent",
            "intent",
            "intent",
            "provider",
        ]
        assert [self._attr(p, "name") for p in queries.findall("package")] == [
            "com.eg.android.AlipayGphone",
            "com.tencent.mm",
        ]
        intents = queries.findall("intent")[1:]
        assert self._attr(intents[0].find("action"), "name") == (
            "android.intent.action.VIEW"
        )
        assert intents[0].find("category") is None
        assert self._attr(intents[0].find("data"), "scheme") == "alipays"
        assert [self._attr(c, "name") for c in intents[1].findall("category")] == [
            "android.intent.category.BROWSABLE"
        ]
        data = intents[1].findall("data")
        assert [self._attr(d, "scheme") for d in data] == ["https", None]
        assert self._attr(data[1], "host") == 'a&b"<c>'
        assert self._attr(intents[2].find("data"), "mimeType") == "image/*"
        assert self._attr(queries.find("provider"), "authorities") == (
            "com.example.settings;com.example.files"
        )

    def test_duplicates_and_whitespace_are_dropped(self):
        """Repeated packages and providers appear once; names are trimmed."""
        assert self._resolve(
            {
                "packages": ["com.example.app", " com.example.app ", "com.example.b"],
                "providers": ["com.example.files", "com.example.files"],
                "intent": [{"action": " android.intent.action.VIEW "}],
            }
        ) == {
            "packages": ["com.example.app", "com.example.b"],
            "intents": [
                {"action": "android.intent.action.VIEW", "categories": [], "data": []}
            ],
            "providers": ["com.example.files"],
        }

    @pytest.mark.parametrize(
        "configured, path",
        [
            ([], "tool.flet.android.queries"),
            ({"package": ["com.example.app"]}, "queries.package"),
            ({"packages": "com.example.app"}, "queries.packages"),
            ({"packages": ["app"]}, "queries.packages"),
            ({"packages": ["com.example.my app"]}, "queries.packages"),
            ({"providers": [""]}, "queries.providers"),
            ({"providers": ["a;;b"]}, "queries.providers"),
            ({"intent": {"action": "a"}}, "queries.intent"),
            ({"intent": [False]}, "queries.intent[0]"),
            ({"intent": [{}]}, "intent[0].action"),
            ({"intent": [{"action": ["a", "b"]}]}, "intent[0].action"),
            ({"intent": [{"action": "a", "actions": ["b"]}]}, "intent[0].actions"),
            ({"intent": [{"action": "a", "categories": "c"}]}, "intent[0].categories"),
            ({"intent": [{"action": "a", "data": "https"}]}, "intent[0].data"),
            ({"intent": [{"action": "a", "data": [{}]}]}, "intent[0].data[0]"),
            (
                {"intent": [{"action": "a", "data": {"path": "/pay"}}]},
                "intent[0].data.path",
            ),
            (
                {"intent": [{"action": "a", "data": {"scheme": ""}}]},
                "intent[0].data.scheme",
            ),
            (
                {
                    "intent": [
                        {"action": "a", "data": [{"scheme": "a"}, {"scheme": "b"}]}
                    ]
                },
                "intent[0].data[1].scheme",
            ),
        ],
    )
    def test_invalid_queries_report_the_setting_path(self, configured, path):
        """Identify the malformed query declaration in errors."""
        with pytest.raises(ValueError) as error:
            self._resolve(configured)
        assert path in str(error.value)


class TestActivityIntentFilters:
    """Cover intent filters added to the main activity and shared filter rules."""

    @staticmethod
    def _activity(configured):
        """Render activity settings and return the main `<activity>` element."""
        manifest = _render_manifest(
            _command({"tool.flet.android.activity": configured})
        )
        return manifest.find("application/activity")

    @staticmethod
    def _attr(element, key):
        """Return an Android XML attribute of an element."""
        return element.get(f"{{{ANDROID_NS}}}{key}")

    @pytest.mark.parametrize("configured", [None, {}, {"intent_filter": []}])
    def test_without_settings_only_the_launcher_filter_remains(self, configured):
        """Without filters, the activity keeps only Flet's launcher filter."""
        filters = self._activity(configured).findall("intent-filter")
        assert len(filters) == 1
        assert (
            self._attr(filters[0].find("action"), "name")
            == "android.intent.action.MAIN"
        )

    def test_filters_render_after_flets_with_attributes_and_data(self):
        """Render each filter's attributes, actions, categories and data in order."""
        configured = {
            "intent_filter": [
                {
                    "autoVerify": True,
                    "actions": ["android.intent.action.VIEW"],
                    "categories": [
                        "android.intent.category.DEFAULT",
                        "android.intent.category.BROWSABLE",
                    ],
                    "data": [
                        {"scheme": "https", "host": "example.com"},
                        {"pathPrefix": "/invite"},
                    ],
                },
                {
                    "actions": ["android.intent.action.SEND"],
                    "categories": ["android.intent.category.DEFAULT"],
                    "data": {"mimeType": "text/plain"},
                    "label": 'A&B "share"',
                },
            ]
        }
        before = copy.deepcopy(configured)
        filters = self._activity(configured).findall("intent-filter")
        assert configured == before
        assert len(filters) == 3
        view, send = filters[1], filters[2]
        assert self._attr(view, "autoVerify") == "true"
        assert [self._attr(c, "name") for c in view.findall("category")] == [
            "android.intent.category.DEFAULT",
            "android.intent.category.BROWSABLE",
        ]
        assert [
            {k.split("}")[1]: v for k, v in d.attrib.items()}
            for d in view.findall("data")
        ] == [{"scheme": "https", "host": "example.com"}, {"pathPrefix": "/invite"}]
        assert self._attr(send.find("action"), "name") == "android.intent.action.SEND"
        assert self._attr(send.find("data"), "mimeType") == "text/plain"
        assert self._attr(send, "label") == 'A&B "share"'

    def test_receiver_filters_accept_data_and_attributes(self):
        """Receivers share the same filter rules, including `<data>`."""
        manifest = _render_manifest(
            _command(
                {
                    "tool.flet.android.receiver": {
                        "com.example.Packages": {
                            "exported": True,
                            "intent_filter": [
                                {
                                    "priority": 10,
                                    "actions": ["android.intent.action.PACKAGE_ADDED"],
                                    "data": {"scheme": "package"},
                                }
                            ],
                        }
                    }
                }
            )
        )
        intent_filter = manifest.find("application/receiver/intent-filter")
        assert self._attr(intent_filter, "priority") == "10"
        assert self._attr(intent_filter.find("data"), "scheme") == "package"

    @pytest.mark.parametrize(
        "configured, path",
        [
            ([], "tool.flet.android.activity"),
            ({"launchMode": "singleTask"}, "activity.launchMode"),
            ({"intent_filter": {}}, "activity.intent_filter"),
            ({"intent_filter": [False]}, "intent_filter[0]"),
            ({"intent_filter": [{}]}, "intent_filter[0].actions"),
            ({"intent_filter": [{"action": "a"}]}, "intent_filter[0].action"),
            (
                {"intent_filter": [{"actions": ["a"], "category": "c"}]},
                "intent_filter[0].category",
            ),
            (
                {"intent_filter": [{"actions": ["a"], "data": "https"}]},
                "intent_filter[0].data",
            ),
            (
                {"intent_filter": [{"actions": ["a"], "data": [{}]}]},
                "intent_filter[0].data[0]",
            ),
            (
                {"intent_filter": [{"actions": ["a"], "data": {"bad:key": "x"}}]},
                "intent_filter[0].data",
            ),
            (
                {"intent_filter": [{"actions": ["a"], "autoVerify": []}]},
                "intent_filter[0].autoVerify",
            ),
        ],
    )
    def test_invalid_activity_settings_report_the_setting_path(self, configured, path):
        """Identify the malformed activity setting or filter in errors."""
        with pytest.raises(ValueError) as error:
            _command({"tool.flet.android.activity": configured}).get_android_activity()
        assert path in str(error.value)


class TestReceivers:
    """Cover receiver declarations, intent filters, and manifest preservation."""

    @staticmethod
    def _resolve(configured):
        """Resolve receiver declarations through the build command."""
        return _command(
            {"tool.flet.android.receiver": configured}
        ).get_android_receivers()

    def _manifest(self, configured):
        """Render receiver settings alongside existing app manifest entries."""
        return _render_manifest(_command({"tool.flet.android.receiver": configured}))

    @pytest.mark.parametrize(
        "configured",
        [None, {}, {"com.example.Skipped": False}, {"com.example.Skipped": {}}],
    )
    def test_absent_or_disabled_receivers_preserve_other_manifest_entries(
        self, configured
    ):
        """Skipping receivers must preserve providers, permissions, and the activity."""
        manifest = self._manifest(configured)
        assert manifest.findall("application/receiver") == []
        assert len(manifest.findall("application/provider")) == 2
        assert len(manifest.findall("uses-permission")) == 1
        assert manifest.find("application/activity") is not None

    def test_receivers_and_filters_escape_xml_and_preserve_configuration(self):
        """Round-trip XML values and distinct filters without mutating the input."""
        configured = {
            "com.example.Simple": {"exported": False, "enabled": True},
            "com.example.Events": {
                "exported": "false",
                "label": 'A&B <events> "label"',
                "intent_filter": [
                    {
                        "actions": ["com.example.FIRST", "com.example.SECOND"],
                        "categories": ["com.example.DEFAULT"],
                    },
                    {"actions": ['com.example.QUOTED&"ACTION']},
                ],
            },
        }
        before = copy.deepcopy(configured)
        manifest = self._manifest(configured)
        assert configured == before
        name = f"{{{ANDROID_NS}}}name"
        receivers = {
            receiver.get(name): receiver
            for receiver in manifest.findall("application/receiver")
        }
        assert (
            receivers["com.example.Simple"].get(f"{{{ANDROID_NS}}}exported") == "false"
        )
        assert receivers["com.example.Simple"].get(f"{{{ANDROID_NS}}}enabled") == "true"
        events = receivers["com.example.Events"]
        assert (
            events.get(f"{{{ANDROID_NS}}}label")
            == configured["com.example.Events"]["label"]
        )
        filters = events.findall("intent-filter")
        assert len(filters) == 2
        assert [a.get(name) for a in filters[0].findall("action")] == [
            "com.example.FIRST",
            "com.example.SECOND",
        ]
        assert [c.get(name) for c in filters[0].findall("category")] == [
            "com.example.DEFAULT"
        ]
        assert filters[1].find("action").get(name) == 'com.example.QUOTED&"ACTION'

    @pytest.mark.parametrize(
        "configured, path",
        [
            ([], "tool.flet.android.receiver"),
            ({"": {"exported": False}}, "receiver"),
            ({"com.example.Bad": True}, 'receiver."com.example.Bad"'),
            ({"com.example.Bad": "false"}, 'receiver."com.example.Bad"'),
            ({"com.example.Bad": {"name": "other"}}, ".name"),
            ({"com.example.Bad": {"bad:name": "value"}}, 'receiver."com.example.Bad"'),
            ({"com.example.Bad": {"enabled": []}}, ".enabled"),
            ({"com.example.Bad": {"intent_filter": {}}}, ".intent_filter"),
            ({"com.example.Bad": {"intent_filter": [False]}}, ".intent_filter[0]"),
            ({"com.example.Bad": {"intent_filter": [{"actions": "one"}]}}, ".actions"),
            ({"com.example.Bad": {"intent_filter": [{"actions": [" "]}]}}, ".actions"),
            ({"com.example.Bad": {"intent_filter": [{}]}}, ".actions"),
            (
                {
                    "com.example.Bad": {
                        "intent_filter": [{"actions": ["one"], "categories": [1]}]
                    }
                },
                ".categories",
            ),
            (
                {
                    "com.example.Bad": {
                        "intent_filter": [{"actions": ["one"], "action": []}]
                    }
                },
                ".action",
            ),
            (
                {"com.example.Bad": {"intent_filter": [{"actions": ["one"]}]}},
                ".exported",
            ),
        ],
    )
    def test_invalid_receivers_report_the_setting_path(self, configured, path):
        """Identify the malformed receiver attribute or nested filter in errors."""
        with pytest.raises(ValueError) as error:
            self._resolve(configured)
        assert path in str(error.value)


class TestServices:
    """Cover service attributes, nested properties, metadata, and XML rendering."""

    @staticmethod
    def _resolve(configured):
        """Resolve service declarations through the build command."""
        return _command(
            {"tool.flet.android.service": configured}
        ).get_android_services()

    @pytest.mark.parametrize(
        "configured",
        [None, {}, {"com.example.Skipped": False}, {"com.example.Skipped": {}}],
    )
    def test_absent_or_disabled_services_preserve_manifest(self, configured):
        """Skipping services leaves existing providers and app entries intact."""
        manifest = _render_manifest(_command({"tool.flet.android.service": configured}))
        assert manifest.findall("application/service") == []
        assert len(manifest.findall("application/provider")) == 2
        assert len(manifest.findall("uses-permission")) == 1
        assert manifest.find("application/activity") is not None

    def test_services_and_children_preserve_values(self):
        """Round-trip child values and resources without mutating configuration."""
        configured = {
            "com.example.Simple": {"exported": False, "enabled": True},
            "com.example.Special": {
                "exported": False,
                "foregroundServiceType": "specialUse",
                "property": {
                    "android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE": {
                        "value": 'A&B <work> "description"'
                    },
                    "com.example.label": {"resource": "@string/app_name"},
                },
                "meta_data": {
                    "com.example.enabled": False,
                    "com.example.count": 3,
                    "com.example.title": "A&B",
                    "com.example.resource": {"resource": "@string/app_name"},
                },
            },
        }
        before = copy.deepcopy(configured)
        manifest = _render_manifest(_command({"tool.flet.android.service": configured}))
        assert configured == before

        def attr(key):
            """Return a qualified Android XML attribute name."""
            return f"{{{ANDROID_NS}}}{key}"

        services = {
            service.get(attr("name")): service
            for service in manifest.findall("application/service")
        }
        simple = services["com.example.Simple"]
        assert simple.get(attr("exported")) == "false"
        assert simple.get(attr("enabled")) == "true"
        special = services["com.example.Special"]
        assert special.get(attr("foregroundServiceType")) == "specialUse"
        properties = {
            child.get(attr("name")): child for child in special.findall("property")
        }
        assert (
            properties["android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"].get(
                attr("value")
            )
            == 'A&B <work> "description"'
        )
        assert (
            properties["com.example.label"].get(attr("resource")) == "@string/app_name"
        )
        metadata = {
            child.get(attr("name")): child for child in special.findall("meta-data")
        }
        assert metadata["com.example.enabled"].get(attr("value")) == "false"
        assert metadata["com.example.count"].get(attr("value")) == "3"
        assert metadata["com.example.title"].get(attr("value")) == "A&B"
        assert (
            metadata["com.example.resource"].get(attr("resource")) == "@string/app_name"
        )

    @pytest.mark.parametrize(
        "configured, path",
        [
            ([], "tool.flet.android.service"),
            ({"": {"exported": False}}, "service"),
            ({"com.example.Bad": True}, 'service."com.example.Bad"'),
            ({"com.example.Bad": {"name": "other"}}, ".name"),
            ({"com.example.Bad": {"bad:name": "value"}}, 'service."com.example.Bad"'),
            ({"com.example.Bad": {"enabled": []}}, ".enabled"),
            ({"com.example.Bad": {"property": []}}, ".property"),
            ({"com.example.Bad": {"meta_data": False}}, ".meta_data"),
            ({"com.example.Bad": {"property": {"": "value"}}}, ".property"),
            ({"com.example.Bad": {"property": {"subtype": {}}}}, '.property."subtype"'),
            (
                {
                    "com.example.Bad": {
                        "property": {
                            "subtype": {"value": "x", "resource": "@string/app_name"}
                        }
                    }
                },
                '.property."subtype"',
            ),
            (
                {"com.example.Bad": {"meta_data": {"entry": []}}},
                '.meta_data."entry".value',
            ),
            (
                {"com.example.Bad": {"meta_data": {"entry": {"resource": False}}}},
                '.meta_data."entry".resource',
            ),
            (
                {
                    "com.example.Bad": {
                        "property": {"entry": {"name": "other", "value": "x"}}
                    }
                },
                '.property."entry".name',
            ),
        ],
    )
    def test_invalid_services_report_setting_path(self, configured, path):
        """Identify malformed services and named child declarations in errors."""
        with pytest.raises(ValueError) as error:
            self._resolve(configured)
        assert path in str(error.value)


def _resources_command(tmp_path, settings):
    """Create a build command with a generated Android project for resources."""
    cmd = _command(settings)
    cmd.package_platform = "Android"
    cmd.python_app_path = tmp_path
    cmd.build_dir = tmp_path / "build"
    cmd.flutter_dir = cmd.build_dir / "flutter"
    cmd.step = lambda status: contextlib.nullcontext()
    res = cmd.flutter_dir / "android/app/src/main/res"
    _write(res / "mipmap-hdpi/ic_launcher.png", b"launcher")
    _write(res / "drawable-xhdpi/splash.png", b"splash")
    _write(res / "values/colors.xml", b"colors")
    return cmd, res


def _write(path, data=b"data"):
    """Create a file and its parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


class TestResources:
    SETTINGS = {"tool.flet.android.res_dir": "android_res"}

    def test_copies_resources_and_keeps_those_referenced_by_name(self, tmp_path):
        """Resources are copied, and every file-based one is kept from shrinking."""
        source = tmp_path / "android_res"
        _write(source / "drawable-hdpi/ic_stat.png", b"hdpi")
        _write(source / "drawable-xhdpi/ic_stat.png", b"xhdpi")
        _write(source / "raw/alert.mp3")
        _write(source / "values/brand.xml")
        _write(source / "raw/.DS_Store")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)

        cmd.copy_android_resources()

        assert (res / "drawable-hdpi/ic_stat.png").read_bytes() == b"hdpi"
        assert (res / "drawable-xhdpi/ic_stat.png").read_bytes() == b"xhdpi"
        assert (res / "raw/alert.mp3").exists()
        assert (res / "values/brand.xml").exists()
        assert not (res / "raw/.DS_Store").exists()
        keep = ET.parse(res / "raw/flet_res_keep.xml").getroot()
        assert keep.get("{http://schemas.android.com/tools}keep") == (
            "@drawable/ic_stat,@raw/alert"
        )

    def test_rebuilds_remove_resources_no_longer_supplied(self, tmp_path):
        """Removing a resource, or the setting, removes it from the next build."""
        source = tmp_path / "android_res"
        _write(source / "drawable/ic_stat.png")
        _write(source / "raw/alert.mp3")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)
        cmd.copy_android_resources()

        (source / "raw/alert.mp3").unlink()
        cmd.copy_android_resources()
        assert (res / "drawable/ic_stat.png").exists()
        assert not (res / "raw/alert.mp3").exists()
        assert "@raw/alert" not in (res / "raw/flet_res_keep.xml").read_text()

        cmd.get_pyproject = {}.get
        cmd.copy_android_resources()
        assert not (res / "drawable/ic_stat.png").exists()
        assert not (res / "raw/flet_res_keep.xml").exists()
        assert (res / "mipmap-hdpi/ic_launcher.png").exists()

    def test_values_only_resources_need_no_keep_rule(self, tmp_path):
        """Resources defined in values files produce no keep file."""
        _write(tmp_path / "android_res/values/strings.xml")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)

        cmd.copy_android_resources()

        assert (res / "values/strings.xml").exists()
        assert not (res / "raw/flet_res_keep.xml").exists()

    @pytest.mark.parametrize(
        ("path", "generated"),
        [
            ("mipmap-hdpi/ic_launcher.png", "mipmap-hdpi/ic_launcher.png"),
            ("drawable-ldpi/splash.png", "drawable-xhdpi/splash.png"),
            ("drawable/splash.xml", "drawable-xhdpi/splash.png"),
            ("values/colors.xml", "values/colors.xml"),
            ("raw/flet_res_keep.txt", "raw/flet_res_keep.xml"),
        ],
    )
    def test_resources_flet_generates_are_reserved_by_name(
        self, tmp_path, path, generated
    ):
        """Any file defining a resource Flet generates is rejected before copying."""
        _write(tmp_path / "android_res/drawable/ic_stat.png")
        _write(tmp_path / "android_res" / path, b"mine")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)

        with pytest.raises(ValueError, match="clash") as exc:
            cmd.copy_android_resources()
        assert f"{path} (Flet's {generated})" in str(exc.value)
        assert not (res / "drawable/ic_stat.png").exists()
        assert (res / "mipmap-hdpi/ic_launcher.png").read_bytes() == b"launcher"

    def test_other_values_files_merge_with_flet_values(self, tmp_path):
        """A values file with its own name is copied beside Flet's values files."""
        _write(tmp_path / "android_res/values/brand_colors.xml")
        _write(tmp_path / "android_res/values-night/colors.xml")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)

        cmd.copy_android_resources()

        assert (res / "values/brand_colors.xml").exists()
        assert (res / "values-night/colors.xml").exists()
        assert (res / "values/colors.xml").read_bytes() == b"colors"

    @pytest.mark.parametrize(
        ("path", "message"),
        [
            ("sounds/alert.mp3", "unknown Android resource type 'sounds'"),
            ("drawable/Icon-1.png", "lowercase letters, digits, and underscores"),
            ("drawable/1icon.png", "must start with a letter"),
            ("drawable/nested/icon.png", "cannot be nested"),
            ("drawable/icon.png+drawable/icon.xml", "the same resource as icon.png"),
            ("icon.png", "expected a resource type directory"),
        ],
    )
    def test_invalid_layouts_report_the_setting(self, tmp_path, path, message):
        """Malformed resource directories fail with the offending entry."""
        for part in path.split("+"):
            _write(tmp_path / "android_res" / part)
        cmd, _ = _resources_command(tmp_path, self.SETTINGS)

        with pytest.raises(ValueError, match="tool.flet.android.res_dir") as exc:
            cmd.copy_android_resources()
        assert message in str(exc.value)

    def test_missing_directory_reports_the_setting(self, tmp_path):
        """A res_dir that does not exist fails the build."""
        cmd, _ = _resources_command(tmp_path, self.SETTINGS)

        with pytest.raises(ValueError, match="is not a directory"):
            cmd.copy_android_resources()

    def test_other_platforms_ignore_resources(self, tmp_path):
        """Builds for other platforms neither validate nor copy resources."""
        _write(tmp_path / "android_res/drawable/ic_stat.png")
        cmd, res = _resources_command(tmp_path, self.SETTINGS)
        cmd.package_platform = "iOS"

        cmd.copy_android_resources()

        assert not (res / "drawable").exists()
