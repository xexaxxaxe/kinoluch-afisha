"""Все SQL-запросы приложения в одном месте."""

_SHOWTIME_COLUMNS = """
    s.id, s.start,
    m.id AS movie_id, m.title, m.duration_min, m.age, m.description,
    h.id AS hall_id, h.name AS hall_name, h.rows_count, h.seats_count
FROM showtimes s
JOIN movies m ON m.id = s.movie_id
JOIN halls h ON h.id = s.hall_id
"""

SHOWTIME_BY_ID = "SELECT" + _SHOWTIME_COLUMNS + "WHERE s.id = ?"

SHOWTIMES_BY_DAY = (
    "SELECT" + _SHOWTIME_COLUMNS + "WHERE date(s.start) = ? ORDER BY m.title, s.start"
)

TAKEN_SEATS = """
SELECT t.row_no, t.seat_no
FROM tickets t
JOIN orders o ON o.id = t.order_id
WHERE o.showtime_id = ? AND o.status = 'paid'
"""

COUNT_TAKEN = """
SELECT COUNT(t.id)
FROM tickets t
JOIN orders o ON o.id = t.order_id
WHERE o.showtime_id = ? AND o.status = 'paid'
"""

INSERT_ORDER = "INSERT INTO orders (user_id, showtime_id, total) VALUES (?, ?, ?)"

INSERT_TICKET = "INSERT INTO tickets (order_id, row_no, seat_no, price) VALUES (?, ?, ?, ?)"

ORDERS_BY_USER = "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC"

ORDER_BY_ID = "SELECT * FROM orders WHERE id = ? AND user_id = ?"

ORDER_SEATS = "SELECT row_no, seat_no FROM tickets WHERE order_id = ? ORDER BY row_no, seat_no"

CANCEL_ORDER = "UPDATE orders SET status = 'cancelled' WHERE id = ?"
