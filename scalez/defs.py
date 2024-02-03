"""
Author: Gregg Oliva
"""
# stdlib imports
from collections import namedtuple
from enum import Enum


class Accidental(Enum):
    NATURAL = ""
    SHARP = "#"
    FLAT = "b"


class Natural(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class ScaleType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    HARMONIC = "harmonic minor"
    MELODIC = "melodic minor"


Key = namedtuple("Key", ["name", "value", "accidental"])


ALL_NATURALS = [Natural.A, Natural.B, Natural.C, Natural.D, Natural.E, Natural.F, Natural.G]
ALL_ACCIDENTALS = [Accidental.NATURAL, Accidental.SHARP, Accidental.FLAT]
ALL_KEYS = [
    Key(
        f"{natural.value}{accidental.value}",
        f"{natural.value}{accidental.value}",
        accidental,
    )
    for natural in ALL_NATURALS
    for accidental in ALL_ACCIDENTALS
]
ALL_SCALE_TYPES = [ScaleType.MAJOR, ScaleType.MINOR, ScaleType.HARMONIC, ScaleType.MELODIC]
