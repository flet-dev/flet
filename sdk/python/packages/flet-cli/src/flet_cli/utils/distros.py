import os
import tarfile
import urllib.request
import zipfile
from typing import Optional

from rich.progress import Progress


def download_with_progress(url, dest_path, progress: Optional[Progress] = None):
    """Downloads a file with a progress bar."""
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get("Content-Length").strip())
        block_size = 8192  # 8 KB chunks

        if progress:
            task = progress.add_task("Downloading...", total=total_size)
        with open(dest_path, "wb") as out_file:
            while chunk := response.read(block_size):
                out_file.write(chunk)
                if progress:
                    progress.update(task, advance=len(chunk))
        if progress:
            progress.remove_task(task)


def extract_with_progress(
    archive_path, extract_to, progress: Optional[Progress] = None
):
    """Extracts an archive with a progress bar and preserves file attributes."""
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as archive:
            total_files = len(archive.namelist())
            if progress:
                task = progress.add_task("Extracting...", total=total_files)
            for member in archive.namelist():
                member = archive.getinfo(member)
                archive.extract(member, extract_to)
                if progress:
                    progress.update(task, advance=1)
                # preserve permissions
                extracted_path = os.path.join(extract_to, member.filename)
                if member.external_attr > 0xFFFF:
                    os.chmod(extracted_path, member.external_attr >> 16)
            if progress:
                progress.remove_task(task)
    elif archive_path.endswith(".tar.xz") or archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:*") as archive:
            members = archive.getmembers()
            total_files = len(members)
            if progress:
                task = progress.add_task("Extracting...", total=total_files)
            for member in members:
                archive.extract(member, extract_to)
                if progress:
                    progress.update(task, advance=1)
                # Preserve permissions (executable flags, etc.)
                extracted_path = os.path.join(extract_to, member.name)
                if member.isfile():
                    os.chmod(extracted_path, member.mode)
            if progress:
                progress.remove_task(task)
