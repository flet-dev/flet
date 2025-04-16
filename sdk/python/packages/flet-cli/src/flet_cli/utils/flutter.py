import os
import platform
import shutil
from pathlib import Path
from typing import Optional

from flet_cli.utils.distros import download_with_progress, extract_with_progress
from rich.console import Console
from rich.progress import Progress


def get_flutter_url(version):
    """Determines the Flutter archive URL based on the platform."""
    system = platform.system()
    machine = platform.machine()

    url_root = "https://storage.googleapis.com/flutter_infra_release/releases/stable"
    if system == "Windows":
        return f"{url_root}/windows/flutter_windows_{version}-stable.zip"
    elif system == "Darwin":
        if machine == "arm64":
            return f"{url_root}/macos/flutter_macos_arm64_{version}-stable.zip"
        else:  # Assume x86_64 for other cases
            return f"{url_root}/macos/flutter_macos_{version}-stable.zip"
    elif system == "Linux":
        return f"{url_root}/linux/flutter_linux_{version}-stable.tar.xz"
    else:
        raise ValueError(f"Unsupported platform: {system}")


def install_flutter(version, log, progress: Optional[Progress] = None):
    home_dir = Path.home()
    install_dir = os.path.join(home_dir, "flutter", version)

    if not os.path.exists(install_dir):
        url = get_flutter_url(version)
        archive_name = os.path.basename(url)
        archive_path = os.path.join(home_dir, archive_name)

        log(f"Downloading Flutter {version} from {url}...")
        download_with_progress(url, archive_path, progress=progress)

        log(f"Extracting Flutter to {install_dir}...")
        temp_extract_dir = os.path.join(home_dir, "flutter", f"{version}_temp")
        os.makedirs(temp_extract_dir, exist_ok=True)

        extract_with_progress(archive_path, temp_extract_dir, progress=progress)

        # Move extracted 'flutter' directory contents to final destination
        flutter_root = os.path.join(temp_extract_dir, "flutter")
        shutil.move(flutter_root, install_dir)

        # Clean up
        os.remove(archive_path)
        shutil.rmtree(temp_extract_dir)

        log(f"Flutter {version} installed at {install_dir}.")
    return install_dir


# Example usage:
if __name__ == "__main__":
    flutter_version = "3.24.3"
    console = Console()
    install_dir = install_flutter(flutter_version, lambda m: console.log(m))
    print(f"Flutter is ready at: {install_dir}")
