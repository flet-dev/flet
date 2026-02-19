import hashlib


def sha1(input_string):
    """
    Calculates SHA-1 digest for a UTF-8 string.

    Args:
        input_string: Input text to hash.

    Returns:
        Hexadecimal SHA-1 digest string.
    """
    sha1_hash = hashlib.sha1()
    sha1_hash.update(input_string.encode("utf-8"))
    return sha1_hash.hexdigest()


def calculate_file_hash(path, blocksize=65536):
    """
    Calculates SHA-256 digest for a file.

    The file is read incrementally using `blocksize` chunks.

    Args:
        path: Path to the file.
        blocksize: Number of bytes to read per iteration.

    Returns:
        Hexadecimal SHA-256 digest string.

    Raises:
        OSError: If the file cannot be opened or read.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            h.update(data)
    return h.hexdigest()
