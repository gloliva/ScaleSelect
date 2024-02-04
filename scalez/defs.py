"""
Author: Gregg Oliva
"""
# stdlib imports
from collections import namedtuple
from enum import Enum


# Class Definitions
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
    MAJOR = "Major"
    MINOR = "minor"
    HARMONIC_MINOR = "Harmonic minor"
    MELODIC_MINOR = "Melodic minor"


Key = namedtuple("Key", ["name", "value", "accidental"])


# Exclusions
class ExcludeType(Enum):
    KEYS = 0
    ACCIDENTALS = 1
    SCALE_TYPES = 2


IGNORED_KEYS = {
    # Ignored Sharps
    f"{Natural.A.value}{Accidental.SHARP.value}",
    f"{Natural.B.value}{Accidental.SHARP.value}",
    f"{Natural.C.value}{Accidental.SHARP.value}",
    f"{Natural.D.value}{Accidental.SHARP.value}",
    f"{Natural.E.value}{Accidental.SHARP.value}",
    f"{Natural.G.value}{Accidental.SHARP.value}",
    # Ignored Flats
    f"{Natural.F.value}{Accidental.FLAT.value}",
}


# Complete Lists
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
ALL_SCALE_TYPES = [ScaleType.MAJOR, ScaleType.MINOR, ScaleType.HARMONIC_MINOR, ScaleType.MELODIC_MINOR]
ALL_EXCLUDED_TYPES = [ExcludeType.KEYS, ExcludeType.ACCIDENTALS, ExcludeType.SCALE_TYPES]
