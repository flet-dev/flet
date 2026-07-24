import java.util.Properties

plugins {
    id("com.android.application")
    // Kotlin is provided by the Flutter Gradle Plugin (Built-in Kotlin), so the
    // app no longer applies the Kotlin Gradle Plugin itself.
    // The Flutter Gradle Plugin must be applied after the Android Gradle plugin.
    id("dev.flutter.flutter-gradle-plugin")
}

val localProperties = Properties().apply {
    val localPropertiesFile = rootProject.file("local.properties")
    if (localPropertiesFile.exists()) {
        localPropertiesFile.inputStream().use { load(it) }
    }
}

val flutterVersionCode = localProperties.getProperty("flutter.versionCode")?.toIntOrNull() ?: 1
val flutterVersionName = localProperties.getProperty("flutter.versionName") ?: "1.0"

android {
    namespace = "{{ cookiecutter.org_name_2 }}.{{ cookiecutter.package_name }}"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    // serious_python loads Python extension modules memory-mapped directly from the
    // APK (no extraction) and ships pure Python in stored asset zips, so
    // `useLegacyPackaging` / `keepDebugSymbols` from earlier Flet templates are no
    // longer needed at minSdk 23+. The `pickFirsts` and `excludes` blocks below
    // address two unrelated multi-source jniLibs issues that AGP can't resolve on
    // its own.
    packaging {
        jniLibs {
            // serious_python_android ships libc++_shared.so as part of the Python runtime payload
            // (the cross-compiled wheels on pypi.flet.dev depend on it at link time). Many third-party
            // Flutter plugins (ultralytics_yolo, sentry_flutter, several ML / CV / audio plugins) also
            // bundle their own copy. When an app pulls in both, Gradle's mergeNativeLibs task aborts
            // with "N files found with path 'lib/<abi>/libc++_shared.so'" because AGP refuses to silently
            // choose between duplicate native libraries (the right default for most .so files).
            //
            // libc++_shared.so is a documented exception: the NDK has held strict ABI compatibility on it
            // since r17, so whichever copy wins input ordering, every consumer that linked against libc++_shared
            // will work against it. pickFirsts is the narrowly-scoped escape hatch for exactly this case -- it
            // only opens a hole for the matching glob; any other future duplicate-native-lib conflict still fails loudly.
            pickFirsts += listOf("**/libc++_shared.so")

// flet: legacy_packaging {% if cookiecutter.options.android_legacy_packaging %}
            // Legacy native-library packaging (opt-in via `--android-legacy-packaging` /
            // `[tool.flet.android].legacy_packaging`). The installer extracts every `.so`
            // to nativeLibraryDir on install instead of the app memory-mapping them
            // straight from the APK. Produces a smaller raw `.apk` for side-loading and
            // a larger on-device install (a second, extracted copy of the libs).
            useLegacyPackaging = true
// flet: end of legacy_packaging {% endif %}

// flet: excluded_abis {% if cookiecutter.options.android_excluded_abis %}
            // Strip native libs of ABIs not requested via `target_arch`.
            // `ndk.abiFilters` alone can't do this: the Flutter Gradle plugin adds all default
            // ABIs as buildType-level filters and AGP merges the two levels as a union.
            excludes += listOf({% for abi in cookiecutter.options.android_excluded_abis %}"lib/{{ abi }}/**"{% if not loop.last %}, {% endif %}{% endfor %})
// flet: end of excluded_abis {% endif %}
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    sourceSets["main"].java.srcDir("src/main/kotlin")

    {% set min_sdk_version = get_pyproject("tool.flet.android.min_sdk_version") %}
    {% set target_sdk_version = get_pyproject("tool.flet.android.target_sdk_version") %}

    defaultConfig {
        applicationId = "{{ cookiecutter.org_name_2 }}.{{ cookiecutter.package_name }}"
        val resolvedMinSdk = {{ min_sdk_version if min_sdk_version else "flutter.minSdkVersion" }}
        minSdk = resolvedMinSdk
        val resolvedTargetSdk = {{ target_sdk_version if target_sdk_version else "flutter.targetSdkVersion" }}
        targetSdk = resolvedTargetSdk
        versionCode = flutterVersionCode
        versionName = flutterVersionName

        println("Gradle build config:")
        println("  minSdkVersion: $resolvedMinSdk")
        println("  targetSdkVersion: $resolvedTargetSdk")
        println("  versionCode: $flutterVersionCode")
        println("  versionName: $flutterVersionName")

// flet: split_per_abi {% if not cookiecutter.split_per_abi %}
        ndk {
            {% if cookiecutter.options.target_arch %}
            abiFilters += listOf({% for arch in cookiecutter.options.target_arch %}"{{ arch }}"{% if not loop.last %}, {% endif %}{% endfor %})
            {% else %}
            abiFilters += listOf("arm64-v8a", "armeabi-v7a", "x86_64")
            {% endif %}
        }
// flet: end of split_per_abi {% endif %}
    }

// flet: android_signing {% if cookiecutter.options.android_signing %}
    signingConfigs {
        create("release") {
            keyAlias = System.getenv("FLET_ANDROID_SIGNING_KEY_ALIAS")
            keyPassword = System.getenv("FLET_ANDROID_SIGNING_KEY_PASSWORD")
            storeFile = System.getenv("FLET_ANDROID_SIGNING_KEY_STORE")?.let { file(it) }
            storePassword = System.getenv("FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD")
        }
    }
// flet: end of android_signing {% endif %}

    buildTypes {
        release {
// flet: android_signing {% if cookiecutter.options.android_signing %}
            signingConfig = signingConfigs.getByName("release")
// {% else %}
            signingConfig = signingConfigs.getByName("debug")
// flet: end of android_signing {% endif %}
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}

dependencies {}
