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
    """Extracts an archive with a progress bar and preserves file attributes, including symbolic links."""
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as archive:
            total_files = len(archive.namelist())
            if progress:
                task = progress.add_task("Extracting...", total=total_files)
            for member in archive.namelist():
                member_info = archive.getinfo(member)
                # Check if the member is a symbolic link
                is_symlink = (member_info.external_attr >> 16) & 0o120000 == 0o120000
                extracted_path = os.path.join(extract_to, member_info.filename)

                if is_symlink:
                    # Read the target of the symlink from the archive
                    with archive.open(member_info) as target_file:
                        target = target_file.read().decode("utf-8")
                    # Create the symbolic link
                    os.symlink(target, extracted_path)
                else:
                    # Extract regular files and directories
                    archive.extract(member_info, extract_to)

                    # Preserve permissions
                    if member_info.external_attr > 0xFFFF:
                        os.chmod(extracted_path, member_info.external_attr >> 16)

                if progress:
                    progress.update(task, advance=1)
            if progress:
                progress.remove_task(task)

    elif archive_path.endswith(".tar.xz") or archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:*") as archive:
            members = archive.getmembers()
            total_files = len(members)
            if progress:
                task = progress.add_task("Extracting...", total=total_files)
            for member in members:
                extracted_path = os.path.join(extract_to, member.name)

                if member.issym():
                    # Create symbolic link manually
                    os.symlink(member.linkname, extracted_path)
                elif member.islnk():
                    # Create hard link manually
                    os.link(os.path.join(extract_to, member.linkname), extracted_path)
                else:
                    # Extract regular files and directories
                    archive.extract(member, extract_to)

                # Preserve permissions
                if member.isfile() or member.isdir():
                    os.chmod(extracted_path, member.mode)

                if progress:
                    progress.update(task, advance=1)
            if progress:
                progress.remove_task(task)
