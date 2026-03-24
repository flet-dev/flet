import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
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

    packaging {
        jniLibs {
            useLegacyPackaging = true
            keepDebugSymbols += listOf(
                "*/arm64-v8a/libpython*.so",
                "*/armeabi-v7a/libpython*.so",
                "*/x86/libpython*.so",
                "*/x86_64/libpython*.so",
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
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

flutter {
    source = "../.."
}

dependencies {}
