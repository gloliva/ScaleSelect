"""
Author: Gregg Oliva
"""
# stdlib imports
from enum import Enum
from random import choice
from typing import Iterable, List, Set

# project imports
from defs import (
    Accidental,
    ScaleType,
    Key,
    ExcludeType,
    ALL_KEYS,
    ALL_SCALE_TYPES,
)


class ScaleBuilder:
    def __init__(self) -> None:
        # excluded scales
        self.excluded_keys: Iterable[Key] = []
        self.excluded_accidentals: Iterable[Accidental] = []
        self.excluded_scale_types: Iterable[ScaleType] = []

        # available scales
        self.scales: Set[str] = set()
        self.build_scales()

    def build_scales(self) -> None:
        # handle excluded
        available_scale_types = [
            scale_type
            for scale_type in ALL_SCALE_TYPES
            if scale_type not in self.excluded_scale_types
        ]

        scales = set()

        for key in ALL_KEYS:
            if key in self.excluded_keys:
                continue

            if key.accidental in self.excluded_accidentals:
                continue

            for scale_type in available_scale_types:
                scale = f"{key.value} {scale_type.value}"
                scales.add(scale)

        self.scales = scales

    def update_excludes(self, exclude_type: ExcludeType, exclude_list: Iterable) -> None:
        if exclude_type == ExcludeType.KEYS:
            self.excluded_keys = exclude_list
        elif exclude_type == ExcludeType.ACCIDENTALS:
            self.excluded_accidentals = exclude_list
        elif exclude_type == ExcludeType.SCALE_TYPES:
            self.excluded_scale_types = exclude_list

    def get_random(self, n: int = 1) -> List[str]:
        scales = []
        available_scales = list(self.scales.copy())

        if not available_scales:
            return []

        for _ in range(n):
            selected = choice(available_scales)
            scales.append(selected)
            available_scales.remove(selected)

        return scales
