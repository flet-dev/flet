import logging
import random
import threading

import websocket

from flet.utils import is_localhost_url

_REMOTE_CONNECT_TIMEOUT_SEC = 5
_LOCAL_CONNECT_TIMEOUT_SEC = 0.2


class ReconnectingWebSocket:
    def __init__(self, url) -> None:
        self._url = url
        self._on_connect_handler = None
        self._on_failed_connect_handler = None
        self._on_message_handler = None
        self.connected = threading.Event()
        self.exit = threading.Event()
        self.retry = 0
        websocket.setdefaulttimeout(
            _LOCAL_CONNECT_TIMEOUT_SEC
            if is_localhost_url(url)
            else _REMOTE_CONNECT_TIMEOUT_SEC
        )

    @property
    def on_connect(self, handler):
        return self._on_connect_handler

    @on_connect.setter
    def on_connect(self, handler):
        self._on_connect_handler = handler

    @property
    def on_failed_connect(self, handler):
        return self._on_failed_connect_handler

    @on_failed_connect.setter
    def on_failed_connect(self, handler):
        self._on_failed_connect_handler = handler

    @property
    def on_message(self, handler):
        return self._on_message_handler

    @on_message.setter
    def on_message(self, handler):
        self._on_message_handler = handler

    def _on_open(self, wsapp) -> None:
        logging.info(f"Successfully connected to {self._url}")
        self.connected.set()
        self.retry = 0
        if self._on_connect_handler != None:
            th = threading.Thread(target=self._on_connect_handler, args=(), daemon=True)
            th.start()

    def _on_message(self, wsapp, data) -> None:
        if self._on_message_handler != None:
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

    # TODO: Can't do CTRL+C while it sleeps between re-connects
    # Change to Event: https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python
    def _connect_loop(self):
        while not self.exit.is_set():
            logging.info(f"Connecting Flet Server at {self._url}...")
            r = self.wsapp.run_forever()
            logging.debug(f"Exited run_forever()")
            self.connected.clear()
            if r != True:
                return

            if self.retry == 0 and self._on_failed_connect_handler != None:
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
