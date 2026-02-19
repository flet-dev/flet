import secrets
import string


def random_string(length):
    """
    Generates a cryptographically secure random alphanumeric string.

    Args:
        length: Desired output length.

    Returns:
        A random string containing ASCII letters and digits.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
