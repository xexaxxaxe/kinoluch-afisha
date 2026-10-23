from ..db import get_db
from ..models import Order
from . import queries
from . import showtimes as showtimes_repo


def begin():
    """Начинает транзакцию: пока она идёт, никто другой не может записывать в базу."""
    get_db().execute("BEGIN IMMEDIATE")


def commit():
    get_db().commit()


def rollback():
    get_db().rollback()


def create(user_id, showtime_id, total, tickets):
    """tickets — список (ряд, место, цена). Возвращает id заказа."""
    db = get_db()
    cursor = db.execute(queries.INSERT_ORDER, (user_id, showtime_id, total))
    order_id = cursor.lastrowid
    db.executemany(
        queries.INSERT_TICKET,
        [(order_id, row, seat, price) for row, seat, price in tickets],
    )
    return order_id


def _to_order(row):
    seats = [
        (r["row_no"], r["seat_no"])
        for r in get_db().execute(queries.ORDER_SEATS, (row["id"],)).fetchall()
    ]
    return Order(
        id=row["id"],
        user_id=row["user_id"],
        showtime=showtimes_repo.get(row["showtime_id"]),
        total=row["total"],
        status=row["status"],
        created=row["created"],
        seats=seats,
    )


def for_user(user_id):
    rows = get_db().execute(queries.ORDERS_BY_USER, (user_id,)).fetchall()
    return [_to_order(r) for r in rows]


def get(order_id, user_id):
    row = get_db().execute(queries.ORDER_BY_ID, (order_id, user_id)).fetchone()
    return _to_order(row) if row else None


def cancel(order_id):
    db = get_db()
    db.execute(queries.CANCEL_ORDER, (order_id,))
    db.commit()
