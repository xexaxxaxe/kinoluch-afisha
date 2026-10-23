"""Начальные данные: фильмы, залы и расписание сеансов на ближайшие дни."""
from datetime import date, timedelta

import config

MOVIES = [
    ("Тайна старого маяка", 105, "6+", "Двое школьников находят на чердаке карту и отправляются к заброшенному маяку."),
    ("Скорость света", 128, "16+", "Гонщица-новичок попадает в команду, где все хотят её подставить."),
    ("Мультяшки в космосе", 92, "0+", "Весёлая команда зверят строит ракету из старого холодильника."),
    ("Последний рубеж", 141, "12+", "Экспедиция на краю Антарктиды получает странный сигнал из-подо льда."),
]

HALLS = [
    ("Большой зал", 8, 10),
    ("Малый зал", 6, 8),
]

# Время начала сеансов в каждом зале (номер зала -> список времён)
TIMES = {
    1: ["10:00", "13:00", "16:30", "19:00", "22:00"],
    2: ["11:30", "15:00", "18:30", "21:30"],
}


def fill(db):
    if db.execute("SELECT COUNT(*) FROM movies").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO movies (title, duration_min, age, description) VALUES (?, ?, ?, ?)",
            MOVIES,
        )
    if db.execute("SELECT COUNT(*) FROM halls").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO halls (name, rows_count, seats_count) VALUES (?, ?, ?)",
            HALLS,
        )

    movie_ids = [r[0] for r in db.execute("SELECT id FROM movies ORDER BY id")]
    today = date.today()
    for offset in range(config.DAYS_AHEAD):
        day = today + timedelta(days=offset)
        exists = db.execute(
            "SELECT COUNT(*) FROM showtimes WHERE date(start) = ?", (day.isoformat(),)
        ).fetchone()[0]
        if exists:
            continue
        for hall_id, times in TIMES.items():
            for slot, time_text in enumerate(times):
                movie_id = movie_ids[(day.toordinal() + slot + hall_id) % len(movie_ids)]
                db.execute(
                    "INSERT INTO showtimes (movie_id, hall_id, start) VALUES (?, ?, ?)",
                    (movie_id, hall_id, f"{day.isoformat()} {time_text}"),
                )
