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

from typing import Dict, Any, TypeVar, Union, Sequence
from typing_extensions import Protocol

import typing


class _JsonList(Protocol):
    def __getitem__(self, idx: int) -> "Json":
        ...

    # hack to enforce an actual list
    def sort(self) -> None:
        ...


class _JsonDict(Protocol):
    def __getitem__(self, key: str) -> "Json":
        ...

    # hack to enforce an actual dict
    @staticmethod
    @typing.overload
    def fromkeys(seq: Sequence[Any]) -> Dict[Any, Any]:
        ...

    @staticmethod  # noqa: F811
    @typing.overload
    def fromkeys(seq: Sequence[Any], value: Any) -> Dict[Any, Any]:
        ...


Json = Union[str, int, float, bool, None, _JsonList, _JsonDict]

_TJson = TypeVar("_TJson", bound=Json)


class AttrDict(Dict[str, _TJson]):
    def __getitem__(self, name_or_index: str) -> _TJson:
        try:
            value = dict.__getitem__(self, name_or_index)

        except KeyError:
            if name_or_index == "_from":
                value = self["from"]

            else:
                raise

        return value

    def __getattr__(self, name_or_index: str) -> _TJson:
        try:
            return self[name_or_index]

        except KeyError as e:
            raise AttributeError from e
