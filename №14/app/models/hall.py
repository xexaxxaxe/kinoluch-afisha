from dataclasses import dataclass

import config


@dataclass
class Hall:
    id: int
    name: str
    rows: int
    seats: int

    @property
    def capacity(self):
        return self.rows * self.seats

    def is_vip(self, row):
        """Ряды нумеруются с 1. VIP — последние config.VIP_ROWS рядов."""
        return row > self.rows - config.VIP_ROWS
