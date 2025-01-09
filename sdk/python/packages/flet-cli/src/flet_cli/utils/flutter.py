import os
import platform
import shutil
from pathlib import Path

from flet_cli.utils.distros import download_with_progress, extract_with_progress


def get_flutter_url(version):
    """Determines the Flutter archive URL based on the platform."""
    system = platform.system()
    machine = platform.machine()

    if system == "Windows":
        return f"https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_{version}-stable.zip"
    elif system == "Darwin":
        if machine == "arm64":
            return f"https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_{version}-stable.zip"
        else:  # Assume x86_64 for other cases
            return f"https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_{version}-stable.zip"
    elif system == "Linux":
        return f"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_{version}-stable.tar.xz"
    else:
        raise ValueError(f"Unsupported platform: {system}")


def install_flutter(version):
    home_dir = Path.home()
    install_dir = os.path.join(home_dir, "flutter", version)

    if os.path.exists(install_dir):
        print(f"Flutter {version} is already installed at {install_dir}.")
        return install_dir

    url = get_flutter_url(version)
    archive_name = os.path.basename(url)
    archive_path = os.path.join(home_dir, archive_name)

    print(f"Downloading Flutter {version} from {url}...")
    download_with_progress(url, archive_path)

    print(f"Extracting to {install_dir}...")
    temp_extract_dir = os.path.join(home_dir, "flutter", f"{version}_temp")
    os.makedirs(temp_extract_dir, exist_ok=True)

    extract_with_progress(archive_path, temp_extract_dir)

    # Move extracted 'flutter' directory contents to final destination
    flutter_root = os.path.join(temp_extract_dir, "flutter")
    shutil.move(flutter_root, install_dir)

    # Clean up
    os.remove(archive_path)
    shutil.rmtree(temp_extract_dir)

    print(f"Flutter {version} installed at {install_dir}.")
    return install_dir


# Example usage:
if __name__ == "__main__":
    flutter_version = "3.24.3"
    install_dir = install_flutter(flutter_version)
    print(f"Flutter is ready at: {install_dir}")
