from dataclasses import dataclass


@dataclass
class Movie:
    id: int
    title: str
    duration_min: int
    age: str
    description: str
