import itertools
import logging
from threading import Thread
from time import sleep
from typing import Union

import httpx
from huokanapiclient.api.users import get_me
from huokanapiclient.client import AuthenticatedClient
from rx.subject.behaviorsubject import BehaviorSubject

from huokanadvertiserclient.core.UnauthorizedException import UnauthorizedException


class LoginHandler:
    def __init__(self, client: AuthenticatedClient):
        self._client = client
        self._is_login_in_progress = False
        self._retry_thread: Union[Thread, None] = None

    def log_in(self) -> BehaviorSubject:
        if self._retry_thread is not None:
            raise Exception("Login in progress")
        self._is_login_in_progress = True

        subject = BehaviorSubject(None)
        self._retry_thread = Thread(target=self._retry_login, args=(subject,))
        self._retry_thread.start()

        return subject

    def _retry_login(self, subject: BehaviorSubject):
        for i in itertools.count(start=0):
            if not self._is_login_in_progress:
                break
            try:
                me_response = get_me.sync_detailed(client=self._client)
                if me_response.status_code == 401:
                    subject.on_error(UnauthorizedException())
                else:
                    subject.on_completed()
                return
            except httpx.RequestError as ex:
                logging.debug("HTTP request failed (%d): %s", i, ex)
            sleep(5)

    def cancel(self):
        self._is_login_in_progress = False
        self._retry_thread = None
