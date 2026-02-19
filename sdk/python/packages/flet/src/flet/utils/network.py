import socket


def get_free_tcp_port():
    """
    Returns an available local TCP port selected by the operating system.

    The port is discovered by binding a socket to port `0`.

    Returns:
        A TCP port number that was available at discovery time.
    """
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def get_local_ip():
    """
    Returns the local IPv4 address used for outbound network traffic.

    This function first infers the address by opening a UDP socket to `8.8.8.8`.
    If that fails, it falls back to resolving the machine hostname.

    Returns:
        Local IPv4 address.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
