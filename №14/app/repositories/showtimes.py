from datetime import datetime

from ..db import get_db
from ..models import Hall, Movie, Showtime
from . import queries


def _to_showtime(row):
    return Showtime(
        id=row["id"],
        start=datetime.strptime(row["start"], "%Y-%m-%d %H:%M"),
        movie=Movie(
            id=row["movie_id"],
            title=row["title"],
            duration_min=row["duration_min"],
            age=row["age"],
            description=row["description"],
        ),
        hall=Hall(
            id=row["hall_id"],
            name=row["hall_name"],
            rows=row["rows_count"],
            seats=row["seats_count"],
        ),
    )


def get(showtime_id):
    row = get_db().execute(queries.SHOWTIME_BY_ID, (showtime_id,)).fetchone()
    return _to_showtime(row) if row else None


def for_day(day):
    rows = get_db().execute(queries.SHOWTIMES_BY_DAY, (day.isoformat(),)).fetchall()
    return [_to_showtime(r) for r in rows]


def taken_seats(showtime_id):
    """Занятые места сеанса: список пар (ряд, место)."""
    rows = get_db().execute(queries.TAKEN_SEATS, (showtime_id,)).fetchall()
    return [(r["row_no"], r["seat_no"]) for r in rows]


def count_taken(showtime_id):
    return get_db().execute(queries.COUNT_TAKEN, (showtime_id,)).fetchone()[0]
