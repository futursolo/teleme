#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2020 Kaede Hoshikawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import Any, Callable, Awaitable

from . import _methods
from ._exceptions import TelemeException, MalformedResponse, FailedRequest
from ._collections import AttrDict, Json
from ._version import get_versions

import hiyori
import json
import functools
import typing

__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "Api", "AttrDict",
    "TelemeException", "MalformedResponse", "FailedRequest",
    "__version__"]

_USER_AGENT = "teleme/{} hiyori/{}".format(__version__, hiyori.__version__)

_DEFAULT_BASE_URL = "https://api.telegram.org/bot{token}/{method}"


class Api:
    def __init__(
        self, token: str, *, base_url: str = _DEFAULT_BASE_URL,
            user_agent: str = _USER_AGENT, timeout: int = 61) -> None:
        self._token = token
        self._base_url = base_url
        self._user_agent = user_agent

        self._client = hiyori.HttpClient(timeout=timeout)

    def _make_request_url(self, method_name: str) -> str:
        try:
            url_name = _methods.get_url_name(method_name)

        except ValueError as e:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute "
                f"'{method_name}'") from e

        return self._base_url.format(
            token=self._token, method=url_name)

    async def _send_anything(
        self, __request_url: str, __method_name: str,
            **kwargs: Any) -> Json:
        """
        If you want to determine which method will be invoked at runtime,
        please use :code:`getattr(Api(), "method_name")` instead of this
        function.
        """

        # Telegram will cut off requests longer than 60 seconds,
        # but it's better to wait the server close the connection first.
        headers = {
            "User-Agent": self._user_agent,
            "Accept": "application/json",
        }

        r = await self._client.post(
            __request_url, headers=headers, json=kwargs)

        try:
            j = json.loads(r.body.to_str(), object_pairs_hook=AttrDict)

        except json.decoder.JSONDecodeError as e:
            raise MalformedResponse(
                status_code=r.status_code,
                method=__method_name,
                body=r.body.to_str(),
                sent_kwargs=kwargs) from e

        except UnicodeDecodeError as e:
            raise MalformedResponse(
                status_code=r.status_code,
                method=__method_name,
                body=r.body,
                sent_kwargs=kwargs) from e

        if not isinstance(j, AttrDict) or "ok" not in j.keys():
            raise MalformedResponse(
                status_code=r.status_code,
                method=__method_name,
                body=j,
                sent_kwargs=kwargs)

        if not j.ok or r.status_code != 200:
            raise FailedRequest(
                status_code=r.status_code,
                method=__method_name,
                body=j,
                sent_kwargs=kwargs)

        return typing.cast(Json, j.result)

    def __getattr__(self, name: str) -> Callable[..., Awaitable[Json]]:
        return functools.partial(
            self._send_anything, self._make_request_url(name), name)
