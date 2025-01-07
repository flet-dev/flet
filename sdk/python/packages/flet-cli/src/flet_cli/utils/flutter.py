import os
import platform
import shutil
import tarfile
import urllib.request
import zipfile

from tqdm import tqdm


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


def download_with_progress(url, dest_path):
    """Downloads a file with a progress bar."""
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get("Content-Length").strip())
        block_size = 8192  # 8 KB chunks

        with open(dest_path, "wb") as out_file, tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Downloading"
        ) as pbar:
            while chunk := response.read(block_size):
                out_file.write(chunk)
                pbar.update(len(chunk))


def extract_with_progress(archive_path, extract_to):
    """Extracts an archive with a progress bar and preserves file attributes."""
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as archive:
            total_files = len(archive.namelist())
            with tqdm(total=total_files, unit="files", desc="Extracting") as pbar:
                for member in archive.namelist():
                    member = archive.getinfo(member)
                    archive.extract(member, extract_to)
                    pbar.update(1)
                    # preserve permissions
                    extracted_path = os.path.join(extract_to, member.filename)
                    if member.external_attr > 0xFFFF:
                        os.chmod(extracted_path, member.external_attr >> 16)
    elif archive_path.endswith(".tar.xz"):
        with tarfile.open(archive_path, "r:xz") as archive:
            members = archive.getmembers()
            total_files = len(members)
            with tqdm(total=total_files, unit="files", desc="Extracting") as pbar:
                for member in members:
                    archive.extract(member, extract_to)
                    pbar.update(1)
                    # Preserve permissions (executable flags, etc.)
                    extracted_path = os.path.join(extract_to, member.name)
                    if member.isfile():
                        os.chmod(extracted_path, member.mode)


def install_flutter(version):
    """Installs Flutter for the current platform."""
    home_dir = os.path.expanduser("~")
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
