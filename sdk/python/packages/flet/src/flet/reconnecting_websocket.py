import logging
import random
import threading

import websocket

from flet.utils import is_localhost_url

_REMOTE_CONNECT_TIMEOUT_SEC = 5
_LOCAL_CONNECT_TIMEOUT_SEC = 0.2


class ReconnectingWebSocket:
    def __init__(
        self, url, on_connect=None, on_failed_connect=None, on_message=None
    ) -> None:
        self._url = url
        self._on_connect_handler = on_connect
        self._on_failed_connect_handler = on_failed_connect
        self._on_message_handler = on_message
        self.connected = threading.Event()
        self.exit = threading.Event()
        self.retry = 0
        # disable websocket logging completely
        # https://github.com/websocket-client/websocket-client/blob/master/websocket/_logging.py#L22-L51
        ws_logger = logging.getLogger("websocket")
        ws_logger.setLevel(logging.FATAL)

    def _on_open(self, wsapp) -> None:
        logging.info(f"Successfully connected to {self._url}")
        websocket.setdefaulttimeout(self.default_timeout)
        self.connected.set()
        self.retry = 0
        if self._on_connect_handler is not None:
            th = threading.Thread(target=self._on_connect_handler, args=(), daemon=True)
            th.start()

    def _on_message(self, wsapp, data) -> None:
        if self._on_message_handler is not None:
            self._on_message_handler(data)

    def connect(self) -> None:
        self.wsapp = websocket.WebSocketApp(
            self._url, on_message=self._on_message, on_open=self._on_open
        )
        th = threading.Thread(target=self._connect_loop, args=(), daemon=True)
        th.start()

    def send(self, message) -> None:
        self.connected.wait()
        self.wsapp.send(message)

    def close(self) -> None:
        self.exit.set()
        self.wsapp.close()

    def _connect_loop(self):
        while not self.exit.is_set():
            logging.info(f"Connecting Flet Server at {self._url}...")
            self.default_timeout = websocket.getdefaulttimeout()
            websocket.setdefaulttimeout(
                _LOCAL_CONNECT_TIMEOUT_SEC
                if is_localhost_url(self._url)
                else _REMOTE_CONNECT_TIMEOUT_SEC
            )
            r = self.wsapp.run_forever()
            logging.debug(f"Exited run_forever()")
            websocket.setdefaulttimeout(self.default_timeout)
            self.connected.clear()
            if r != True:
                return

            if self.retry == 0 and self._on_failed_connect_handler is not None:
                th = threading.Thread(
                    target=self._on_failed_connect_handler, args=(), daemon=True
                )
                th.start()

            backoff_in_seconds = 1
            sleep = 0.1
            if not is_localhost_url(self._url):
                sleep = backoff_in_seconds * 2**self.retry + random.uniform(0, 1)
            logging.info(f"Reconnecting Flet Server in {sleep} seconds")
            self.exit.wait(sleep)
            self.retry += 1
