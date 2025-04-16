import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from flet_cli.utils.distros import download_with_progress, extract_with_progress
from rich.console import Console
from rich.progress import Progress

# Constants
JDK_MAJOR_VER = 17
JDK_RELEASE = "17.0.13"
JDK_BUILD = "11"
JDK_DIR_NAME = f"{JDK_RELEASE}+{JDK_BUILD}"


def get_java_home():
    return os.getenv("JAVA_HOME")


def check_jdk_version(jdk_path):
    try:
        result = subprocess.run(
            [os.path.join(jdk_path, "bin", "javac"), "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        version_line = result.stdout.strip("\n").split(" ")[
            1
        ]  # Extract version from output
        major_version = int(version_line.split(".")[0])
        return major_version == JDK_MAJOR_VER
    except (IndexError, ValueError, FileNotFoundError) as e:
        return False


def platform_info():
    """Detect platform and architecture details."""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if system == "darwin":
        platform_name = "mac"
        arch_name = "aarch64" if arch == "arm64" else "x64"
        ext = "tar.gz"
    elif system == "linux":
        platform_name = "linux"
        if arch in ["armv7l", "armv8l"]:
            arch_name = "arm"
        elif arch == "aarch64":
            arch_name = "aarch64"
        else:
            arch_name = "x64"
        ext = "tar.gz"
    elif system == "windows":
        platform_name = "windows"
        arch_name = "x64"  # Assuming only x64 for simplicity
        ext = "zip"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    return platform_name, arch_name, ext


def install_jdk(log, progress: Optional[Progress] = None):
    java_home = get_java_home()

    # Step 1: Check if JAVA_HOME is set and valid
    if java_home and check_jdk_version(java_home):
        return java_home
    elif java_home:
        log("JAVA_HOME points to a JRE. Proceeding to install JDK.")

    # Step 2: On macOS, try /usr/libexec/java_home
    if platform.system() == "Darwin":
        try:
            java_home = subprocess.check_output(
                ["/usr/libexec/java_home"], text=True
            ).strip()
            log(f"JAVA HOME for macOS: {java_home}")
            if check_jdk_version(java_home):
                log(f"Using JDK from /usr/libexec/java_home: {java_home}")
                return java_home
        except subprocess.CalledProcessError:
            pass  # No valid JDK found, proceed with installation

    # Step 3: Determine platform-specific download URL
    platform_name, arch_name, ext = platform_info()
    url = (
        f"https://github.com/adoptium/temurin{JDK_MAJOR_VER}-binaries/"
        f"releases/download/jdk-{JDK_RELEASE}+{JDK_BUILD}/"
        f"OpenJDK{JDK_MAJOR_VER}U-jdk_{arch_name}_{platform_name}_hotspot_"
        f"{JDK_RELEASE}_{JDK_BUILD}.{ext}"
    )

    install_dir = Path.home() / "java" / JDK_DIR_NAME

    # Step 4: Check if JDK is already installed
    if not install_dir.exists():

        # Step 5: Download and extract JDK
        archive_path = os.path.join(tempfile.gettempdir(), f"jdk-{JDK_DIR_NAME}.{ext}")
        log(f"Downloading JDK from {url}...")
        download_with_progress(url, archive_path, progress=progress)

        log(f"Extracting JDK to {install_dir}...")
        install_dir.mkdir(exist_ok=True, parents=True)
        extract_with_progress(archive_path, str(install_dir), progress=progress)

        # Move contents of extracted `jdk-{JDK_DIR_NAME}` to the destination
        extracted_root = os.path.join(install_dir, f"jdk-{JDK_DIR_NAME}")
        for item in os.listdir(extracted_root):
            shutil.move(os.path.join(extracted_root, item), str(install_dir))

        shutil.rmtree(extracted_root)  # remove root

        # Step 6: Clean up archive
        os.remove(archive_path)

    log(f"JDK installed at {install_dir}")

    if platform.system() == "Darwin":
        install_dir = install_dir / "Contents" / "Home"

    return str(install_dir)


# Example usage
if __name__ == "__main__":
    console = Console()
    jdk_path = install_jdk(lambda m: console.log(m))
    print(f"JDK path: {jdk_path}")
