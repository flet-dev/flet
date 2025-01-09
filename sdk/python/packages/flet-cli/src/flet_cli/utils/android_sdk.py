import platform
import subprocess

# TODO:
# - check if Android SDK is already installed as part of Android Studio
# - download commandlinetools
#
#
#
#
ANDROID_CMDLINE_TOOLS_VERSION = "11076708"
ANDROID_API_VERSION = "35"
BUILD_TOOLS_VERSION = "33.0.1"


def cmdline_tools_url():
    try:
        url_platform = {
            "Darwin": {
                "arm64": "mac",
                "x86_64": "mac",
            },
            "Linux": {
                "x86_64": "linux",
            },
            "Windows": {
                "AMD64": "win",
            },
        }[platform.system()][platform.machine()]
    except KeyError as e:
        raise Exception(
            f"Unsupported platform: {platform.system()}-{platform.machine()}"
        )

    return (
        f"https://dl.google.com/android/repository/"
        f"commandlinetools-{url_platform}-{ANDROID_CMDLINE_TOOLS_VERSION}_latest.zip"
    )


def install_android_sdk():
    # path to installed Android SDK
    return ""


def accept_sdkmanager_licenses():
    """
    Automatically accept all licenses for the Android SDK Manager.
    """
    try:
        # Define the command for sdkmanager --licenses
        command = [
            "C:\\Android\\sdk\\cmdline-tools\\latest\\bin\\sdkmanager.bat",
            "--licenses",
        ]

        # Run the command, sending 'y' (yes) to approve all licenses
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={"JAVA_HOME": "C:\\Users\\feodo\\java\\17.0.13+11"},
        )
        # Simulate accepting licenses by sending 'y' repeatedly
        stdout, stderr = process.communicate(input="y\n" * 100)

        # Check the process return code
        if process.returncode == 0:
            print("All licenses accepted successfully.")
        else:
            print(f"Failed to accept licenses. Error: {stderr}")
    except FileNotFoundError:
        print(
            "sdkmanager not found. Ensure the Android SDK is installed and in your PATH."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    jdk_path = accept_sdkmanager_licenses()
