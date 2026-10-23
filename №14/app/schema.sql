CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    duration_min INTEGER NOT NULL,
    age TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rows_count INTEGER NOT NULL,
    seats_count INTEGER NOT NULL
);

-- start хранится как 'ГГГГ-ММ-ДД ЧЧ:ММ'
CREATE TABLE IF NOT EXISTS showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL REFERENCES movies (id),
    hall_id INTEGER NOT NULL REFERENCES halls (id),
    start TEXT NOT NULL
);

-- status: 'paid' — оплачен, 'cancelled' — возвращён
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users (id),
    showtime_id INTEGER NOT NULL REFERENCES showtimes (id),
    total INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'paid',
    created TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders (id),
    row_no INTEGER NOT NULL,
    seat_no INTEGER NOT NULL,
    price INTEGER NOT NULL
);
