from __future__ import annotations


class PersonBase:
    """Common person attributes shared by Teacher/Student."""

    def __init__(self, name: str) -> None:
        self.name = name

