from dataclasses import dataclass
from datetime import datetime

from .hall import Hall
from .movie import Movie


@dataclass
class Showtime:
    id: int
    start: datetime
    movie: Movie
    hall: Hall

    def is_past(self, now=None):
        now = now or datetime.now()
        return self.start <= now

    def minutes_left(self, now=None):
        """Сколько минут осталось до начала сеанса (отрицательное — уже начался)."""
        now = now or datetime.now()
        return int((self.start - now).total_seconds() // 60)
