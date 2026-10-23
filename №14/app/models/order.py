from dataclasses import dataclass, field

from .showtime import Showtime


@dataclass
class Order:
    id: int
    user_id: int
    showtime: Showtime
    total: int
    status: str
    created: str
    seats: list = field(default_factory=list)   # [(ряд, место), ...]

    @property
    def is_paid(self):
        return self.status == "paid"
