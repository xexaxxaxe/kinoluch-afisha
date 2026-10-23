"""Покупка и возврат билетов."""
import config

from ..repositories import orders as orders_repo
from ..repositories import showtimes as showtimes_repo
from . import pricing


class BookingError(Exception):
    pass


def book(user_id, showtime, seats):
    """seats — то, что прислал браузер: [[ряд, место], ...]. Возвращает id заказа."""
    if showtime.is_past():
        raise BookingError("Этот сеанс уже начался")
    if not isinstance(seats, list) or not seats:
        raise BookingError("Выберите хотя бы одно место")
    if len(seats) > config.MAX_SEATS:
        raise BookingError(f"За один раз можно купить не больше {config.MAX_SEATS} билетов")

    try:
        requested = [[int(row), int(number)] for row, number in seats]
    except (TypeError, ValueError):
        raise BookingError("Неверный формат мест")

    hall = showtime.hall
    for row, number in requested:
        if not (1 <= row <= hall.rows and 1 <= number <= hall.seats):
            raise BookingError(f"Такого места нет: ряд {row}, место {number}")
    for seat in requested:
        if requested.count(seat) > 1:
            raise BookingError("Одно и то же место выбрано два раза")

    orders_repo.begin()
    try:
        taken = showtimes_repo.taken_seats(showtime.id)
        for seat in requested:
            if seat in taken:
                raise BookingError(
                    f"Место {seat[1]} в ряду {seat[0]} уже занято — обновите страницу"
                )
        tickets = [(row, number, pricing.seat_price(showtime, row)) for row, number in requested]
        total = sum(price for _, _, price in tickets)
        order_id = orders_repo.create(user_id, showtime.id, total, tickets)
    except Exception:
        orders_repo.rollback()
        raise
    orders_repo.commit()
    return order_id


def can_cancel(order):
    return order.is_paid and order.showtime.minutes_left() >= config.CANCEL_MINUTES


def cancel(user_id, order_id):
    order = orders_repo.get(order_id, user_id)
    if order is None:
        raise BookingError("Заказ не найден")
    if not order.is_paid:
        raise BookingError("Этот заказ уже отменён")
    if not can_cancel(order):
        raise BookingError(
            f"Вернуть билет можно не позже чем за {config.CANCEL_MINUTES} минут до начала сеанса"
        )
    orders_repo.cancel(order_id)
