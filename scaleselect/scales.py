"""
Author: Gregg Oliva
"""
# stdlib imports
from random import choice
from typing import Iterable, List, Set

# project imports
from defaults import EXCLUDE_SCALES


class Accidental:
    NATURAL = ""
    SHARP = "#"
    FLAT = "b"


class Quality:
    MAJOR = "major"
    MINOR = "minor"
    HARMONIC = "harmonic minor"
    MELODIC = "melodic minor"


class Scales:
    LETTERS = ["A", "B", "C", "D", "E", "F", "G"]
    ALL_ACCIDENTALS = [Accidental.NATURAL, Accidental.SHARP, Accidental.FLAT]
    ALL_QUALITIES = [Quality.MAJOR, Quality.MINOR, Quality.HARMONIC, Quality.MELODIC]

    def __init__(self) -> None:
        # excluded scales
        self.excluded_scales: Iterable[str] = []
        self.excluded_accidentals: Iterable[str] = []
        self.excluded_qualities: Iterable[str] = []

        # available scales
        self.scales: Set[str] = self.build_scales()

    def build_scales(self) -> Set[str]:
        # handle excluded
        available_accidentals = [accidental for accidental in self.ALL_ACCIDENTALS if accidental not in self.excluded_accidentals]
        available_qualities = [quality for quality in self.ALL_QUALITIES if quality not in self.excluded_qualities]

        scales = set()

        for letter in self.LETTERS:
            for accidental in available_accidentals:
                if f"{letter}{accidental}" in EXCLUDE_SCALES:
                    continue

                for quality in available_qualities:
                    scale = f"{letter}{accidental} {quality}"
                    scales.add(scale)

        return scales

    def get_random(self, n: int = 1,) -> List[str]:
        scales = []
        available_scales = list(self.scales.copy())

        for _ in range(n):
            selected = choice(available_scales)
            scales.append(selected)
            available_scales.remove(selected)

        return scales
