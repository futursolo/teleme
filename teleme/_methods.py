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

from typing import Dict

import threading
import re

_GLOBAL_LOCK = threading.Lock()

_NAME_RE = re.compile(r"^[a-z]([a-z\_]+)?$")

_CACHED_METHODS: Dict[str, str] = {}


def get_url_name(attr_name: str) -> str:
    """
    Translate pep8 compliant names to telegram api method names.
    """
    with _GLOBAL_LOCK:
        if attr_name not in _CACHED_METHODS.keys():
            if _NAME_RE.fullmatch(attr_name) is None:
                raise ValueError(
                    f"Unacceptable API Method Name: `{attr_name}`, "
                    f"r\"{_NAME_RE.pattern}\" is expected.")

            _CACHED_METHODS[attr_name] = attr_name.replace("_", "")

        return _CACHED_METHODS[attr_name]
