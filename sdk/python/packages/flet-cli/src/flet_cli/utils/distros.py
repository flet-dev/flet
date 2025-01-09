import os
import tarfile
import urllib.request
import zipfile

from rich.progress import Progress


def download_with_progress(url, dest_path):
    """Downloads a file with a progress bar."""
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get("Content-Length").strip())
        block_size = 8192  # 8 KB chunks

        with Progress(transient=True) as progress:
            task = progress.add_task("Downloading...", total=total_size)
            with open(dest_path, "wb") as out_file:
                while chunk := response.read(block_size):
                    out_file.write(chunk)
                    progress.update(task, advance=len(chunk))


def extract_with_progress(archive_path, extract_to):
    """Extracts an archive with a progress bar and preserves file attributes."""
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as archive:
            total_files = len(archive.namelist())
            with Progress(transient=True) as progress:
                task = progress.add_task("Extracting...", total=total_files)
                for member in archive.namelist():
                    member = archive.getinfo(member)
                    archive.extract(member, extract_to)
                    progress.update(task, advance=1)
                    # preserve permissions
                    extracted_path = os.path.join(extract_to, member.filename)
                    if member.external_attr > 0xFFFF:
                        os.chmod(extracted_path, member.external_attr >> 16)
    elif archive_path.endswith(".tar.xz") or archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:*") as archive:
            members = archive.getmembers()
            total_files = len(members)
            with Progress(transient=True) as progress:
                task = progress.add_task("Extracting...", total=total_files)
                for member in members:
                    archive.extract(member, extract_to)
                    progress.update(task, advance=1)
                    # Preserve permissions (executable flags, etc.)
                    extracted_path = os.path.join(extract_to, member.name)
                    if member.isfile():
                        os.chmod(extracted_path, member.mode)
