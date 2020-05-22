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

from typing import Dict, Any


class AttrDict(Dict[str, Any]):
    def __getitem__(self, name_or_index: str) -> Any:
        try:
            value = dict.__getitem__(self, name_or_index)

        except KeyError:
            if name_or_index == "_from":
                value = self["from"]

            else:
                raise

        return value

    def __getattr__(self, name_or_index: str) -> Any:
        try:
            return self[name_or_index]

        except KeyError as e:
            raise AttributeError from e
