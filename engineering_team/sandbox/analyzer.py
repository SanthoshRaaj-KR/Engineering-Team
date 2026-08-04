from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

VOWELS = frozenset("aeiouAEIOU")


@dataclass(frozen=True)
class CharacterCounts:
    vowels: int
    consonants: int
    special_characters: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "vowels": self.vowels,
            "consonants": self.consonants,
            "special_characters": self.special_characters,
        }


def analyze_text(text: str) -> CharacterCounts:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    vowels = 0
    consonants = 0
    special_characters = 0

    for character in text:
        if character.isalpha():
            if character in VOWELS:
                vowels += 1
            else:
                consonants += 1
        else:
            special_characters += 1

    return CharacterCounts(vowels=vowels, consonants=consonants, special_characters=special_characters)
