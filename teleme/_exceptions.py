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

from typing import Any, Union, Dict

from ._collections import AttrDict, Json


class TelemeException(Exception):
    def __init__(
        self, *, status_code: int, method: str,
        body: Union[AttrDict[Json], str, bytes],
            sent_kwargs: Dict[str, Any]) -> None:
        self.method = method
        self.sent_kwargs = sent_kwargs

        self.status_code = status_code
        self.body = body

        super().__init__(
            f"Request: {self.method}({repr(self.sent_kwargs)})\n"
            f"Status Code: {self.status_code}\n"
            f"Response Body: \n{repr(self.body)}")


class FailedRequest(TelemeException):
    pass


class MalformedResponse(TelemeException):
    pass
